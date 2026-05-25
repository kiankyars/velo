from __future__ import annotations

import html
import json
import mimetypes
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlencode, urlparse

from .config import load_bike_profiles, load_watchlist, project_root
from .db import get_candidate, list_candidates, update_candidate
from .evidence import export_evidence
from .ingest import add_candidate_record


STATUSES = ["new", "monitor", "possible_match", "likely_match", "rejected"]


def esc(value: object) -> str:
    return html.escape("" if value is None else str(value))


def page(title: str, body: str) -> bytes:
    return f"""<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{esc(title)}</title>
  <style>
    :root {{ color-scheme: light dark; }}
    body {{ font: 14px/1.45 -apple-system, BlinkMacSystemFont, sans-serif; margin: 0; }}
    header {{ padding: 16px 24px; border-bottom: 1px solid #ccc; display: flex; gap: 16px; align-items: center; }}
    main {{ padding: 20px 24px 40px; }}
    a {{ color: #0b64c0; }}
    table {{ width: 100%; border-collapse: collapse; }}
    th, td {{ padding: 8px; border-bottom: 1px solid #ddd; text-align: left; vertical-align: top; }}
    input, textarea, select {{ box-sizing: border-box; width: 100%; padding: 7px; font: inherit; }}
    textarea {{ min-height: 90px; }}
    button {{ padding: 7px 10px; font: inherit; cursor: pointer; }}
    .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(230px, 1fr)); gap: 12px; }}
    .field {{ margin-bottom: 10px; }}
    .score {{ font-weight: 700; }}
    .muted {{ color: #666; }}
    .thumb {{ max-width: 360px; max-height: 260px; border: 1px solid #ddd; }}
    .mini-thumb {{ width: 72px; height: 72px; object-fit: cover; border: 1px solid #ddd; }}
    .reasons li {{ margin-bottom: 4px; }}
  </style>
</head>
<body>
  <header>
    <strong>Velo Recovery Watch</strong>
    <a href="/">Candidates</a>
    <a href="/add">Add Candidate</a>
    <a href="/watchlist">Watchlist</a>
  </header>
  <main>{body}</main>
</body>
</html>
""".encode("utf-8")


