from __future__ import annotations

import os
import re
from datetime import date, datetime, timedelta
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any
from urllib.parse import parse_qsl, urlencode, urlparse, urlunparse

from .config import ensure_layout, load_watchlist, project_root
from .db import delete_candidates_by_urls, delete_scan_candidates_not_after, init_db
from .env import load_home_env
from .ingest import add_candidate_record


class BrowserbaseUnavailable(RuntimeError):
    pass


def run_browserbase_scan(root: str | Path | None = None) -> list[dict[str, Any]]:
    root_path = project_root(root)
    ensure_layout(root_path)
    init_db(root_path)
    env_path = load_home_env()

    api_key = os.environ.get("BROWSERBASE_API_KEY")
    if not api_key:
        raise BrowserbaseUnavailable(
            f"BROWSERBASE_API_KEY is not set. Add it to {env_path} or export it "
            "before running: uv run velo-watch scan"
        )

    try:
        from browserbase import Browserbase
        from playwright.sync_api import sync_playwright
    except Exception as exc:
        raise BrowserbaseUnavailable(
            "Browserbase support is not installed. Run: uv sync"
        ) from exc

    watchlist = load_watchlist(root_path)
    searches = watchlist.get("searches", []) or []
    wait_ms = int(os.environ.get("VELO_SCAN_WAIT_MS", "6000"))
    detail_wait_ms = int(os.environ.get("VELO_DETAIL_WAIT_MS", "1000"))
    detail_timeout_ms = int(os.environ.get("VELO_DETAIL_TIMEOUT_MS", "12000"))
    max_listings = int(os.environ.get("VELO_MAX_LISTINGS_PER_SEARCH", "8"))
    posted_after = parse_cutoff_date(os.environ.get("VELO_POSTED_AFTER_DATE", "2026-05-04"))
    project_id = os.environ.get("BROWSERBASE_PROJECT_ID")
    proxy_country = os.environ.get("BROWSERBASE_PROXY_COUNTRY", "US")
    proxy_state = os.environ.get("BROWSERBASE_PROXY_STATE", "CA")
    proxy_city = os.environ.get("BROWSERBASE_PROXY_CITY", "San Francisco")
    use_proxy = os.environ.get("BROWSERBASE_USE_PROXY", "true").lower() not in {
        "0",
        "false",
        "no",
    }

    bb = Browserbase(api_key=api_key)
    session_args: dict[str, Any] = {
        "browser_settings": {
            "viewport": {"width": 1440, "height": 1800},
            "recordSession": True,
            "logSession": True,
            "solveCaptchas": False,
        },
        "user_metadata": {"task": "velo-watch-scan"},
    }
    if use_proxy:
        session_args["proxies"] = [
            {
                "type": "browserbase",
                "geolocation": {
                    "country": proxy_country,
                    "state": proxy_state,
                    "city": proxy_city,
                },
            }
        ]
    if project_id:
        session_args["project_id"] = project_id

    session = bb.sessions.create(**session_args)
    session_url = f"https://browserbase.com/sessions/{session.id}"
    results: list[dict[str, Any]] = []
    search_page_urls: list[str] = []

    playwright = sync_playwright().start()
    browser = None
    try:
        browser = playwright.chromium.connect_over_cdp(session.connect_url)
        browser_context = browser.contexts[0] if browser.contexts else browser.new_context()

        with TemporaryDirectory() as directory:
            tmp_dir = Path(directory)
            for search in searches:
                page = browser_context.new_page()
                name = str(search.get("name") or search.get("marketplace") or "marketplace")
                marketplace = str(search.get("marketplace") or "browserbase")
                url = str(search.get("url") or "")
                if not url:
                    page.close()
                    continue
                search_page_urls.append(url)
                print(f"Scanning {name}...", flush=True)

                try:
                    page.goto(url, wait_until="domcontentloaded", timeout=60_000)
                    page.wait_for_timeout(wait_ms)

                    body_text = visible_body_text(page)
                    screenshot = tmp_dir / f"{safe_slug(name)}.png"
                    page.screenshot(path=str(screenshot), full_page=True)
                    listings = extract_listing_candidates(
                        page,
                        marketplace=marketplace,
                        search_name=name,
                        search_url=url,
                        max_listings=max_listings,
                    )
                    print(f"  found {len(listings)} listing links", flush=True)

                    for listing_index, listing in enumerate(listings, start=1):
                        listing["listing_image_path"] = str(
                            screenshot_listing_card(
                                page,
                                listing.get("container_id"),
                                tmp_dir,
                                name,
                                listing_index,
                            )
                            or ""
                        )

                    for listing in listings:
                        if not listing.get("posted_at"):
                            enrich_listing_detail(
                                page,
                                listing,
                                wait_ms=detail_wait_ms,
                                timeout_ms=detail_timeout_ms,
                            )
                        posted_at = parse_posted_date(
                            "\n".join(
                                part
                                for part in [
                                    listing.get("posted_at") or "",
                                    listing.get("context") or "",
                                    listing.get("detail_text") or "",
                                ]
                                if part
                            )
                        )
                        if posted_at is None or posted_at <= posted_after:
                            print(
                                f"  skipped {listing.get('title') or listing.get('url')} "
                                f"(posted_at={posted_at})",
                                flush=True,
                            )
                            continue

                        context_text = "\n".join(
                            part
                            for part in [
                                listing.get("context") or "",
                                listing.get("image_alt") or "",
                                f"Posted at: {posted_at.isoformat()}",
                            ]
                            if part
                        ) or body_text[:1500]
                        listing_image = listing.get("listing_image_path") or None
                        row_id, created, candidate = add_candidate_record(
                            root_path,
                            source=marketplace,
                            url=listing["url"],
                            title=listing["title"],
                            price=listing["price"],
                            location="San Francisco / Bay Area",
                            posted_at=posted_at.isoformat(),
                            screenshot=screenshot,
                            listing_image=listing_image,
                            raw_text=context_text,
                            notes=(
                                f"Browserbase scan: {session_url}\n"
                                f"Search: {name}\n"
                                f"Search URL: {url}"
                            ),
                        )
                        results.append(
                            {
                                "id": row_id,
                                "created": created,
                                "source": marketplace,
                                "title": candidate.get("title"),
                                "score": candidate.get("score"),
                                "url": listing["url"],
                                "session_url": session_url,
                            }
                        )
                        print(
                            f"  kept candidate #{row_id}: {candidate.get('title')} "
                            f"posted_at={posted_at.isoformat()}",
                            flush=True,
                        )
                finally:
                    page.close()

        if results:
            delete_candidates_by_urls(root_path, search_page_urls)
        delete_scan_candidates_not_after(root_path, posted_after.isoformat())
    finally:
        if browser is not None:
            browser.close()
        playwright.stop()

    return results


