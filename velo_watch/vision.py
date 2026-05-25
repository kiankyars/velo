from __future__ import annotations

from pathlib import Path


def ocr_image(path: str | Path | None) -> tuple[str, str | None]:
    if not path:
        return "", None
    try:
        from PIL import Image
        import pytesseract
    except Exception:
        return "", "OCR unavailable: install Pillow, pytesseract, and tesseract."

    try:
        image = Image.open(path)
        return pytesseract.image_to_string(image), None
    except Exception as exc:  # pragma: no cover - depends on local OCR install
        return "", f"OCR failed: {exc}"


def average_hash(path: str | Path, hash_size: int = 8) -> int | None:
    try:
        from PIL import Image
    except Exception:
        return None

    try:
        image = Image.open(path).convert("L").resize((hash_size, hash_size))
    except Exception:
        return None

    pixels = list(image.getdata())
    avg = sum(pixels) / len(pixels)
    bits = 0
    for pixel in pixels:
        bits = (bits << 1) | int(pixel >= avg)
    return bits


def hamming_distance(left: int, right: int) -> int:
    return (left ^ right).bit_count()


def best_reference_similarity(
    listing_image: str | Path | None,
    reference_images: list[Path],
) -> tuple[float, Path | None]:
    if not listing_image or not reference_images:
        return 0.0, None

    listing_hash = average_hash(listing_image)
    if listing_hash is None:
        return 0.0, None

    best_score = 0.0
    best_path: Path | None = None
    max_distance = 64
    for reference_image in reference_images:
        reference_hash = average_hash(reference_image)
        if reference_hash is None:
            continue
        distance = hamming_distance(listing_hash, reference_hash)
        similarity = max(0.0, 1.0 - (distance / max_distance))
        if similarity > best_score:
            best_score = similarity
            best_path = reference_image

    return best_score, best_path
