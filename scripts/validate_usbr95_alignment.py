#!/usr/bin/env python3
"""
Compare the built route against the OFFICIAL US Bicycle Route 95.

Why this exists: the first version of this route was built purely with BRouter,
without first checking whether an official designated line existed. It does.
**USBR 95 is an AASHTO-designated national route running the length of
California, Crescent City to the Mexican border**, and it is exactly the
"official backbone" that ROUTE-GPX.md's own method says to start from - the same
way the Frankfurt loop uses the official EuroVelo GPX for EV15/17/7/6 and reserves
BRouter for connectors. Skipping that check was a process miss, and this script is
the fix: the official line is now a permanent reference the route is measured
against, not something to rediscover.

Source of the official geometry: the OSM route relations tagged
`route=bicycle, network=ncn, ref=95`. Adventure Cycling also publishes the USBRS
digital maps for free (advcy.link/causbr) if you want the authoritative file.

What it reports, per stage:
  * share of the built line lying within 100 / 250 / 500 / 1000 m of USBR 95
  * every divergence longer than `--min-km`, with location and length

A divergence is not automatically a defect. This route deliberately departs from
USBR 95 to start at the rider's front door, to split the days at Limekiln and
Refugio, and to finish at LA Union Station where the train home leaves from.
The point of the report is to make each departure visible and deliberate.

Usage:
    python3 scripts/validate_usbr95_alignment.py [--min-km 1.5] [--refetch]

Writes data/pch_usbr95_alignment.json. Overpass responses cache under
scripts/.cache, so re-runs are free.
"""
import os
import sys
import json
import math
import time
import argparse
import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from pch_waypoints import STAGES                                    # noqa: E402

BASE = os.path.dirname(HERE)
GPX_DIR = os.path.join(BASE, "gpx")
DATA_DIR = os.path.join(BASE, "data")
CACHE = os.path.join(HERE, ".cache", "usbr95")
NS = "{http://www.topografix.com/GPX/1/1}"

OVERPASS = [
    "https://maps.mail.ru/osm/tools/overpass/api/interpreter",
    "https://overpass-api.de/api/interpreter",
    "https://overpass.private.coffee/api/interpreter",
]
# California bbox, trimmed to the latitudes this route actually covers.
CA_BBOX = (32.4, -124.6, 38.4, -117.0)
GRID = 200          # ~500 m cells: int(deg * 200)
NO_MATCH_M = 2000.0  # reported when nothing is found in the 3x3 cell neighbourhood


def hav(a, b):
    R = 6371000.0
    p1, p2 = math.radians(a[0]), math.radians(b[0])
    dp = math.radians(b[0] - a[0])
    dl = math.radians(b[1] - a[1])
    h = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * R * math.asin(math.sqrt(h))


def overpass(query, cache_name):
    os.makedirs(CACHE, exist_ok=True)
    cf = os.path.join(CACHE, cache_name)
    if os.path.exists(cf) and os.path.getsize(cf) > 500:
        return json.load(open(cf))
    last = None
    for host in OVERPASS:
        try:
            data = urllib.parse.urlencode({"data": query}).encode()
            req = urllib.request.Request(
                host, data=data, headers={"User-Agent": "velo-planner/1.0"})
            with urllib.request.urlopen(req, timeout=240) as r:
                d = json.loads(r.read().decode())
            if "elements" not in d:
                raise ValueError("no elements")
            json.dump(d, open(cf, "w"))
            return d
        except Exception as e:                                      # noqa: BLE001
            last = e
            sys.stderr.write(f"  overpass {host.split('/')[2]}: {e}\n")
            time.sleep(3)
    raise RuntimeError(f"all overpass mirrors failed: {last}")


def fetch_usbr95(refetch=False):
    """Relation ids first, then each relation's way geometry separately.

    One combined query for the whole state times out; per-relation works.
    """
    if refetch:
        for f in os.listdir(CACHE) if os.path.isdir(CACHE) else []:
            os.remove(os.path.join(CACHE, f))
    s, w, n, e = CA_BBOX
    rels = overpass(
        f'[out:json][timeout:200];'
        f'relation["route"="bicycle"]["network"="ncn"]["ref"="95"]({s},{w},{n},{e});'
        f'out tags;', "relations.json")
    ids = [r["id"] for r in rels.get("elements", [])]
    proposed = {r["id"] for r in rels.get("elements", [])
                if (r.get("tags") or {}).get("state") == "proposed"}
    nodes, ways = [], 0
    for rid in ids:
        d = overpass(f'[out:json][timeout:200];rel(id:{rid});way(r);out geom;',
                     f"rel_{rid}.json")
        for el in d.get("elements", []):
            g = el.get("geometry") or []
            if not g:
                continue
            ways += 1
            for p in g:
                if p and p.get("lat") is not None:
                    nodes.append((p["lat"], p["lon"]))
    return ids, proposed, ways, nodes