class DashboardHandler(BaseHTTPRequestHandler):
    root: Path

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        if parsed.path == "/":
            self.respond(self.index(parsed.query))
        elif parsed.path == "/candidate":
            self.respond(self.candidate_detail(parsed.query))
        elif parsed.path == "/add":
            self.respond(self.add_form())
        elif parsed.path == "/watchlist":
            self.respond(self.watchlist_page())
        elif parsed.path == "/export":
            self.respond(self.export_page(parsed.query))
        elif parsed.path == "/file":
            self.serve_file(parsed.query)
        else:
            self.send_error(404)

    def do_HEAD(self) -> None:
        parsed = urlparse(self.path)
        if parsed.path in {"/", "/candidate", "/add", "/watchlist", "/export"}:
            self.send_response(200)
            self.send_header("content-type", "text/html; charset=utf-8")
            self.end_headers()
        else:
            self.send_error(404)

    def do_POST(self) -> None:
        parsed = urlparse(self.path)
        length = int(self.headers.get("content-length", "0"))
        payload = self.rfile.read(length).decode("utf-8")
        form = {key: values[0] for key, values in parse_qs(payload).items()}
        if parsed.path == "/candidate/update":
            candidate_id = int(form["id"])
            update_candidate(
                self.root,
                candidate_id,
                status=form.get("status"),
                notes=form.get("notes"),
            )
            self.redirect(f"/candidate?id={candidate_id}")
        elif parsed.path == "/add":
            row_id, _, _ = add_candidate_record(
                self.root,
                source=form.get("source") or None,
                url=form.get("url") or None,
                title=form.get("title") or None,
                price=form.get("price") or None,
                location=form.get("location") or None,
                seller=form.get("seller") or None,
                posted_at=form.get("posted_at") or None,
                screenshot=form.get("screenshot_path") or None,
                listing_image=form.get("listing_image_path") or None,
                raw_text=form.get("raw_text") or None,
                notes=form.get("notes") or None,
            )
            self.redirect(f"/candidate?id={row_id}")
        else:
            self.send_error(404)

    def log_message(self, format: str, *args: object) -> None:
        return

    def respond(self, payload: bytes, status: int = 200) -> None:
        self.send_response(status)
        self.send_header("content-type", "text/html; charset=utf-8")
        self.send_header("content-length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def redirect(self, target: str) -> None:
        self.send_response(303)
        self.send_header("location", target)
        self.end_headers()

    def index(self, query: str) -> bytes:
        params = parse_qs(query)
        status = params.get("status", [None])[0] or None
        rows = list_candidates(self.root, status=status, limit=250)
        status_links = " ".join(
            f'<a href="/?{urlencode({"status": value})}">{esc(value)}</a>'
            for value in STATUSES
        )
        body_rows = []
        for row in rows:
            title = esc(row.get("title") or row.get("url") or "untitled")
            url = row.get("url") or ""
            title_link = (
                f'<a href="{esc(url)}">{title}</a>'
                if url
                else title
            )
            thumb = thumbnail_tag(row.get("listing_image_path"))
            body_rows.append(
                "<tr>"
                f'<td><a href="/candidate?id={row["id"]}">#{row["id"]}</a></td>'
                f"<td>{thumb}</td>"
                f"<td>{esc(row.get('source'))}</td>"
                f"<td class=\"score\">{esc(row.get('score'))}</td>"
                f"<td>{esc(row.get('matched_bike'))}</td>"
                f"<td>{esc(row.get('status'))}</td>"
                f"<td>{title_link}</td>"
                f"<td>{esc(row.get('price'))}</td>"
                f"<td>{esc(row.get('location'))}</td>"
                f"<td>{esc(row.get('updated_at'))}</td>"
                "</tr>"
            )
        body = f"""
<h1>Candidates</h1>
<p class="muted">Filter: <a href="/">all</a> {status_links}</p>
<table>
  <thead>
    <tr><th>ID</th><th>Image</th><th>Source</th><th>Score</th><th>Bike</th><th>Status</th><th>Title / URL</th><th>Price</th><th>Location</th><th>Updated</th></tr>
  </thead>
  <tbody>{''.join(body_rows) or '<tr><td colspan="10">No candidates yet.</td></tr>'}</tbody>
</table>
"""
        return page("Candidates", body)

    def candidate_detail(self, query: str) -> bytes:
        params = parse_qs(query)
        candidate_id = int(params.get("id", ["0"])[0])
        candidate = get_candidate(self.root, candidate_id)
        if not candidate:
            return page("Not found", "<h1>Candidate not found</h1>")
        reasons = json.loads(candidate.get("score_reasons") or "[]")
        screenshot = image_tag(candidate.get("screenshot_path"), "Screenshot")
        listing_image = image_tag(candidate.get("listing_image_path"), "Listing image")
        status_options = "".join(
            f'<option value="{esc(status)}" {"selected" if candidate.get("status") == status else ""}>{esc(status)}</option>'
            for status in STATUSES
        )
        body = f"""
<h1>Candidate #{candidate_id}</h1>
<p><a href="{esc(candidate.get('url'))}">{esc(candidate.get('url'))}</a></p>
<div class="grid">
  <div>
    <p><strong>Source:</strong> {esc(candidate.get('source'))}</p>
    <p><strong>Title:</strong> {esc(candidate.get('title'))}</p>
    <p><strong>Price:</strong> {esc(candidate.get('price'))}</p>
    <p><strong>Location:</strong> {esc(candidate.get('location'))}</p>
    <p><strong>Seller:</strong> {esc(candidate.get('seller'))}</p>
    <p><strong>Score:</strong> <span class="score">{esc(candidate.get('score'))}</span></p>
    <p><strong>Matched bike:</strong> {esc(candidate.get('matched_bike'))}</p>
    <p><a href="/export?id={candidate_id}">Export evidence packet</a></p>
  </div>
  <div>{screenshot}{listing_image}</div>
</div>
<h2>Match Reasons</h2>
<ul class="reasons">{''.join(f'<li>{esc(reason)}</li>' for reason in reasons)}</ul>
<h2>Review</h2>
<form method="post" action="/candidate/update">
  <input type="hidden" name="id" value="{candidate_id}">
  <div class="field"><label>Status<select name="status">{status_options}</select></label></div>
  <div class="field"><label>Notes<textarea name="notes">{esc(candidate.get('notes'))}</textarea></label></div>
  <button type="submit">Save</button>
</form>
<h2>Extracted Text</h2>
<pre>{esc(candidate.get('raw_text'))}</pre>
"""
        return page(f"Candidate {candidate_id}", body)

    def add_form(self) -> bytes:
        body = """
<h1>Add Candidate</h1>
<form method="post" action="/add">
  <div class="grid">
    <div class="field"><label>Source<input name="source" placeholder="craigslist / offerup / facebook"></label></div>
    <div class="field"><label>URL<input name="url"></label></div>
    <div class="field"><label>Title<input name="title"></label></div>
    <div class="field"><label>Price<input name="price"></label></div>
    <div class="field"><label>Location<input name="location"></label></div>
    <div class="field"><label>Seller<input name="seller"></label></div>
    <div class="field"><label>Posted at<input name="posted_at"></label></div>
    <div class="field"><label>Screenshot path<input name="screenshot_path" placeholder="/path/to/screenshot.png"></label></div>
    <div class="field"><label>Listing image crop path<input name="listing_image_path" placeholder="/path/to/crop.jpg"></label></div>
  </div>
  <div class="field"><label>Raw text<textarea name="raw_text"></textarea></label></div>
  <div class="field"><label>Notes<textarea name="notes"></textarea></label></div>
  <button type="submit">Add</button>
</form>
"""
        return page("Add Candidate", body)

    def watchlist_page(self) -> bytes:
        profiles = load_bike_profiles(self.root)
        watchlist = load_watchlist(self.root)
        rows = []
        for search in watchlist.get("searches", []) or []:
            url = search.get("url") or ""
            rows.append(
                "<tr>"
                f"<td>{esc(search.get('name'))}</td>"
                f"<td>{esc(search.get('marketplace'))}</td>"
                f'<td><a href="{esc(url)}">{esc(url)}</a></td>'
                "</tr>"
            )
        body = f"""
<h1>Watchlist</h1>
<p><strong>Cadence:</strong> {esc(watchlist.get('cadence'))}</p>
<table><thead><tr><th>Name</th><th>Marketplace</th><th>URL</th></tr></thead><tbody>{''.join(rows)}</tbody></table>
<h2>Bike Profiles</h2>
{''.join(profile_summary(profile) for profile in profiles)}
"""
        return page("Watchlist", body)

    def export_page(self, query: str) -> bytes:
        params = parse_qs(query)
        candidate_id = int(params.get("id", ["0"])[0])
        path = export_evidence(self.root, candidate_id)
        return page(
            "Evidence exported",
            f"<h1>Evidence exported</h1><p>{esc(path)}</p><p><a href=\"/candidate?id={candidate_id}\">Back</a></p>",
        )

    def serve_file(self, query: str) -> None:
        params = parse_qs(query)
        relative = params.get("path", [""])[0]
        if not relative or Path(relative).is_absolute():
            self.send_error(400)
            return

        target = (self.root / relative).resolve()
        try:
            target.relative_to(self.root.resolve())
        except ValueError:
            self.send_error(403)
            return

        if not target.exists() or not target.is_file():
            self.send_error(404)
            return

        content_type = mimetypes.guess_type(target.name)[0] or "application/octet-stream"
        payload = target.read_bytes()
        self.send_response(200)
        self.send_header("content-type", content_type)
        self.send_header("content-length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)


def image_tag(path: str | None, label: str) -> str:
    if not path:
        return ""
    url = "/file?" + urlencode({"path": path})
    return (
        f"<figure><img class=\"thumb\" src=\"{esc(url)}\" alt=\"{esc(label)}\">"
        f"<figcaption>{esc(label)}: {esc(path)}</figcaption></figure>"
    )


def thumbnail_tag(path: str | None) -> str:
    if not path:
        return ""
    url = "/file?" + urlencode({"path": path})
    return f'<img class="mini-thumb" src="{esc(url)}" alt="Listing image">'


def profile_summary(profile: dict) -> str:
    project529 = profile.get("project529_url") or ""
    project529_link = ""
    if project529:
        project529_link = (
            f' - Project 529: <a href="{esc(project529)}">{esc(project529)}</a>'
        )
    return (
        "<p>"
        f"<strong>{esc(profile.get('name'))}</strong>: "
        f"{esc(profile.get('make'))} {esc(profile.get('model'))} "
        f"{esc(profile.get('color'))} {esc(profile.get('size'))}"
        f"{project529_link}"
        "</p>"
    )


def run_server(root: str | Path | None = None, host: str = "127.0.0.1", port: int = 8765) -> None:
    root_path = project_root(root)
    handler = type("BoundDashboardHandler", (DashboardHandler,), {"root": root_path})
    server = ThreadingHTTPServer((host, port), handler)
    print(f"Serving Velo Recovery Watch at http://{host}:{port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped Velo Recovery Watch")
    finally:
        server.server_close()
