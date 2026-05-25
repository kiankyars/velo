from __future__ import annotations

import json
import shutil
from datetime import datetime
from pathlib import Path

from .config import exports_dir, load_bike_profiles, project_root, reference_photo_paths
from .db import get_candidate


def copy_if_present(root: Path, value: str | None, target_dir: Path) -> str | None:
    if not value:
        return None
    source = (root / value).resolve() if not Path(value).is_absolute() else Path(value)
    if not source.exists():
        return None
    target = target_dir / source.name
    shutil.copy2(source, target)
    return target.name


def export_evidence(root: str | Path | None, candidate_id: int) -> Path:
    root_path = project_root(root)
    candidate = get_candidate(root_path, candidate_id)
    if not candidate:
        raise ValueError(f"No candidate with id {candidate_id}")

    profile = matched_profile(root_path, candidate)
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    export_dir = exports_dir(root_path) / f"candidate-{candidate_id}-{timestamp}"
    export_dir.mkdir(parents=True, exist_ok=True)

    screenshot_name = copy_if_present(root_path, candidate.get("screenshot_path"), export_dir)
    listing_image_name = copy_if_present(
        root_path, candidate.get("listing_image_path"), export_dir
    )
    reference_names = []
    for reference in reference_photo_paths(root_path, profile):
        target = export_dir / reference.name
        shutil.copy2(reference, target)
        reference_names.append(target.name)

    reasons = json.loads(candidate.get("score_reasons") or "[]")
    summary = evidence_markdown(
        candidate,
        profile,
        reasons,
        screenshot_name,
        listing_image_name,
        reference_names,
    )
    (export_dir / "summary.md").write_text(summary, encoding="utf-8")
    return export_dir


def evidence_markdown(
    candidate: dict,
    profile: dict,
    reasons: list[str],
    screenshot_name: str | None,
    listing_image_name: str | None,
    reference_names: list[str],
) -> str:
    lines = [
        f"# Candidate {candidate['id']} Evidence Packet",
        "",
        "## Candidate",
        f"- Source: {candidate.get('source') or ''}",
        f"- URL: {candidate.get('url') or ''}",
        f"- Title: {candidate.get('title') or ''}",
        f"- Price: {candidate.get('price') or ''}",
        f"- Location: {candidate.get('location') or ''}",
        f"- Seller: {candidate.get('seller') or ''}",
        f"- Captured at: {candidate.get('captured_at') or ''}",
        f"- Score: {candidate.get('score') or 0}",
        f"- Matched bike: {candidate.get('matched_bike') or ''}",
        f"- Status: {candidate.get('status') or ''}",
        "",
        "## Match Reasons",
    ]
    lines.extend(f"- {reason}" for reason in reasons)
    lines.extend(
        [
            "",
            "## Bike Profile",
            f"- Name: {profile.get('name') or ''}",
            f"- Make: {profile.get('make') or ''}",
            f"- Model: {profile.get('model') or ''}",
            f"- Serial: {profile.get('serial') or ''}",
            f"- Color: {profile.get('color') or ''}",
            f"- Size: {profile.get('size') or ''}",
            f"- Theft date: {profile.get('theft_date') or ''}",
            f"- Theft location: {profile.get('theft_location') or ''}",
            f"- Project 529: {profile.get('project529_url') or ''}",
            f"- Bike Index: {profile.get('bike_index_url') or ''}",
            f"- Police report: {profile.get('police_report_number') or ''}",
            "",
            "## Files",
            f"- Candidate screenshot: {screenshot_name or ''}",
            f"- Listing image crop: {listing_image_name or ''}",
        ]
    )
    lines.extend(f"- Reference photo: {name}" for name in reference_names)
    lines.extend(
        [
            "",
            "## Notes",
            candidate.get("notes") or "",
            "",
            "## Extracted Text",
            "```",
            candidate.get("raw_text") or "",
            "```",
            "",
        ]
    )
    return "\n".join(lines)


def matched_profile(root: Path, candidate: dict) -> dict:
    profiles = load_bike_profiles(root)
    matched_bike = candidate.get("matched_bike")
    for profile in profiles:
        name = profile.get("name") or profile.get("model") or profile.get("make")
        if matched_bike and name == matched_bike:
            return profile
    return profiles[0] if profiles else {}