def visible_body_text(page: Any) -> str:
    try:
        return page.locator("body").inner_text(timeout=5000)
    except Exception:
        return ""


def extract_listing_candidates(
    page: Any,
    *,
    marketplace: str,
    search_name: str,
    search_url: str,
    max_listings: int,
) -> list[dict[str, str | None]]:
    anchors = page.evaluate(
        """
        () => Array.from(document.querySelectorAll('a[href]')).map((anchor) => {
          const container = anchor.closest(
            'li, article, [role="listitem"], [data-testid], .result-row, .cl-static-search-result'
          ) || anchor.parentElement;
          const id = `velo-listing-${Math.random().toString(36).slice(2)}`;
          anchor.setAttribute('data-velo-anchor-id', id);
          if (container) container.setAttribute('data-velo-card-id', id);
          const image = (container || anchor).querySelector('img');
          const text = (anchor.innerText || anchor.textContent || anchor.getAttribute('aria-label') || '').trim();
          const context = (container && (container.innerText || container.textContent) || text || '').trim();
          return {
            href: anchor.href,
            text,
            context,
            containerId: id,
            imageSrc: image && (image.currentSrc || image.src || ''),
            imageAlt: image && (image.alt || '')
          };
        })
        """
    )

    listings: list[dict[str, str | None]] = []
    seen: set[str] = set()
    for anchor in anchors:
        url = normalize_listing_url(str(anchor.get("href") or ""))
        if not url or url in seen or not is_listing_url(url, marketplace):
            continue
        seen.add(url)
        context = clean_text(str(anchor.get("context") or ""))
        posted_at = parse_posted_date(context)
        title = title_from_anchor(str(anchor.get("text") or ""), context, search_name)
        listings.append(
            {
                "url": url,
                "title": title,
                "price": price_from_text(context),
                "context": context,
                "container_id": str(anchor.get("containerId") or ""),
                "image_src": str(anchor.get("imageSrc") or ""),
                "image_alt": str(anchor.get("imageAlt") or ""),
                "posted_at": posted_at.isoformat() if posted_at else None,
                "search_url": search_url,
            }
        )
        if len(listings) >= max_listings:
            break

    return listings


def screenshot_listing_card(
    page: Any,
    container_id: str | None,
    tmp_dir: Path,
    search_name: str,
    listing_index: int,
) -> Path | None:
    if not container_id:
        return None
    target = tmp_dir / f"{safe_slug(search_name)}-{listing_index:02d}-listing.png"
    try:
        locator = page.locator(f'[data-velo-card-id="{container_id}"]').first
        locator.screenshot(path=str(target), timeout=5000)
        return target
    except Exception:
        return None