def build_grid(nodes):
    grid = {}
    for la, lo in nodes:
        grid.setdefault((int(la * GRID), int(lo * GRID)), []).append((la, lo))
    return grid


def nearest(grid, p):
    k = (int(p[0] * GRID), int(p[1] * GRID))
    best = NO_MATCH_M
    for da in (-1, 0, 1):
        for db in (-1, 0, 1):
            for q in grid.get((k[0] + da, k[1] + db), ()):
                d = hav(p, q)
                if d < best:
                    best = d
    return best


def load_track(path):
    return [(float(x.attrib["lat"]), float(x.attrib["lon"]))
            for x in ET.parse(path).getroot().iter(NS + "trkpt")]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--min-km", type=float, default=1.5,
                    help="report divergences longer than this (km)")
    ap.add_argument("--refetch", action="store_true")
    args = ap.parse_args()

    print("Fetching official USBR 95 from OSM (route=bicycle, network=ncn, ref=95)...")
    ids, proposed, ways, nodes = fetch_usbr95(args.refetch)
    grid = build_grid(nodes)
    print(f"  {len(ids)} relations ({len(proposed)} marked state=proposed), "
          f"{ways} ways, {len(nodes):,} nodes\n")

    report = {
        "generated_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "reference": "OSM route=bicycle network=ncn ref=95 (US Bicycle Route 95, "
                     "AASHTO-designated: Crescent City to the Mexican border). "
                     "Adventure Cycling publishes the USBRS digital maps free at "
                     "advcy.link/causbr.",
        "relations": ids, "proposed_relations": sorted(proposed),
        "reference_nodes": len(nodes),
        "no_match_reported_as_m": NO_MATCH_M,
        "stages": [],
    }

    print(f"{'stage':30}{'pts':>6}{'<100m':>8}{'<250m':>8}{'<500m':>8}{'<1km':>7}"
          f"{'median':>8}")
    for stage in STAGES:
        path = os.path.join(GPX_DIR, stage["id"] + ".gpx")
        if not os.path.exists(path):
            continue
        t = load_track(path)
        ds = [nearest(grid, p) for p in t]
        km = [0.0]
        for i in range(len(t) - 1):
            km.append(km[-1] + hav(t[i], t[i + 1]) / 1000.0)
        n = len(ds)

        def frac(lim):
            return round(100.0 * sum(1 for d in ds if d < lim) / n, 1)

        med = sorted(ds)[n // 2]

        # contiguous runs further than 300 m from the official line
        runs, i = [], 0
        while i < len(ds):
            if ds[i] > 300:
                j = i
                while j < len(ds) and ds[j] > 300:
                    j += 1
                jj = min(j, len(km) - 1)
                if km[jj] - km[i] > args.min_km:
                    runs.append({
                        "from_km": round(km[i], 1), "to_km": round(km[jj], 1),
                        "length_km": round(km[jj] - km[i], 1),
                        "max_offset_m": (None if max(ds[i:j]) >= NO_MATCH_M
                                         else round(max(ds[i:j]))),
                        "beyond_search_radius": max(ds[i:j]) >= NO_MATCH_M,
                        "start": [round(t[i][0], 5), round(t[i][1], 5)],
                        "end": [round(t[jj][0], 5), round(t[jj][1], 5)],
                    })
                i = j
            else:
                i += 1
        runs.sort(key=lambda r: -r["length_km"])

        print(f"{stage['id'].replace('pch_',''):30}{n:>6}{frac(100):>7.1f}%"
              f"{frac(250):>7.1f}%{frac(500):>7.1f}%{frac(1000):>6.1f}%{med:>7.0f}m")
        report["stages"].append({
            "id": stage["id"], "points": n,
            "within_100m_pct": frac(100), "within_250m_pct": frac(250),
            "within_500m_pct": frac(500), "within_1000m_pct": frac(1000),
            "median_offset_m": round(med),
            "divergences_over_min_km": runs,
        })

    json.dump(report, open(os.path.join(DATA_DIR, "pch_usbr95_alignment.json"), "w"),
              indent=1)
    print(f"\nDivergences longer than {args.min_km} km:")
    for s in report["stages"]:
        if not s["divergences_over_min_km"]:
            continue
        print(f"  {s['id'].replace('pch_','')}:")
        for r in s["divergences_over_min_km"][:6]:
            off = ("beyond 2 km" if r["beyond_search_radius"]
                   else f"max {r['max_offset_m']} m")
            print(f"     km {r['from_km']:6.1f} -> {r['to_km']:6.1f}  "
                  f"({r['length_km']:5.1f} km, {off})")
    print(f"\nwrote {os.path.join(DATA_DIR, 'pch_usbr95_alignment.json')}")
    print("\nNOTE: a divergence is not a defect. This route departs from USBR 95 on "
          "purpose to\nstart at the rider's door, split the days at Limekiln and "
          "Refugio, and finish at LA\nUnion Station. The report exists to keep every "
          "departure visible and deliberate.")


if __name__ == "__main__":
    main()
