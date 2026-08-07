#!/usr/bin/env python3
"""
Build the waypoint layer for the San Francisco -> Los Angeles coast route.

Two sources, deliberately kept apart:

  * OpenStreetMap, via Overpass - the objective stuff whose coordinates should
    not come out of anyone's memory: drinking water taps, bike shops,
    campgrounds, shops, toilets, fuel. Queried with `around` against the routed
    line itself, so everything returned is genuinely beside the road, then
    annotated with its distance along the route.
  * scripts/pch_pois.py - the curated points that need a sentence: where you
    sleep, where the road is dangerous or legally awkward, where you can quit.

Also computes the thing that actually matters on this route: the longest stretch
with no water and no shop, and where it starts.

Outputs
  gpx/pch_waypoints.gpx        - every POI, for loading alongside the tracks
  gpx/pch_day*_annotated.gpx   - each riding day's track WITH its own waypoints
  data/pch_pois.json           - the merged, distance-annotated POI table

Usage: python3 scripts/harvest_pch_pois.py [--no-network]
  --no-network reuses data/pch_pois.json's OSM half instead of re-querying.
"""
import os
import sys
import json
import math
import time
import hashlib
import urllib.request
import urllib.parse

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from pch_waypoints import STAGES                                    # noqa: E402
from pch_pois import POIS                                           # noqa: E402
from build_pch_route import (brouter, write_gpx, cumdist, simplify,  # noqa: E402
                             GPX_DIR, DATA_DIR, CACHE, CHUNK)
from build_routes import analyze_brouter, haversine                 # noqa: E402
from pch_waypoints import PERMISSIVE_LEGS                           # noqa: E402

# The main Overpass instance times out constantly; these two answer.
OVERPASS = [
    "https://maps.mail.ru/osm/tools/overpass/api/interpreter",
    "https://overpass-api.de/api/interpreter",
    "https://overpass.private.coffee/api/interpreter",
]

# What to harvest, and how close to the route it has to be to matter.
# (label, overpass filter, radius in metres, GPX sym, category)
HARVEST = [
    ("drinking water", '["amenity"="drinking_water"]',   350, "Drinking Water",     "water"),
    ("bike shop",      '["shop"="bicycle"]',            1200, "Mine",               "bikeshop"),
    ("campground",     '["tourism"="camp_site"]',       1500, "Campground",         "camp"),
    ("supermarket",    '["shop"="supermarket"]',         600, "Shopping Center",    "food"),
    ("convenience",    '["shop"="convenience"]',         400, "Convenience Store",  "food"),
    ("fuel+shop",      '["amenity"="fuel"]',             400, "Gas Station",        "food"),
    ("toilets",        '["amenity"="toilets"]',          250, "Restroom",           "toilet"),
    ("drinking fountain", '["amenity"="fountain"]["drinking_water"="yes"]', 350,
                                                              "Drinking Water",     "water"),
]

SAMPLE_M = 1000.0      # spacing of the `around` polyline sent to Overpass


def build_stage_track(pts, nogos=()):
    """Re-route a stage (from cache) and return its track.

    nogos must match what build_pch_route.py used for the same stage, or the
    harvested POI distances would be measured against a different line.
    """
    runs, cur = [], [pts[0]]
    for i in range(len(pts) - 1):
        if (pts[i][0], pts[i + 1][0]) in PERMISSIVE_LEGS:
            if len(cur) > 1:
                runs.append((cur, False))
            runs.append(([pts[i], pts[i + 1]], True))
            cur = [pts[i + 1]]
        else:
            cur.append(pts[i + 1])
    if len(cur) > 1:
        runs.append((cur, False))
    track = []
    for run_pts, is_bridge in runs:
        step = 1 if is_bridge else CHUNK
        i = 0
        while i < len(run_pts) - 1:
            chunk = run_pts[i:i + step + 1]
            a = analyze_brouter(brouter([(la, lo) for _, la, lo in chunk],
                                        bridge=is_bridge, nogos=nogos))
            seg = a["track"]
            if track and haversine((track[-1][0], track[-1][1]),
                                   (seg[0][0], seg[0][1])) < 60:
                seg = seg[1:]
            track += seg
            i += step
    return track