def enrich_listing_detail(
    page: Any,
    listing: dict[str, str | None],
    *,
    wait_ms: int,
    timeout_ms: int,
) -> None:
    try:
        page.goto(str(listing["url"]), wait_until="domcontentloaded", timeout=timeout_ms)
        page.wait_for_timeout(wait_ms)
        detail_text = visible_body_text(page)
        listing["detail_text"] = clean_text(detail_text, 4000)
        if not listing.get("posted_at"):
            posted_at = parse_posted_date(detail_text)
            if posted_at:
                listing["posted_at"] = posted_at.isoformat()
    except Exception as exc:
        listing["detail_text"] = f"Listing detail load failed: {exc}"


def is_listing_url(url: str, marketplace: str) -> bool:
    parsed = urlparse(url)
    host = parsed.netloc.lower()
    path = parsed.path.lower()
    marketplace = marketplace.lower()

    if marketplace == "craigslist":
        return "craigslist." in host and path.endswith(".html") and "/search/" not in path
    if marketplace == "offerup":
        return "offerup." in host and (
            "/item/detail/" in path or "/item/" in path or "/listing/" in path
        )
    if marketplace == "facebook":
        return "facebook." in host and "/marketplace/item/" in path
    return False


def normalize_listing_url(url: str) -> str | None:
    if not url.startswith(("http://", "https://")):
        return None
    parsed = urlparse(url)
    keep_query = [
        (key, value)
        for key, value in parse_qsl(parsed.query, keep_blank_values=False)
        if key.lower() not in {"utm_source", "utm_medium", "utm_campaign", "utm_term", "utm_content"}
    ]
    return urlunparse(
        (
            parsed.scheme,
            parsed.netloc,
            parsed.path.rstrip("/") + ("/" if parsed.path.endswith("/") else ""),
            "",
            urlencode(keep_query),
            "",
        )
    )


def clean_text(value: str, limit: int = 1600) -> str:
    return re.sub(r"\s+", " ", value).strip()[:limit]


def title_from_anchor(text: str, context: str, fallback: str) -> str:
    cleaned = clean_text(text, 180)
    if len(cleaned) >= 4:
        return cleaned
    for line in re.split(r"[$\n|]", context):
        line = clean_text(line, 180)
        if len(line) >= 4:
            return line
    return fallback


def price_from_text(value: str) -> str | None:
    match = re.search(r"\$\s?[0-9][0-9,]{1,7}", value)
    return match.group(0).replace(" ", "") if match else None


MONTHS = {
    "jan": 1,
    "january": 1,
    "feb": 2,
    "february": 2,
    "mar": 3,
    "march": 3,
    "apr": 4,
    "april": 4,
    "may": 5,
    "jun": 6,
    "june": 6,
    "jul": 7,
    "july": 7,
    "aug": 8,
    "august": 8,
    "sep": 9,
    "sept": 9,
    "september": 9,
    "oct": 10,
    "october": 10,
    "nov": 11,
    "november": 11,
    "dec": 12,
    "december": 12,
}


def parse_cutoff_date(value: str) -> date:
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except ValueError as exc:
        raise ValueError("VELO_POSTED_AFTER_DATE must use YYYY-MM-DD") from exc


def parse_posted_date(value: str | None, today: date | None = None) -> date | None:
    if not value:
        return None
    today = today or date.today()
    text = clean_text(value, 5000).lower()

    if re.search(r"\b(today|just now|minutes? ago|hours? ago|an hour ago)\b", text):
        return today
    if "yesterday" in text:
        return today - timedelta(days=1)

    relative = re.search(r"\b(?:listed|posted)?\s*(\d+)\s*(day|week|month)s?\s+ago\b", text)
    if relative:
        amount = int(relative.group(1))
        unit = relative.group(2)
        days = amount
        if unit == "week":
            days = amount * 7
        elif unit == "month":
            days = amount * 30
        return today - timedelta(days=days)

    numeric = re.search(r"\b(\d{1,2})/(\d{1,2})(?:/(\d{2,4}))?\b", text)
    if numeric:
        month = int(numeric.group(1))
        day = int(numeric.group(2))
        year = normalize_year(numeric.group(3), today.year)
        return safe_date(year, month, day)

    month_names = "|".join(MONTHS)
    named = re.search(
        rf"\b({month_names})\.?\s+(\d{{1,2}})(?:st|nd|rd|th)?(?:,?\s+(\d{{4}}))?\b",
        text,
    )
    if named:
        month = MONTHS[named.group(1).rstrip(".")]
        day = int(named.group(2))
        year = int(named.group(3)) if named.group(3) else today.year
        parsed = safe_date(year, month, day)
        if parsed and parsed > today + timedelta(days=7):
            parsed = safe_date(year - 1, month, day)
        return parsed

    return None


def normalize_year(value: str | None, default: int) -> int:
    if not value:
        return default
    year = int(value)
    if year < 100:
        return 2000 + year
    return year


def safe_date(year: int, month: int, day: int) -> date | None:
    try:
        return date(year, month, day)
    except ValueError:
        return None


def safe_slug(value: str) -> str:
    slug = re.sub(r"[^A-Za-z0-9_.-]+", "-", value).strip("-").lower()
    return slug or "scan"
