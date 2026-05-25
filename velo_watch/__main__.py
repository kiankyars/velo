from __future__ import annotations

import argparse
import shutil
from pathlib import Path

from .browser_helper import write_review_sheet
from .browserbase_scan import BrowserbaseUnavailable, run_browserbase_scan
from .config import ensure_layout, project_root
from .dashboard import run_server
from .db import (
    delete_candidate,
    init_db,
    list_candidates,
)
from .evidence import export_evidence
from .ingest import add_candidate_record, ingest_email_path


IMAGE_SUFFIXES = {".jpg", ".jpeg", ".png", ".webp", ".heic"}
TEXT_SUFFIXES = {".txt", ".md", ".html", ".htm"}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="velo-watch")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("init", help="Initialize the local workspace.")
    subparsers.add_parser("scan", help="Run the Browserbase marketplace scan.")

    add = subparsers.add_parser("add", help="Add a URL, screenshot, text file, or .eml file.")
    add.add_argument("input")

    subparsers.add_parser("list", help="List candidates.")

    export = subparsers.add_parser("export", help="Export an evidence packet.")
    export.add_argument("candidate_id", type=int)

    delete = subparsers.add_parser("delete", help="Delete a candidate and its local files.")
    delete.add_argument("candidate_id", type=int)

    subparsers.add_parser("serve", help="Run the local dashboard.")

    args = parser.parse_args(argv)
    root = project_root(".")

    if args.command == "init":
        ensure_layout(root)
        init_db(root)
        review_sheet = write_review_sheet(root)
        print(f"Initialized Velo Recovery Watch in {root}")
        print(f"Review sheet: {review_sheet}")
        return 0

    if args.command == "scan":
        try:
            results = run_browserbase_scan(root)
        except BrowserbaseUnavailable as exc:
            print(str(exc))
            return 2
        for result in results:
            action = "created" if result["created"] else "updated"
            print(
                f"{action} candidate #{result['id']} "
                f"score={result['score']} source={result['source']}"
            )
        if results:
            print(f"Browserbase session: {results[0]['session_url']}")
        return 0

    if args.command == "add":
        created_ids = add_input(root, args.input)
        print(f"Added/updated {len(created_ids)} candidate record(s): {', '.join(map(str, created_ids))}")
        return 0

    if args.command == "list":
        rows = list_candidates(root, limit=100)
        for row in rows:
            title = row.get("title") or row.get("url") or "untitled"
            print(
                f"#{row['id']} score={row['score']} status={row['status']} "
                f"bike={row.get('matched_bike') or ''} source={row['source']} title={title}"
            )
        return 0

    if args.command == "delete":
        candidate = delete_candidate(root, args.candidate_id)
        if not candidate:
            raise SystemExit(f"No candidate with id {args.candidate_id}")
        removed_files = []
        for key in ("screenshot_path", "listing_image_path"):
            removed_files.extend(remove_project_file(root, candidate.get(key)))
        export_root = root / "exports"
        for export_path in export_root.glob(f"candidate-{args.candidate_id}-*"):
            if export_path.is_dir():
                shutil.rmtree(export_path)
                removed_files.append(str(export_path.relative_to(root)))
        print(f"Deleted candidate #{args.candidate_id}")
        for path in removed_files:
            print(f"- removed {path}")
        return 0

    if args.command == "export":
        path = export_evidence(root, args.candidate_id)
        print(path)
        return 0

    if args.command == "serve":
        ensure_layout(root)
        init_db(root)
        run_server(root, "127.0.0.1", 8765)
        return 0

    return 1


def add_input(root: Path, value: str) -> list[int]:
    if looks_like_url(value):
        row_id, _, _ = add_candidate_record(root, url=value)
        return [row_id]

    path = Path(value).expanduser()
    if not path.exists():
        row_id, _, _ = add_candidate_record(root, raw_text=value)
        return [row_id]

    suffix = path.suffix.lower()
    if path.is_dir() or suffix == ".eml":
        return ingest_email_path(root, path)
    if suffix in IMAGE_SUFFIXES:
        row_id, _, _ = add_candidate_record(root, screenshot=path)
        return [row_id]
    if suffix in TEXT_SUFFIXES:
        row_id, _, _ = add_candidate_record(
            root,
            raw_text=path.read_text(encoding="utf-8", errors="replace"),
            notes=f"Imported from {path}",
        )
        return [row_id]

    row_id, _, _ = add_candidate_record(root, raw_text=str(path), notes="Unrecognized input")
    return [row_id]


def looks_like_url(value: str) -> bool:
    return value.startswith("http://") or value.startswith("https://")


def remove_project_file(root: Path, value: str | None) -> list[str]:
    if not value:
        return []
    path = (root / value).resolve()
    try:
        path.relative_to(root.resolve())
    except ValueError:
        return []
    if path.exists() and path.is_file():
        path.unlink()
        return [str(path.relative_to(root))]
    return []


if __name__ == "__main__":
    raise SystemExit(main())
