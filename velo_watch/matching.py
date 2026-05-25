from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from .config import load_bike_profiles, reference_photo_paths
from .vision import best_reference_similarity


LOCAL_TERMS = [
    "san francisco",
    "sf",
    "sfbay",
    "oakland",
    "berkeley",
    "daly city",
    "south san francisco",
    "san mateo",
    "marin",
    "sacramento",
    "stockton",
    "modesto",
    "santa cruz",
]


def normalize_text(value: str | None) -> str:
    return re.sub(r"\s+", " ", (value or "").lower()).strip()


def candidate_text(candidate: dict[str, Any]) -> str:
    return normalize_text(
        "\n".join(
            str(candidate.get(key) or "")
            for key in (
                "source",
                "url",
                "title",
                "price",
                "location",
                "seller",
                "raw_text",
            )
        )
    )


def profile_terms(profile: dict[str, Any]) -> list[tuple[str, str, float]]:
    terms: list[tuple[str, str, float]] = []
    weighted_fields = [
        ("make", 25),
        ("model", 20),
        ("color", 10),
        ("size", 6),
        ("serial", 100),
    ]
    for field, weight in weighted_fields:
        value = normalize_text(str(profile.get(field) or ""))
        if len(value) >= 2 and value not in {"unspecified", "unknown", "n/a"}:
            terms.append((field, value, weight))

    for term in profile.get("distinctive_terms", []) or []:
        normalized = normalize_text(str(term))
        if len(normalized) >= 3:
            terms.append(("distinctive", normalized, 5))

    for term in profile.get("components", []) or []:
        normalized = normalize_text(str(term))
        if len(normalized) >= 3:
            terms.append(("component", normalized, 8))

    return terms


def parse_price(value: str | None) -> int | None:
    if not value:
        return None
    match = re.search(r"\$?\s*([0-9][0-9,]{1,7})", value)
    if not match:
        return None
    try:
        return int(match.group(1).replace(",", ""))
    except ValueError:
        return None


def score_candidate(
    root: str | Path,
    candidate: dict[str, Any],
    profile: dict[str, Any],
) -> tuple[float, list[str]]:
    text = candidate_text(candidate)
    score = 0.0
    reasons: list[str] = []
    seen_terms: set[str] = set()

    for label, term, weight in profile_terms(profile):
        if term in seen_terms:
            continue
        if term and term in text:
            score += weight
            seen_terms.add(term)
            reasons.append(f"{label} match: {term} (+{weight:g})")

    if any(term in text for term in LOCAL_TERMS):
        score += 8
        reasons.append("Bay Area / nearby location signal (+8)")

    price = parse_price(str(candidate.get("price") or "") or text)
    threshold = int(profile.get("low_price_threshold") or 0)
    if price is not None and threshold and price <= threshold:
        score += 8
        reasons.append(f"price at or below ${threshold:,}: ${price:,} (+8)")

    listing_image = candidate.get("listing_image_path") or candidate.get("screenshot_path")
    references = reference_photo_paths(root, profile)
    similarity, reference = best_reference_similarity(listing_image, references)
    if similarity >= 0.75:
        score += 35
        reasons.append(
            f"strong image-hash similarity to {reference.name if reference else 'reference'} "
            f"({similarity:.2f}, +35)"
        )
    elif similarity >= 0.60:
        score += 15
        reasons.append(
            f"moderate image-hash similarity to {reference.name if reference else 'reference'} "
            f"({similarity:.2f}, +15)"
        )

    if not reasons:
        reasons.append("no configured profile terms matched")

    return round(score, 2), reasons


def score_candidate_for_profiles(
    root: str | Path,
    candidate: dict[str, Any],
    profiles: list[dict[str, Any]],
) -> tuple[float, list[str], str]:
    if not profiles:
        score, reasons = score_candidate(root, candidate, {})
        return score, reasons, ""

    best_score = -1.0
    best_reasons: list[str] = []
    best_name = ""
    profile_scores: list[tuple[str, float]] = []
    for profile in profiles:
        score, reasons = score_candidate(root, candidate, profile)
        name = str(profile.get("name") or profile.get("model") or profile.get("make") or "bike")
        profile_scores.append((name, score))
        if score > best_score:
            best_score = score
            best_reasons = reasons
            best_name = name

    profile_scores.sort(key=lambda item: item[1], reverse=True)
    reasons = [f"matched bike profile: {best_name}"] + best_reasons
    if len(profile_scores) > 1:
        score_line = ", ".join(f"{name}: {score:g}" for name, score in profile_scores)
        reasons.append(f"profile scores: {score_line}")
    return round(best_score, 2), reasons, best_name


def score_candidate_for_all_profiles(
    root: str | Path,
    candidate: dict[str, Any],
) -> tuple[float, list[str], str]:
    return score_candidate_for_profiles(root, candidate, load_bike_profiles(root))
