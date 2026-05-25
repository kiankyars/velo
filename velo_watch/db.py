from __future__ import annotations

import hashlib
import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .config import data_dir, ensure_layout


SCHEMA = """
CREATE TABLE IF NOT EXISTS candidates (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  fingerprint TEXT NOT NULL UNIQUE,
  source TEXT NOT NULL DEFAULT 'manual',
  url TEXT,
  title TEXT,
  price TEXT,
  location TEXT,
  seller TEXT,
  posted_at TEXT,
  captured_at TEXT NOT NULL,
  screenshot_path TEXT,
  listing_image_path TEXT,
  raw_text TEXT,
  matched_bike TEXT,
  score REAL NOT NULL DEFAULT 0,
  score_reasons TEXT NOT NULL DEFAULT '[]',
  status TEXT NOT NULL DEFAULT 'new',
  notes TEXT NOT NULL DEFAULT '',
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_candidates_status_score
ON candidates(status, score DESC);
"""


def now_iso() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def db_path(root: str | Path | None = None) -> Path:
    return data_dir(root) / "candidates.sqlite"


def connect(root: str | Path | None = None) -> sqlite3.Connection:
    ensure_layout(root)
    conn = sqlite3.connect(db_path(root))
    conn.row_factory = sqlite3.Row
    return conn


def init_db(root: str | Path | None = None) -> None:
    with connect(root) as conn:
        conn.executescript(SCHEMA)
        ensure_column(conn, "candidates", "matched_bike", "TEXT")


def ensure_column(
    conn: sqlite3.Connection,
    table: str,
    column: str,
    definition: str,
) -> None:
    existing = {
        str(row["name"])
        for row in conn.execute(f"PRAGMA table_info({table})").fetchall()
    }
    if column not in existing:
        conn.execute(f"ALTER TABLE {table} ADD COLUMN {column} {definition}")


def candidate_fingerprint(candidate: dict[str, Any]) -> str:
    durable = candidate.get("url") or ""
    if not durable:
        durable = "\n".join(
            str(candidate.get(key) or "")
            for key in ("source", "title", "price", "location", "raw_text")
        )
    return hashlib.sha256(durable.encode("utf-8", errors="ignore")).hexdigest()


