from __future__ import annotations

import re
import shutil
from datetime import datetime
from email import policy
from email.parser import BytesParser
from pathlib import Path
from typing import Any

from .config import captures_dir, project_root, resolve_project_path
from .db import add_or_update_candidate, now_iso
from .matching import score_candidate_for_all_profiles
from .vision import ocr_image


URL_RE = re.compile(r"https?://[^\s<>\")]+")


def stage_file(root: str | Path, source: str | Path | None, label: str) -> str | None:
    if not source:
        return None
    source_path = resolve_project_path(root, str(source))
    if not source_path or not source_path.exists():
        raise FileNotFoundError(f"No such file: {source}")

    target_dir = captures_dir(root)
    target_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    safe_label = re.sub(r"[^A-Za-z0-9_.-]+", "-", label).strip("-") or "candidate"
    target = target_dir / f"{timestamp}-{safe_label}{source_path.suffix.lower()}"
    if source_path.resolve() != target.resolve():
        shutil.copy2(source_path, target)
    return str(target.relative_to(project_root(root)))


def infer_source(url: str | None, fallback: str | None = None) -> str:
    url = (url or "").lower()
    if "craigslist." in url:
        return "craigslist"
    if "offerup." in url:
        return "offerup"
    if "facebook." in url:
        return "facebook"
    return fallback or "manual"


def guess_title(raw_text: str | None) -> str | None:
    if not raw_text:
        return None
    for line in raw_text.splitlines():
        line = line.strip()
        if len(line) >= 8 and not line.startswith("http"):
            return line[:160]
    return None


def add_candidate_record(
    root: str | Path | None,
    *,
    source: str | None = None,
    url: str | None = None,
    title: str | None = None,
    price: str | None = None,
    location: str | None = None,
    seller: str | None = None,
    posted_at: str | None = None,
    screenshot: str | Path | None = None,
    listing_image: str | Path | None = None,
    raw_text: str | None = None,
    notes: str | None = None,
) -> tuple[int, bool, dict[str, Any]]:
    root_path = project_root(root)
    staged_screenshot = stage_file(root_path, screenshot, source or "screenshot")
    staged_listing_image = stage_file(root_path, listing_image, source or "listing-image")

    ocr_text = ""
    ocr_warning = None
    if staged_screenshot:
        ocr_text, ocr_warning = ocr_image(root_path / staged_screenshot)

    combined_text = "\n".join(part for part in [raw_text, ocr_text] if part)
    candidate = {
        "source": source or infer_source(url),
        "url": url,
        "title": title or guess_title(combined_text),
        "price": price,
        "location": location,
        "seller": seller,
        "posted_at": posted_at,
        "captured_at": now_iso(),
        "screenshot_path": staged_screenshot,
        "listing_image_path": staged_listing_image,
        "raw_text": combined_text,
        "notes": notes or "",
    }

    score, reasons, matched_bike = score_candidate_for_all_profiles(root_path, candidate)
    if ocr_warning:
        reasons.append(ocr_warning)
    candidate["score"] = score
    candidate["score_reasons"] = reasons
    candidate["matched_bike"] = matched_bike

    row_id, created = add_or_update_candidate(root_path, candidate)
    return row_id, created, candidate


def email_text(path: str | Path) -> tuple[str, str]:
    with Path(path).open("rb") as handle:
        message = BytesParser(policy=policy.default).parse(handle)

    subject = message.get("subject", "")
    parts: list[str] = []
    if message.is_multipart():
        for part in message.walk():
            content_type = part.get_content_type()
            if content_type == "text/plain":
                payload = part.get_content()
                if isinstance(payload, str):
                    parts.append(payload)
    else:
        payload = message.get_content()
        if isinstance(payload, str):
            parts.append(payload)

    return subject, "\n".join(parts)


def marketplace_urls(text: str) -> list[str]:
    urls = []
    for url in URL_RE.findall(text):
        lowered = url.lower()
        if any(host in lowered for host in ("craigslist.", "offerup.", "facebook.")):
            urls.append(url.rstrip(".,;"))
    return sorted(set(urls))


def ingest_email_path(root: str | Path | None, path: str | Path) -> list[int]:
    path = Path(path).expanduser()
    paths = sorted(path.rglob("*.eml")) if path.is_dir() else [path]
    added: list[int] = []

    for email_path in paths:
        subject, body = email_text(email_path)
        urls = marketplace_urls(body)
        raw_text = f"{subject}\n\n{body}"
        if not urls:
            row_id, _, _ = add_candidate_record(
                root,
                source="email",
                title=subject,
                raw_text=raw_text,
                notes=f"Imported from {email_path}",
            )
            added.append(row_id)
            continue

        for url in urls:
            row_id, _, _ = add_candidate_record(
                root,
                source=infer_source(url, "email"),
                url=url,
                title=subject,
                raw_text=raw_text,
                notes=f"Imported from {email_path}",
            )
            added.append(row_id)

    return added