def sample_along(track, spacing_m=SAMPLE_M):
    """Points every ~spacing_m along the track, for the Overpass `around` clause."""
    out = [track[0]]
    acc = 0.0
    for i in range(len(track) - 1):
        acc += haversine((track[i][0], track[i][1]), (track[i + 1][0], track[i + 1][1]))
        if acc >= spacing_m:
            out.append(track[i + 1])
            acc = 0.0
    if out[-1] is not track[-1]:
        out.append(track[-1])
    return out


def overpass(query):
    key = hashlib.md5(query.encode()).hexdigest()
    cf = os.path.join(CACHE, f"overpass_{key}.json")
    if os.path.exists(cf):
        return json.load(open(cf))
    last = None
    for host in OVERPASS:
        for attempt in range(2):
            try:
                data = urllib.parse.urlencode({"data": query}).encode()
                req = urllib.request.Request(
                    host, data=data,
                    headers={"User-Agent": "velo-planner/1.0 (bike route planning)"})
                with urllib.request.urlopen(req, timeout=240) as r:
                    d = json.loads(r.read().decode())
                if "elements" not in d:
                    raise ValueError("no elements in response")
                json.dump(d, open(cf, "w"))
                return d
            except Exception as e:                                  # noqa: BLE001
                last = e
                sys.stderr.write(f"  overpass {host.split('/')[2]} retry {attempt}: {e}\n")
                time.sleep(4 * (attempt + 1))
    raise RuntimeError(f"all overpass mirrors failed: {last}")


def harvest(track, label, filt, radius, sym, cat, dropped=None):
    """Harvest one category. A category that cannot be fetched is RECORDED as
    dropped and skipped, rather than killing a 25-minute run - but it is never
    dropped silently, because a missing category looks identical to "there is no
    water on this stretch", which is exactly the wrong thing to believe."""
    poly = sample_along(track)
    around = ",".join(f"{p[0]:.5f},{p[1]:.5f}" for p in poly)
    q = (f'[out:json][timeout:240];'
         f'nwr{filt}(around:{radius},{around});'
         f'out center tags;')
    try:
        d = overpass(q)
    except RuntimeError as e:                                    # noqa: BLE001
        print(f"    {label:18s} DROPPED - Overpass unavailable ({e})")
        if dropped is not None:
            dropped.append({"category": label, "radius_m": radius, "error": str(e)})
        return []
    found = []
    for e in d.get("elements", []):
        c = e.get("center") or {"lat": e.get("lat"), "lon": e.get("lon")}
        if c.get("lat") is None:
            continue
        t = e.get("tags", {})
        found.append({
            "osm": f"{e['type']}/{e['id']}",
            "name": t.get("name") or t.get("operator") or f"({label})",
            "lat": float(c["lat"]), "lon": float(c["lon"]),
            "cat": cat, "sym": sym, "kind": label,
            "tags": {k: v for k, v in t.items() if k in (
                "name", "operator", "opening_hours", "phone", "website",
                "drinking_water", "fee", "access", "seasonal", "toilets",
                "shower", "reservation", "description")},
        })
    print(f"    {label:18s} radius {radius:5d} m -> {len(found):4d}")
    return found


def annotate(pois, track, km):
    """Attach distance-along-route and offset-from-route to each POI."""
    out = []
    for p in pois:
        best, best_d = 0, float("inf")
        for j in range(len(track)):
            d = haversine((track[j][0], track[j][1]), (p["lat"], p["lon"]))
            if d < best_d:
                best_d, best = d, j
        q = dict(p)
        q["km"] = round(km[best], 1)
        q["offset_m"] = round(best_d)
        q["ele_m"] = round(track[best][2]) if track[best][2] is not None else None
        out.append(q)
    return out


