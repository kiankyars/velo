#!/usr/bin/env python3
"""Validate that EV15 follows the official Rhine-side EuroVelo corridor."""

import argparse
import math
import os
import tempfile
import urllib.request
import xml.etree.ElementTree as ET


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOCAL_EV15 = os.path.join(BASE_DIR, "gpx", "ev15_rhine.gpx")
OFFICIAL_EV15_STAGE_URL = "https://en.eurovelo.com/route/get-gpx/227?developed=1"

CHECKPOINTS = {
    "Mainz": ((50.005355648, 8.273509573), 900, "near"),
    "Oppenheim": ((49.8540, 8.3597), 500, "near"),
    "Worms": ((49.6341, 8.3507), 2000, "near"),
    "Speyer": ((49.3173, 8.4412), 500, "near"),
    "Germersheim": ((49.2232, 8.3660), 500, "near"),
    "Karlsruhe-Maxau": ((49.0375, 8.3014), 500, "near"),
    "Andermatt": ((46.6340499, 8.5948148), 50, "near"),
    "Osthofen": ((49.7039, 8.3283), 1500, "away"),
}


def haversine_m(a, b):
    radius_m = 6371000.0
    phi1 = math.radians(a[0])
    phi2 = math.radians(b[0])
    dphi = math.radians(b[0] - a[0])
    dlambda = math.radians(b[1] - a[1])
    h = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    return 2 * radius_m * math.asin(math.sqrt(h))


def read_trackpoints(path):
    root = ET.parse(path).getroot()
    ns = "{http://www.topografix.com/GPX/1/1}" if root.tag.startswith("{") else ""
    return [
        (float(point.attrib["lat"]), float(point.attrib["lon"]))
        for point in root.findall(f".//{ns}trkpt")
    ]


def nearest_distance_m(track, latlon):
    return min(haversine_m(point, latlon) for point in track)


def nearest_index(track, latlon):
    return min(range(len(track)), key=lambda i: haversine_m(track[i], latlon))


def validate_local():
    if not os.path.exists(LOCAL_EV15):
        raise SystemExit(f"Missing EV15 GPX: {LOCAL_EV15}")

    track = read_trackpoints(LOCAL_EV15)
    if len(track) < 10000:
        raise SystemExit(f"EV15 GPX has too few points: {len(track)}")

    failures = []
    print(f"EV15 local GPX: {len(track)} points")
    for name, (latlon, threshold_m, mode) in CHECKPOINTS.items():
        distance_m = nearest_distance_m(track, latlon)
        print(f"{name}: {distance_m:.0f} m")
        if mode == "near" and distance_m > threshold_m:
            failures.append(f"{name} is {distance_m:.0f} m away; expected <= {threshold_m} m")
        if mode == "away" and distance_m < threshold_m:
            failures.append(f"{name} is {distance_m:.0f} m away; expected >= {threshold_m} m")

    if failures:
        raise SystemExit("Route alignment failed:\n- " + "\n- ".join(failures))
    return track


def validate_against_official(local_track):
    with tempfile.NamedTemporaryFile(suffix=".gpx") as handle:
        request = urllib.request.Request(
            OFFICIAL_EV15_STAGE_URL,
            headers={"User-Agent": "velo-route-validator/1.0"},
        )
        with urllib.request.urlopen(request, timeout=60) as response:
            handle.write(response.read())
        handle.flush()
        official_stage = read_trackpoints(handle.name)

    mainz = (50.005355648, 8.273509573)
    maxau = (49.0375, 8.3014)
    i_mainz = nearest_index(official_stage, mainz)
    i_maxau = nearest_index(official_stage, maxau)
    lo, hi = sorted((i_mainz, i_maxau))
    official_slice = official_stage[lo : hi + 1]

    max_nearest_m = max(nearest_distance_m(local_track, point) for point in official_slice)
    print(f"Official EV15 Mainz-Maxau comparison: max nearest-point drift {max_nearest_m:.2f} m")
    if max_nearest_m > 3:
        raise SystemExit("Local EV15 GPX no longer matches the official EuroVelo Mainz-Maxau line")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--compare-official",
        action="store_true",
        help="Download the official EuroVelo stage GPX and compare Mainz-Maxau.",
    )
    args = parser.parse_args()

    local_track = validate_local()
    if args.compare_official:
        validate_against_official(local_track)
    print("Route alignment ok")


if __name__ == "__main__":
    main()