def add_or_update_candidate(
    root: str | Path | None, candidate: dict[str, Any]
) -> tuple[int, bool]:
    init_db(root)
    timestamp = now_iso()
    fingerprint = candidate.get("fingerprint") or candidate_fingerprint(candidate)
    candidate = {**candidate, "fingerprint": fingerprint}

    with connect(root) as conn:
        existing = conn.execute(
            "SELECT id FROM candidates WHERE fingerprint = ?", (fingerprint,)
        ).fetchone()
        if existing:
            fields = [
                "source",
                "url",
                "title",
                "price",
                "location",
                "seller",
                "posted_at",
                "screenshot_path",
                "listing_image_path",
                "raw_text",
                "matched_bike",
                "score",
                "score_reasons",
            ]
            updates = {key: candidate.get(key) for key in fields if candidate.get(key)}
            if "score_reasons" in updates:
                updates["score_reasons"] = json.dumps(updates["score_reasons"])
            updates["updated_at"] = timestamp
            if updates:
                assignments = ", ".join(f"{key} = ?" for key in updates)
                conn.execute(
                    f"UPDATE candidates SET {assignments} WHERE id = ?",
                    [*updates.values(), existing["id"]],
                )
            return int(existing["id"]), False

        conn.execute(
            """
            INSERT INTO candidates (
              fingerprint, source, url, title, price, location, seller, posted_at,
              captured_at, screenshot_path, listing_image_path, raw_text, score,
              matched_bike, score_reasons, status, notes, created_at, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                fingerprint,
                candidate.get("source") or "manual",
                candidate.get("url"),
                candidate.get("title"),
                candidate.get("price"),
                candidate.get("location"),
                candidate.get("seller"),
                candidate.get("posted_at"),
                candidate.get("captured_at") or timestamp,
                candidate.get("screenshot_path"),
                candidate.get("listing_image_path"),
                candidate.get("raw_text"),
                float(candidate.get("score") or 0),
                candidate.get("matched_bike"),
                json.dumps(candidate.get("score_reasons") or []),
                candidate.get("status") or "new",
                candidate.get("notes") or "",
                timestamp,
                timestamp,
            ),
        )
        row_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
        return int(row_id), True


def rows_to_dicts(rows: list[sqlite3.Row]) -> list[dict[str, Any]]:
    return [dict(row) for row in rows]


def list_candidates(
    root: str | Path | None = None,
    *,
    status: str | None = None,
    limit: int = 100,
) -> list[dict[str, Any]]:
    init_db(root)
    with connect(root) as conn:
        if status:
            rows = conn.execute(
                """
                SELECT * FROM candidates
                WHERE status = ?
                ORDER BY score DESC, updated_at DESC
                LIMIT ?
                """,
                (status, limit),
            ).fetchall()
        else:
            rows = conn.execute(
                """
                SELECT * FROM candidates
                ORDER BY score DESC, updated_at DESC
                LIMIT ?
                """,
                (limit,),
            ).fetchall()
    return rows_to_dicts(rows)


def get_candidate(root: str | Path | None, candidate_id: int) -> dict[str, Any] | None:
    init_db(root)
    with connect(root) as conn:
        row = conn.execute(
            "SELECT * FROM candidates WHERE id = ?", (candidate_id,)
        ).fetchone()
    return dict(row) if row else None


def update_candidate(
    root: str | Path | None,
    candidate_id: int,
    *,
    status: str | None = None,
    notes: str | None = None,
    score: float | None = None,
    score_reasons: list[str] | None = None,
) -> None:
    updates: dict[str, Any] = {"updated_at": now_iso()}
    if status is not None:
        updates["status"] = status
    if notes is not None:
        updates["notes"] = notes
    if score is not None:
        updates["score"] = float(score)
    if score_reasons is not None:
        updates["score_reasons"] = json.dumps(score_reasons)

    assignments = ", ".join(f"{key} = ?" for key in updates)
    with connect(root) as conn:
        conn.execute(
            f"UPDATE candidates SET {assignments} WHERE id = ?",
            [*updates.values(), candidate_id],
        )


def delete_candidate(root: str | Path | None, candidate_id: int) -> dict[str, Any] | None:
    candidate = get_candidate(root, candidate_id)
    if not candidate:
        return None
    with connect(root) as conn:
        conn.execute("DELETE FROM candidates WHERE id = ?", (candidate_id,))
    return candidate


def delete_candidates_by_urls(root: str | Path | None, urls: list[str]) -> int:
    if not urls:
        return 0
    init_db(root)
    placeholders = ", ".join("?" for _ in urls)
    with connect(root) as conn:
        cursor = conn.execute(
            f"DELETE FROM candidates WHERE url IN ({placeholders})",
            urls,
        )
        return int(cursor.rowcount or 0)


def delete_scan_candidates_not_after(root: str | Path | None, cutoff_date: str) -> int:
    init_db(root)
    with connect(root) as conn:
        cursor = conn.execute(
            """
            DELETE FROM candidates
            WHERE notes LIKE 'Browserbase scan:%'
              AND (
                posted_at IS NULL
                OR posted_at = ''
                OR substr(posted_at, 1, 10) <= ?
              )
            """,
            (cutoff_date,),
        )
        return int(cursor.rowcount or 0)


def iter_candidate_ids(root: str | Path | None = None) -> list[int]:
    init_db(root)
    with connect(root) as conn:
        rows = conn.execute("SELECT id FROM candidates ORDER BY id").fetchall()
    return [int(row["id"]) for row in rows]