def dedupe(pois, tol_m=60.0):
    """Drop OSM duplicates that sit on top of each other with the same category."""
    kept = []
    for p in sorted(pois, key=lambda x: (x["cat"], x["km"])):
        dup = False
        for q in kept:
            if q["cat"] == p["cat"] and abs(q["km"] - p["km"]) < 0.4 and \
                    haversine((q["lat"], q["lon"]), (p["lat"], p["lon"])) < tol_m:
                dup = True
                break
        if not dup:
            kept.append(p)
    return kept


def resupply_gaps(pois, stage_km):
    """Longest run with no water and no food, per stage.

    Only counts POIs actually beside the road (<=400 m off) - a supermarket
    2 km inland is not resupply when you are chasing daylight.
    """
    pts = sorted([p["km"] for p in pois
                  if p["cat"] in ("water", "food") and p["offset_m"] <= 400])
    marks = [0.0] + pts + [stage_km]
    worst, worst_at = 0.0, 0.0
    for i in range(len(marks) - 1):
        g = marks[i + 1] - marks[i]
        if g > worst:
            worst, worst_at = g, marks[i]
    return round(worst, 1), round(worst_at, 1), len(pts)


def main():
    no_net = "--no-network" in sys.argv
    cached = {}
    if no_net and os.path.exists(os.path.join(DATA_DIR, "pch_pois.json")):
        cached = json.load(open(os.path.join(DATA_DIR, "pch_pois.json")))

    all_rows = []
    per_stage = {}
    for stage in STAGES:
        print(f"\n{stage['id']}:", flush=True)
        track = build_stage_track(stage["pts"], nogos=stage.get("nogos", ()))
        km = cumdist(track)
        stage_km = km[-1]

        osm_rows = []
        dropped = []
        if no_net:
            osm_rows = [r for r in cached.get("pois", [])
                        if r.get("stage") == stage["id"] and r.get("osm")]
            print(f"    reusing {len(osm_rows)} cached OSM rows")
        else:
            for label, filt, radius, sym, cat in HARVEST:
                osm_rows += harvest(track, label, filt, radius, sym, cat, dropped)

        osm_rows = annotate(osm_rows, track, km)
        osm_rows = [r for r in osm_rows if r["offset_m"] <= 1600]
        osm_rows = dedupe(osm_rows)

        # curated POIs belonging to this stage: those that land on it
        cur_rows = annotate([dict(p) for p in POIS], track, km)
        cur_rows = [r for r in cur_rows if r["offset_m"] <= 2500]

        for r in osm_rows + cur_rows:
            r["stage"] = stage["id"]
        gap_km, gap_at, n_supply = resupply_gaps(osm_rows + cur_rows, stage_km)
        per_stage[stage["id"]] = {
            "distance_km": round(stage_km, 1),
            "osm_pois": len(osm_rows), "curated_pois": len(cur_rows),
            "resupply_points_on_road": n_supply,
            "longest_no_water_no_food_km": gap_km,
            "that_gap_starts_at_km": gap_at,
            "dropped_categories": dropped,
        }
        if dropped:
            print(f"    WARNING: {len(dropped)} category/categories dropped for "
                  f"{stage['id']}: {[d['category'] for d in dropped]}")
        print(f"    {len(osm_rows)} OSM + {len(cur_rows)} curated; "
              f"longest gap with no water/food: {gap_km} km from km {gap_at}")

        # annotated per-day file: track + its waypoints
        wpts = [{"lat": r["lat"], "lon": r["lon"], "ele": r.get("ele_m"),
                 "name": f"{r['km']:.0f}km {r['name']}",
                 "desc": r.get("desc") or _osm_desc(r),
                 "sym": r.get("sym"), "type": r.get("cat")}
                for r in sorted(osm_rows + cur_rows, key=lambda x: x["km"])]
        write_gpx(os.path.join(GPX_DIR, stage["id"] + "_annotated.gpx"),
                  [(stage["name"], simplify(track))], waypoints=wpts,
                  name=stage["name"] + " (with waypoints)", desc=stage["desc"])
        print(f"    wrote gpx/{stage['id']}_annotated.gpx ({len(wpts)} waypoints)")
        all_rows += osm_rows + cur_rows

    # one waypoint-only file for the whole route
    wpts = [{"lat": r["lat"], "lon": r["lon"], "ele": r.get("ele_m"),
             "name": f"{r['name']}",
             "desc": (r.get("desc") or _osm_desc(r)) +
                     f"  [{r['stage'].replace('pch_','')} km {r['km']:.0f}"
                     f"{', ' + str(r['offset_m']) + ' m off route' if r['offset_m'] > 150 else ''}]",
             "sym": r.get("sym"), "type": r.get("cat")}
            for r in sorted(all_rows, key=lambda x: (x["stage"], x["km"]))]
    write_gpx(os.path.join(GPX_DIR, "pch_waypoints.gpx"), [], waypoints=wpts,
              name="SF -> LA coast route: all waypoints",
              desc="Camping, lodging, water, food, bike shops, hazards and rail "
                   "bail-outs along the southbound Highway 1 route")
    print(f"\nwrote gpx/pch_waypoints.gpx: {len(wpts)} waypoints")

    # A trimmed file for the device you actually navigate with. The full set runs
    # to several hundred points per day - mostly city convenience stores and
    # public toilets - which is thorough but unreadable on a bike computer. This
    # keeps everything curated plus the categories that matter when you are
    # moving: water, camping, bike shops.
    ESSENTIAL = {"water", "camp", "bikeshop", "hazard", "info",
                 "bailout", "lodging", "services"}
    ess = [r for r in all_rows
           if r["cat"] in ESSENTIAL and (r.get("desc") or r["offset_m"] <= 500)]
    ewpts = [{"lat": r["lat"], "lon": r["lon"], "ele": r.get("ele_m"),
              "name": r["name"],
              "desc": (r.get("desc") or _osm_desc(r)) +
                      f"  [{r['stage'].replace('pch_','')} km {r['km']:.0f}]",
              "sym": r.get("sym"), "type": r.get("cat")}
             for r in sorted(ess, key=lambda x: (x["stage"], x["km"]))]
    write_gpx(os.path.join(GPX_DIR, "pch_waypoints_essential.gpx"), [],
              waypoints=ewpts,
              name="SF -> LA coast route: essential waypoints",
              desc="Curated stops plus water, campgrounds and bike shops only - "
                   "the readable subset for a bike computer")
    print(f"wrote gpx/pch_waypoints_essential.gpx: {len(ewpts)} waypoints")

    out = {
        "generated_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "osm_source": "Overpass `around` against the routed line; "
                      "radii per category in harvest_pch_pois.HARVEST",
        "stages": per_stage,
        "counts_by_category": _counts(all_rows),
        "pois": all_rows,
    }
    json.dump(out, open(os.path.join(DATA_DIR, "pch_pois.json"), "w"), indent=1)
    print(f"wrote data/pch_pois.json ({len(all_rows)} rows)")
    for sid, s in per_stage.items():
        print(f"  {sid:28s} {s['distance_km']:6.1f} km  "
              f"{s['osm_pois']:4d} OSM + {s['curated_pois']:2d} curated  "
              f"worst dry stretch {s['longest_no_water_no_food_km']:5.1f} km "
              f"from km {s['that_gap_starts_at_km']}")


def _osm_desc(r):
    t = r.get("tags") or {}
    bits = [f"{k}={v}" for k, v in t.items() if k != "name"]
    kind = r.get("kind", "")
    return (f"OSM {kind} ({r.get('osm','')})" + ("; " + "; ".join(bits) if bits else ""))


def _counts(rows):
    c = {}
    for r in rows:
        c[r["cat"]] = c.get(r["cat"], 0) + 1
    return dict(sorted(c.items(), key=lambda kv: -kv[1]))


if __name__ == "__main__":
    main()
