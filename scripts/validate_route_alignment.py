#!/usr/bin/env python3
"""Validate that the EuroVelo backbone legs follow the official EuroVelo GPX.

EV15/EV17/EV7/EV6 are assembled from the official eurovelo.com GPX (BRouter is
used only for the connectors that are not part of any signed EuroVelo route).
This script checks:

  * EV15 passes the Rhine-side checkpoints and stays away from the inland
    Osthofen short-cut that the original generated route took.
  * with --compare-official: every official-backbone leg stays within a few
    metres of the official EuroVelo line on the stretch it is meant to follow
    (EV15 is additionally compared against the official Mainz-Maxau stage).
"""

import argparse
import math
import os
import re
import urllib.request
import xml.etree.ElementTree as ET


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GPX_DIR = os.path.join(BASE_DIR, "gpx")
CACHE = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".cache")
NS = "{http://www.topografix.com/GPX/1/1}"

LOCAL_EV15 = os.path.join(GPX_DIR, "ev15_rhine.gpx")
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

# Official-backbone overlap checks: local gpx, eurovelo route gpx url, the track
# numbers the build follows, and the max tolerated nearest-point drift (metres).
OFFICIAL_OVERLAP = {
    "ev17_rhone": ("https://en.eurovelo.com/route/get-gpx/37",
                   [1, 2, 3, 4, 5, 8, 9, 10, 11] + list(range(12, 33)), 60),
    "ev7_central": ("https://en.eurovelo.com/route/get-gpx/30", [95, 96, 97, 98], 60),
    "ev6_danube": ("https://en.eurovelo.com/route/get-gpx/29", [79, 80, 81, 82, 83], 60),
}


def haversine_m(a, b):
    radius_m = 6371000.0
    phi1, phi2 = math.radians(a[0]), math.radians(b[0])
    dphi = math.radians(b[0] - a[0])
    dlambda = math.radians(b[1] - a[1])
    h = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    return 2 * radius_m * math.asin(math.sqrt(h))


def read_trackpoints(path, track_numbers=None):
    root = ET.parse(path).getroot()
    ns = NS if root.tag.startswith("{") else ""
    wanted = set(track_numbers) if track_numbers else None
    pts = []
    for idx, trk in enumerate(root.findall(f"{ns}trk"), start=1):
        if wanted and idx not in wanted:
            continue
        pts.extend((float(p.attrib["lat"]), float(p.attrib["lon"]))
                   for p in trk.iter(f"{ns}trkpt"))
    return pts


class Grid:
    """Coarse spatial index for fast nearest-point lookups."""

    def __init__(self, pts, cell=0.01):
        self.cell = cell
        self.g = {}
        for p in pts:
            self.g.setdefault((int(p[0] / cell), int(p[1] / cell)), []).append(p)

    def nearest_m(self, p):
        c = self.cell
        k = (int(p[0] / c), int(p[1] / c))
        best = float("inf")
        for dx in (-2, -1, 0, 1, 2):
            for dy in (-2, -1, 0, 1, 2):
                for q in self.g.get((k[0] + dx, k[1] + dy), ()):
                    best = min(best, haversine_m(p, q))
        if best == float("inf"):   # far from any point: fall back to a global scan
            for cell_pts in self.g.values():
                for q in cell_pts:
                    best = min(best, haversine_m(p, q))
        return best


def fetch_official(url):
    """Prefer the build cache, else download the official GPX into the cache."""
    m = re.search(r"get-gpx/(\d+)", url)
    rid = {"36": "ev15", "37": "ev17", "30": "ev7", "29": "ev6"}.get(m.group(1) if m else "")
    if rid:
        cached = os.path.join(CACHE, f"official_{rid}.gpx")
        if os.path.exists(cached):
            return cached
    os.makedirs(CACHE, exist_ok=True)
    dest = os.path.join(CACHE, f"official_stage_{m.group(1) if m else 'x'}.gpx")
    req = urllib.request.Request(url, headers={"User-Agent": "velo-route-validator/1.0"})
    with urllib.request.urlopen(req, timeout=90) as response:
        open(dest, "wb").write(response.read())
    return dest


def validate_ev15_checkpoints():
    if not os.path.exists(LOCAL_EV15):
        raise SystemExit(f"Missing EV15 GPX: {LOCAL_EV15}")
    track = read_trackpoints(LOCAL_EV15)
    if len(track) < 10000:
        raise SystemExit(f"EV15 GPX has too few points: {len(track)}")
    grid = Grid(track)
    failures = []
    print(f"EV15 local GPX: {len(track)} points")
    for name, (latlon, threshold_m, mode) in CHECKPOINTS.items():
        distance_m = grid.nearest_m(latlon)
        print(f"  {name}: {distance_m:.0f} m")
        if mode == "near" and distance_m > threshold_m:
            failures.append(f"{name} is {distance_m:.0f} m away; expected <= {threshold_m} m")
        if mode == "away" and distance_m < threshold_m:
            failures.append(f"{name} is {distance_m:.0f} m away; expected >= {threshold_m} m")
    if failures:
        raise SystemExit("EV15 checkpoint alignment failed:\n- " + "\n- ".join(failures))


def validate_ev15_stage():
    stage = read_trackpoints(fetch_official(OFFICIAL_EV15_STAGE_URL))
    local = Grid(read_trackpoints(LOCAL_EV15))
    mainz, maxau = (50.005355648, 8.273509573), (49.0375, 8.3014)
    i_mainz = min(range(len(stage)), key=lambda i: haversine_m(stage[i], mainz))
    i_maxau = min(range(len(stage)), key=lambda i: haversine_m(stage[i], maxau))
    lo, hi = sorted((i_mainz, i_maxau))
    drift = max(local.nearest_m(p) for p in stage[lo:hi + 1])
    print(f"EV15 official Mainz-Maxau stage: max drift {drift:.2f} m")
    if drift > 3:
        raise SystemExit("EV15 no longer matches the official Mainz-Maxau line")


def validate_overlap(seg_id, url, tracks, tol_m):
    local_path = os.path.join(GPX_DIR, seg_id + ".gpx")
    official = read_trackpoints(fetch_official(url), tracks)
    grid = Grid(read_trackpoints(local_path))
    drifts = sorted(grid.nearest_m(p) for p in official)
    worst = drifts[-1]
    p95 = drifts[int(len(drifts) * 0.95)]
    print(f"{seg_id}: official overlap {len(official)} pts -> max drift {worst:.0f} m (p95 {p95:.0f} m)")
    if worst > tol_m:
        raise SystemExit(f"{seg_id} drifts {worst:.0f} m from the official EuroVelo line (> {tol_m} m)")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--compare-official", action="store_true",
                        help="Download the official EuroVelo GPX and compare every backbone leg.")
    args = parser.parse_args()

    validate_ev15_checkpoints()
    if args.compare_official:
        validate_ev15_stage()
        for seg_id, (url, tracks, tol) in OFFICIAL_OVERLAP.items():
            validate_overlap(seg_id, url, tracks, tol)
    print("Route alignment ok")


if __name__ == "__main__":
    main()
