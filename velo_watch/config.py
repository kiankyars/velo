from __future__ import annotations

import json
from pathlib import Path
from typing import Any


DEFAULT_BIKE_PROFILE = """name: "Stolen Cannondale"
make: "Cannondale"
model: ""
serial: ""
color: ""
size: ""
theft_date: ""
theft_location: "San Francisco, CA"
project529_url: "https://project529.com/garage/bikes/pannier-crank-aero-helmet/"
bike_index_url: ""
police_report_number: ""
low_price_threshold: 1200
reference_photos:
  - "bike.jpg"
  - "vélo.jpg"
distinctive_terms:
  - "cannondale"
  - "pannier"
  - "crank"
  - "aero"
  - "helmet"
components:
"""

DEFAULT_WATCHLIST = """cadence: "twice_daily"
searches:
  - name: "OfferUp Cannondale"
    marketplace: "offerup"
    url: "https://offerup.com/search?q=cannondale"
  - name: "Craigslist SFBay Cannondale"
    marketplace: "craigslist"
    url: "https://sfbay.craigslist.org/search/bia?query=cannondale#search=2~gallery~0"
  - name: "Facebook Marketplace SF Cannondale"
    marketplace: "facebook"
    url: "https://www.facebook.com/marketplace/sanfrancisco/search/?query=cannondale"
  - name: "OfferUp Trek Fuel EX 7"
    marketplace: "offerup"
    url: "https://offerup.com/search?q=trek%20fuel%20ex%207"
  - name: "Craigslist SFBay Trek Fuel EX 7"
    marketplace: "craigslist"
    url: "https://sfbay.craigslist.org/search/bia?query=trek%20fuel%20ex%207#search=2~gallery~0"
  - name: "Facebook Marketplace SF Trek Fuel EX 7"
    marketplace: "facebook"
    url: "https://www.facebook.com/marketplace/sanfrancisco/search/?query=trek%20fuel%20ex%207"
"""


def project_root(root: str | Path | None = None) -> Path:
    return Path(root or Path.cwd()).resolve()


def config_dir(root: str | Path | None = None) -> Path:
    return project_root(root) / "config"


def data_dir(root: str | Path | None = None) -> Path:
    return project_root(root) / "data"


def captures_dir(root: str | Path | None = None) -> Path:
    return project_root(root) / "captures"


def exports_dir(root: str | Path | None = None) -> Path:
    return project_root(root) / "exports"


def ensure_layout(root: str | Path | None = None) -> None:
    root_path = project_root(root)
    config_dir(root_path).mkdir(parents=True, exist_ok=True)
    data_dir(root_path).mkdir(parents=True, exist_ok=True)
    captures_dir(root_path).mkdir(parents=True, exist_ok=True)
    exports_dir(root_path).mkdir(parents=True, exist_ok=True)

    profile_path = config_dir(root_path) / "bike_profile.yml"
    if not profile_path.exists():
        profile_path.write_text(DEFAULT_BIKE_PROFILE, encoding="utf-8")

    watchlist_path = config_dir(root_path) / "watchlist.yml"
    if not watchlist_path.exists():
        watchlist_path.write_text(DEFAULT_WATCHLIST, encoding="utf-8")


def load_bike_profile(root: str | Path | None = None) -> dict[str, Any]:
    profiles = load_bike_profiles(root)
    if profiles:
        return profiles[0]
    return normalize_profile({})


def load_bike_profiles(root: str | Path | None = None) -> list[dict[str, Any]]:
    bikes_path = config_dir(root) / "bikes.json"
    if bikes_path.exists():
        payload = json.loads(bikes_path.read_text(encoding="utf-8"))
        profiles = payload.get("bikes", [])
        return [normalize_profile(dict(profile)) for profile in profiles]

    return [load_yaml_bike_profile(root)]


def load_yaml_bike_profile(root: str | Path | None = None) -> dict[str, Any]:
    path = config_dir(root) / "bike_profile.yml"
    profile = load_simple_yaml(path)
    return normalize_profile(profile)


def normalize_profile(profile: dict[str, Any]) -> dict[str, Any]:
    profile.setdefault("reference_photos", [])
    profile.setdefault("distinctive_terms", [])
    profile.setdefault("components", [])
    profile.setdefault("low_price_threshold", 1200)
    for key in ("reference_photos", "distinctive_terms", "components"):
        profile[key] = coerce_list(profile.get(key))
    return profile


def coerce_list(value: Any) -> list[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    if isinstance(value, str):
        return [part.strip() for part in value.split(",") if part.strip()]
    return [value]


def load_watchlist(root: str | Path | None = None) -> dict[str, Any]:
    path = config_dir(root) / "watchlist.yml"
    watchlist = load_simple_yaml(path)
    watchlist.setdefault("cadence", "twice_daily")
    watchlist.setdefault("searches", [])
    return watchlist


def load_simple_yaml(path: str | Path) -> dict[str, Any]:
    """Parse the small YAML subset used by this project.

    This is not a general YAML parser. It supports top-level scalar values,
    top-level lists of scalars, and top-level lists of simple mappings.
    """

    result: dict[str, Any] = {}
    current_key: str | None = None
    current_item: dict[str, Any] | None = None

    for raw_line in Path(path).read_text(encoding="utf-8").splitlines():
        if not raw_line.strip() or raw_line.lstrip().startswith("#"):
            continue

        indent = len(raw_line) - len(raw_line.lstrip(" "))
        stripped = raw_line.strip()

        if indent == 0 and ":" in stripped and not stripped.startswith("- "):
            key, value = stripped.split(":", 1)
            key = key.strip()
            value = value.strip()
            if value:
                result[key] = parse_scalar(value)
                current_key = None
                current_item = None
            else:
                result[key] = []
                current_key = key
                current_item = None
            continue

        if current_key is None:
            continue

        if stripped.startswith("- "):
            item = stripped[2:].strip()
            if ":" in item:
                key, value = item.split(":", 1)
                current_item = {key.strip(): parse_scalar(value.strip())}
                result[current_key].append(current_item)
            else:
                current_item = None
                result[current_key].append(parse_scalar(item))
            continue

        if current_item is not None and ":" in stripped:
            key, value = stripped.split(":", 1)
            current_item[key.strip()] = parse_scalar(value.strip())

    return result


def parse_scalar(value: str) -> Any:
    value = value.strip()
    if value == "":
        return ""
    if value in {"[]", "null", "Null", "NULL"}:
        return [] if value == "[]" else None
    if value in {"true", "True"}:
        return True
    if value in {"false", "False"}:
        return False
    if (value.startswith('"') and value.endswith('"')) or (
        value.startswith("'") and value.endswith("'")
    ):
        return value[1:-1]
    try:
        return int(value)
    except ValueError:
        pass
    try:
        return float(value)
    except ValueError:
        return value


def resolve_project_path(root: str | Path, value: str | None) -> Path | None:
    if not value:
        return None
    path = Path(value).expanduser()
    if path.is_absolute():
        return path
    return project_root(root) / path


def reference_photo_paths(root: str | Path, profile: dict[str, Any]) -> list[Path]:
    paths: list[Path] = []
    for value in profile.get("reference_photos", []) or []:
        path = resolve_project_path(root, str(value))
        if path and path.exists():
            paths.append(path)
    return paths
