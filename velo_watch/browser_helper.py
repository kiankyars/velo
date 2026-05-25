from __future__ import annotations

import html
import webbrowser
from pathlib import Path

from .config import data_dir, load_watchlist, project_root


def print_watchlist(root: str | Path | None = None) -> None:
    watchlist = load_watchlist(root)
    for search in watchlist.get("searches", []) or []:
        print(f"{search.get('name')} [{search.get('marketplace')}]\n  {search.get('url')}")


def open_watchlist(root: str | Path | None = None) -> None:
    watchlist = load_watchlist(root)
    for search in watchlist.get("searches", []) or []:
        url = search.get("url")
        if url:
            webbrowser.open(url)


def write_review_sheet(root: str | Path | None = None) -> Path:
    root_path = project_root(root)
    watchlist = load_watchlist(root_path)
    rows = []
    for search in watchlist.get("searches", []) or []:
        url = search.get("url") or ""
        rows.append(
            "<tr>"
            f"<td>{html.escape(search.get('name') or '')}</td>"
            f"<td>{html.escape(search.get('marketplace') or '')}</td>"
            f'<td><a href="{html.escape(url)}">{html.escape(url)}</a></td>'
            "</tr>"
        )

    body = f"""<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <title>Velo Review Sheet</title>
  <style>
    body {{ font: 15px/1.45 -apple-system, BlinkMacSystemFont, sans-serif; margin: 32px; }}
    table {{ border-collapse: collapse; width: 100%; }}
    td, th {{ border-bottom: 1px solid #ddd; padding: 10px; text-align: left; }}
    code {{ background: #f4f4f4; padding: 2px 4px; border-radius: 3px; }}
  </style>
</head>
<body>
  <h1>Velo Review Sheet</h1>
  <p>Open each saved search, capture suspicious listings, then add them with
  <code>uv run velo-watch add</code> or the local dashboard.</p>
  <table>
    <thead><tr><th>Name</th><th>Marketplace</th><th>URL</th></tr></thead>
    <tbody>{''.join(rows)}</tbody>
  </table>
</body>
</html>
"""
    target = data_dir(root_path) / "review_sheet.html"
    target.write_text(body, encoding="utf-8")
    return target
