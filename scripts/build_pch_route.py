#!/usr/bin/env python3
"""
Build the San Francisco -> Los Angeles coast GPX from real road data.

Geometry comes from BRouter on OpenStreetMap using `velo_pch_road.brf` (see the
header of that file for why the stock trekking profile is wrong here). Every OSM
way tag is echoed back, so the finished line can be audited rather than trusted:

  * legality   - any bicycle=no metre is a hard failure (the profile excludes it,
                 this proves it); freeway metres are reported separately, split
                 into bicycle-legal shoulder vs. anything else
  * surface    - unpaved kilometres, for a road bike on 25-32 mm
  * structures - every tunnel and bridge, located
  * climbs     - detected from the elevation profile, not from memory
  * cue sheet  - cumulative distance to every corridor waypoint

Outputs
  gpx/pch_day1_sf_limekiln.gpx, pch_day2_limekiln_refugio.gpx,
  gpx/pch_day3_refugio_la.gpx          - the three riding days
  gpx/pch_sf_la_master.gpx             - all three as one multi-track file
  gpx/pch_day1_alt_*.gpx, pch_day2_alt_*.gpx  - the variant endpoints
  data/pch_route_summary.json          - distances, audit, climbs, cue sheet

Responses are cached under scripts/.cache so re-runs are free and reproducible.
"""
import os
import sys
import json
import math
import time
import hashlib
import urllib.request
import urllib.parse
import xml.sax.saxutils as sx

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from pch_waypoints import (STAGES, VARIANTS, variant_points,           # noqa: E402
                            PERMISSIVE_LEGS)
from build_routes import (analyze_brouter, haversine, haversine_total,  # noqa: E402
                          densify)

BASE = os.path.dirname(HERE)
GPX_DIR = os.path.join(BASE, "gpx")
DATA_DIR = os.path.join(BASE, "data")
CACHE = os.path.join(HERE, ".cache")
PROFILE_FILE = os.path.join(HERE, "velo_pch_road.brf")
# The permissive twin, used ONLY for legs named in PERMISSIVE_LEGS.
BRIDGE_PROFILE_FILE = os.path.join(HERE, "velo_pch_road_bridge.brf")
PROFILE_CACHE_KEY = "velo_pch_road_v6"   # bump to invalidate the cache
os.makedirs(CACHE, exist_ok=True)

# BRouter takes a limited number of via points per request; route in overlapping
# chunks and stitch. 8 legs per call keeps well inside the limit.
CHUNK = 8
# Douglas-Peucker tolerance. 2.5 m keeps every turn while producing a file a
# phone app will actually import (the repo's established figure).
SIMPLIFY_TOL_M = 2.5
# ...then re-densify to cap the point spacing. Simplifying alone leaves multi-km
# straights on highway sections (a 2.7 km single segment through the Guadalupe
# dunes), which renders badly on a device and makes a continuity check
# meaningless. Interpolating along a segment Douglas-Peucker already certified as
# within 2.5 m of the road adds no positional error, so this is free accuracy-wise.
DENSIFY_MAX_M = 300.0

_PROFILE_IDS = {}


def profile_id(bridge=False):
    path = BRIDGE_PROFILE_FILE if bridge else PROFILE_FILE
    if path in _PROFILE_IDS:
        return _PROFILE_IDS[path]
    body = open(path, "rb").read()
    req = urllib.request.Request("https://brouter.de/brouter/profile", data=body,
                                 headers={"User-Agent": "velo-planner/1.0"})
    with urllib.request.urlopen(req, timeout=60) as r:
        _PROFILE_IDS[path] = json.load(r)["profileid"]
    return _PROFILE_IDS[path]


def brouter(latlons, bridge=False, nogos=()):
    """Route through the given (lat, lon) points with the PCH road profile.

    bridge=True selects the permissive twin profile; only legs named in
    pch_waypoints.PERMISSIVE_LEGS may use it.

    nogos is a sequence of (lat, lon, radius_m) exclusion circles. Used where a
    routing constraint cannot be expressed in the profile at all: the Camp
    Pendleton bicycle gate is tagged access=permit, and `permit` is not in
    BRouter's lookups.dat, so the router cannot see that it needs a pass. A small
    nogo over the gate is the only way to keep the line out of the base.
    """
    lonlats = "|".join(f"{lon:.6f},{lat:.6f}" for lat, lon in latlons)
    nogo_s = "|".join(f"{lon:.6f},{lat:.6f},{r}" for lat, lon, r in nogos)
    tag_key = PROFILE_CACHE_KEY + ("_bridge" if bridge else "") + ("|nogo:" + nogo_s if nogo_s else "")
    key = hashlib.md5((tag_key + "|" + lonlats).encode()).hexdigest()
    cf = os.path.join(CACHE, f"pch_{key}.json")
    if os.path.exists(cf):
        return json.load(open(cf))
    q = {"lonlats": lonlats, "profile": profile_id(bridge),
         "alternativeidx": "0", "format": "geojson"}
    if nogo_s:
        q["nogos"] = nogo_s
    url = "https://brouter.de/brouter?" + urllib.parse.urlencode(q)
    last = None
    for attempt in range(5):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "velo-planner/1.0"})
            with urllib.request.urlopen(req, timeout=180) as r:
                d = json.load(r)
            json.dump(d, open(cf, "w"))
            return d
        except Exception as e:                                  # noqa: BLE001
            last = e
            sys.stderr.write(f"  brouter retry {attempt}: {e}\n")
            time.sleep(3 * (attempt + 1))
    raise RuntimeError(f"brouter failed: {last}")


# --------------------------------------------------------------------------
# auditing
# --------------------------------------------------------------------------
def tag(waytags, key):
    """Value of `key` in a BRouter WayTags string, or None."""
    for t in (waytags or "").split():
        if t.startswith(key + "="):
            return t[len(key) + 1:]
    return None


def audit_rows(msgs):
    """Walk BRouter's per-way message rows and total up what matters here."""
    h = msgs[0]
    iLon, iLat = h.index("Longitude"), h.index("Latitude")
    iDist, iWT = h.index("Distance"), h.index("WayTags")

    cats = {
        "total": 0.0,
        "bicycle_no": 0.0,          # must be 0.0 - illegal
        "permit": 0.0,              # access=permit: gated, needs a pass
        "motorway": 0.0,            # all freeway metres
        "motorway_legal": 0.0,      # freeway explicitly open to bikes
        "motorway_illegal": 0.0,    # freeway with no bicycle tag - must be 0.0
        "trunk": 0.0, "primary": 0.0, "secondary": 0.0, "tertiary": 0.0,
        "residential": 0.0, "cycleway": 0.0, "path": 0.0, "service": 0.0,
        "unpaved": 0.0, "tunnel": 0.0, "bridge": 0.0,
        "cyclenet": 0.0, "ferry": 0.0, "steps": 0.0,
    }
    UNPAVED = {"unpaved", "gravel", "fine_gravel", "compacted", "ground", "dirt",
               "earth", "mud", "sand", "grass", "grass_paver", "pebblestone",
               "rock", "stone", "cobblestone", "metal", "wood"}
    hits = {"bicycle_no": [], "motorway": [], "unpaved": [], "tunnel": [],
            "ferry": [], "permit": []}

    for row in msgs[1:]:
        m = float(row[iDist])
        wt = row[iWT] or ""
        lat, lon = int(row[iLat]) / 1e6, int(row[iLon]) / 1e6
        cats["total"] += m
        hw = tag(wt, "highway") or ""
        bic = tag(wt, "bicycle")
        surf = tag(wt, "surface")

        # Permit-gated ways. BOTH spellings matter and neither is visible to the
        # router: `permit` is not a value in BRouter's lookups.dat, so a profile
        # cannot exclude it. Camp Pendleton's Stuart Mesa Road and Vandegrift
        # Boulevard are tagged bicycle=permit across every way; an earlier version
        # of this audit only looked for access=permit and therefore reported 80 m
        # where the real figure was far higher.
        if "access=permit" in wt or "bicycle=permit" in wt:
            cats["permit"] += m
            hits["permit"].append([lat, lon, m, wt])
        if bic in ("no", "private"):
            cats["bicycle_no"] += m
            hits["bicycle_no"].append([lat, lon, m, wt])
        if hw in ("motorway", "motorway_link"):
            cats["motorway"] += m
            if bic in ("yes", "designated", "permissive"):
                cats["motorway_legal"] += m
            else:
                cats["motorway_illegal"] += m
            hits["motorway"].append([lat, lon, m, wt])
        for k, names in (("trunk", ("trunk", "trunk_link")),
                         ("primary", ("primary", "primary_link")),
                         ("secondary", ("secondary", "secondary_link")),
                         ("tertiary", ("tertiary", "tertiary_link")),
                         ("residential", ("residential", "living_street")),
                         ("cycleway", ("cycleway",)),
                         ("path", ("path", "footway", "track", "pedestrian")),
                         ("service", ("service",)),
                         ("steps", ("steps",))):
            if hw in names:
                cats[k] += m
        if surf in UNPAVED:
            cats["unpaved"] += m
            hits["unpaved"].append([lat, lon, m, wt])
        tun = tag(wt, "tunnel")
        if tun and tun != "no":
            cats["tunnel"] += m
            hits["tunnel"].append([lat, lon, m, wt])
        brg = tag(wt, "bridge")
        if brg and brg != "no":
            cats["bridge"] += m
        if "route=ferry" in wt:
            cats["ferry"] += m
            hits["ferry"].append([lat, lon, m, wt])
        if any(f"route_bicycle_{x}cn=yes" in wt for x in "inrl"):
            cats["cyclenet"] += m

    def merge(rows, deg=0.01):
        out = []
        for lat, lon, m, wt in rows:
            if out and abs(out[-1][0] - lat) < deg and abs(out[-1][1] - lon) < deg:
                out[-1][2] += m
            else:
                out.append([lat, lon, m, wt])
        return out

    return cats, {k: merge(v) for k, v in hits.items()}


def cumdist(track):
    """Cumulative distance in km at each track point."""
    out = [0.0]
    for i in range(len(track) - 1):
        out.append(out[-1] + haversine((track[i][0], track[i][1]),
                                       (track[i + 1][0], track[i + 1][1])) / 1000.0)
    return out


def smooth_ele(track, window=9):
    """Moving-average the elevation so SRTM noise doesn't invent 30 m climbs."""
    e = [p[2] if p[2] is not None else 0.0 for p in track]
    n = len(e)
    half = window // 2
    out = []
    run = sum(e[:min(window, n)])
    for i in range(n):
        lo, hi = max(0, i - half), min(n, i + half + 1)
        out.append(sum(e[lo:hi]) / (hi - lo))
    return out


def detect_climbs(track, min_gain_m=70.0, max_dip_m=18.0):
    """Find sustained ascents in the elevation profile.

    Walks the smoothed profile accumulating gain; a descent deeper than
    max_dip_m ends the current climb. Runs with at least min_gain_m are kept.
    Reported numbers therefore come from the route's own elevation data.
    """
    ele = smooth_ele(track)
    km = cumdist(track)
    climbs = []
    i = 0
    n = len(track)
    while i < n - 1:
        if ele[i + 1] <= ele[i]:
            i += 1
            continue
        start = i
        peak_i = i
        j = i
        while j < n - 1:
            if ele[j + 1] > ele[peak_i]:
                peak_i = j + 1
            elif ele[peak_i] - ele[j + 1] > max_dip_m:
                break
            j += 1
        gain = ele[peak_i] - ele[start]
        if gain >= min_gain_m:
            length_km = km[peak_i] - km[start]
            climbs.append({
                "start_km": round(km[start], 1),
                "summit_km": round(km[peak_i], 1),
                "length_km": round(length_km, 2),
                "gain_m": round(gain),
                "avg_pct": round(100 * gain / (length_km * 1000), 1) if length_km > 0.05 else None,
                "summit_ele_m": round(ele[peak_i]),
                "summit_lat": round(track[peak_i][0], 5),
                "summit_lon": round(track[peak_i][1], 5),
            })
        i = max(peak_i, start + 1)
    return climbs


def ascent(track):
    e = [p[2] for p in track if p[2] is not None]
    return sum(max(0.0, e[i + 1] - e[i]) for i in range(len(e) - 1))


# --------------------------------------------------------------------------
# geometry helpers
# --------------------------------------------------------------------------
def perp_m(p, a, b):
    lat0 = math.radians(a[0])
    bx = (b[1] - a[1]) * math.cos(lat0) * 111320
    by = (b[0] - a[0]) * 110540
    px = (p[1] - a[1]) * math.cos(lat0) * 111320
    py = (p[0] - a[0]) * 110540
    if bx == 0 and by == 0:
        return math.hypot(px, py)
    t = max(0.0, min(1.0, (px * bx + py * by) / (bx * bx + by * by)))
    return math.hypot(px - t * bx, py - t * by)


def simplify(track, tol_m=SIMPLIFY_TOL_M):
    """Douglas-Peucker: drop collinear points, keep every turn."""
    if len(track) < 3:
        return list(track)
    keep = [False] * len(track)
    keep[0] = keep[-1] = True
    stack = [(0, len(track) - 1)]
    while stack:
        s, e = stack.pop()
        dmax, idx = 0.0, -1
        for i in range(s + 1, e):
            d = perp_m(track[i], track[s], track[e])
            if d > dmax:
                dmax, idx = d, i
        if dmax > tol_m and idx > 0:
            keep[idx] = True
            stack.append((s, idx))
            stack.append((idx, e))
    return [p for i, p in enumerate(track) if keep[i]]


def build(points, nogos=()):
    """Route through `points` (label, lat, lon), chunked, honouring PERMISSIVE_LEGS.

    The point list is first split into runs at every leg named in
    PERMISSIVE_LEGS. Ordinary runs use the strict profile; a permissive leg is
    routed on its own with the bridge profile. This keeps the exception confined
    to exactly the two waypoints that name it.
    """
    runs = []          # (list_of_points, is_bridge)
    cur = [points[0]]
    for i in range(len(points) - 1):
        pair = (points[i][0], points[i + 1][0])
        if pair in PERMISSIVE_LEGS:
            if len(cur) > 1:
                runs.append((cur, False))
            runs.append(([points[i], points[i + 1]], True))
            cur = [points[i + 1]]
        else:
            cur.append(points[i + 1])
    if len(cur) > 1:
        runs.append((cur, False))

    track, msgs_all, legs, bridged = [], [], [], []
    filtered_ascend = 0.0
    for run_pts, is_bridge in runs:
        i = 0
        step = 1 if is_bridge else CHUNK
        while i < len(run_pts) - 1:
            chunk = run_pts[i:i + step + 1]
            d = brouter([(lat, lon) for _, lat, lon in chunk], bridge=is_bridge,
                        nogos=nogos)
            a = analyze_brouter(d)
            seg = a["track"]
            if track and haversine((track[-1][0], track[-1][1]),
                                   (seg[0][0], seg[0][1])) < 60:
                seg = seg[1:]
            track += seg
            props = d["features"][0]["properties"]
            # BRouter's own noise-filtered ascent. Summing raw SRTM point-to-point
            # over ~8,000 points inflates the total badly (it counts sampling
            # noise as climbing), so this is the number to quote.
            filtered_ascend += float(props.get("filtered ascend") or 0)
            msgs_all.append(props["messages"])
            legs.append((chunk[0][0], chunk[-1][0], a["brouter_len_km"], is_bridge))
            if is_bridge:
                bridged.append({
                    "from": chunk[0][0], "to": chunk[-1][0],
                    "km": round(a["brouter_len_km"], 2),
                    "reason": PERMISSIVE_LEGS[(chunk[0][0], chunk[-1][0])],
                })
            i += step
    return track, msgs_all, legs, filtered_ascend, bridged


def merge_audits(msgs_all):
    total = None
    hits = {}
    for msgs in msgs_all:
        cats, h = audit_rows(msgs)
        if total is None:
            total = cats
        else:
            for k, v in cats.items():
                total[k] += v
        for k, v in h.items():
            hits.setdefault(k, []).extend(v)
    return total, hits


def cue_sheet(points, track):
    """Cumulative km to the nearest track point for each corridor waypoint."""
    km = cumdist(track)
    out = []
    search_from = 0
    for label, lat, lon in points:
        # Full scan forward from the previous match. An earlier version bailed
        # out early on a "we are clearly past it" heuristic and silently pinned
        # every waypoint after El Capitan to km 2.8; a route this long is only a
        # few thousand points, so just scan it properly.
        best, best_d = search_from, float("inf")
        for j in range(search_from, len(track)):
            d = haversine((track[j][0], track[j][1]), (lat, lon))
            if d < best_d:
                best_d, best = d, j
        out.append({"label": label, "km": round(km[best], 1),
                    "offset_m": round(best_d), "lat": lat, "lon": lon,
                    "ele_m": round(track[best][2]) if track[best][2] is not None else None})
        search_from = max(search_from, best - 20)
    return out


def write_gpx(path, tracks, waypoints=None, name=None, desc=None):
    """tracks: list of (name, track). waypoints: list of dicts (optional)."""
    L = ['<?xml version="1.0" encoding="UTF-8"?>',
         '<gpx version="1.1" creator="velo-build_pch_route" '
         'xmlns="http://www.topografix.com/GPX/1/1" '
         'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" '
         'xsi:schemaLocation="http://www.topografix.com/GPX/1/1 '
         'http://www.topografix.com/GPX/1/1/gpx.xsd">']
    L.append('  <metadata>')
    L.append(f'    <name>{sx.escape(name or os.path.basename(path))}</name>')
    if desc:
        L.append(f'    <desc>{sx.escape(desc)}</desc>')
    L.append(f'    <time>{time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}</time>')
    L.append('  </metadata>')
    for w in (waypoints or []):
        L.append(f'  <wpt lat="{w["lat"]:.6f}" lon="{w["lon"]:.6f}">')
        if w.get("ele") is not None:
            L.append(f'    <ele>{w["ele"]:.1f}</ele>')
        L.append(f'    <name>{sx.escape(w["name"])}</name>')
        if w.get("desc"):
            L.append(f'    <desc>{sx.escape(w["desc"])}</desc>')
        if w.get("cmt"):
            L.append(f'    <cmt>{sx.escape(w["cmt"])}</cmt>')
        if w.get("sym"):
            L.append(f'    <sym>{sx.escape(w["sym"])}</sym>')
        if w.get("type"):
            L.append(f'    <type>{sx.escape(w["type"])}</type>')
        L.append('  </wpt>')
    for tname, track in tracks:
        L.append('  <trk>')
        L.append(f'    <name>{sx.escape(tname)}</name>')
        L.append('    <trkseg>')
        for lat, lon, ele in track:
            if ele is not None:
                L.append(f'     <trkpt lat="{lat:.6f}" lon="{lon:.6f}"><ele>{ele:.1f}</ele></trkpt>')
            else:
                L.append(f'     <trkpt lat="{lat:.6f}" lon="{lon:.6f}"></trkpt>')
        L.append('    </trkseg>')
        L.append('  </trk>')
    L.append('</gpx>')
    open(path, "w").write("\n".join(L) + "\n")


def report(label, cats, hits, dist_km, climb_m, npts, filt_m):
    tot = cats["total"] or 1.0
    print(f"\n== {label}: {dist_km:.1f} km, +{filt_m:.0f} m filtered "
          f"(+{climb_m:.0f} m raw SRTM), {npts} raw pts")
    print(f"   road mix: trunk {cats['trunk']/1000:6.1f}  primary {cats['primary']/1000:6.1f}  "
          f"secondary {cats['secondary']/1000:6.1f}  tertiary {cats['tertiary']/1000:6.1f}")
    print(f"             residential {cats['residential']/1000:5.1f}  cycleway {cats['cycleway']/1000:5.1f}  "
          f"path/track {cats['path']/1000:5.1f}  service {cats['service']/1000:5.1f}")
    print(f"   freeway:  {cats['motorway']/1000:.2f} km total "
          f"({cats['motorway_legal']/1000:.2f} bicycle-legal, "
          f"{cats['motorway_illegal']/1000:.2f} NOT)")
    print(f"   legality: bicycle=no {cats['bicycle_no']/1000:.3f} km   "
          f"access=permit {cats['permit']/1000:.3f} km   "
          f"ferry {cats['ferry']/1000:.2f}   steps {cats['steps']/1000:.3f}")
    print(f"   surface:  unpaved {cats['unpaved']/1000:.2f} km  "
          f"({100*cats['unpaved']/tot:.2f}%)   tunnel {cats['tunnel']/1000:.2f} km   "
          f"bridge {cats['bridge']/1000:.2f} km")
    print(f"   on OSM cycle network: {100*cats['cyclenet']/tot:.0f}%")
    for k in ("bicycle_no", "motorway", "unpaved", "tunnel"):
        for lat, lon, m, wt in hits.get(k, []):
            if m < 120 and k in ("unpaved",):
                continue
            short = " ".join(t for t in wt.split()
                             if t.split("=")[0] in ("highway", "bicycle", "surface",
                                                    "tunnel", "name", "tracktype"))
            print(f"     ! {k:11s} {m:7.0f} m at {lat:.4f},{lon:.4f}  {short}")


def main():
    only = sys.argv[1:] or None
    results = []
    all_specs = [(s["id"], s["name"], s["desc"], s["pts"], True, s.get("nogos", ()),
                  s.get("optional", False)) for s in STAGES]
    all_specs += [(v["id"], v["name"], v["desc"], variant_points(v), False,
                   v.get("nogos", ()), False) for v in VARIANTS]

    for sid, sname, sdesc, pts, is_main, nogos, optional in all_specs:
        if only and sid not in only:
            continue
        print(f"\nRouting {sid} ({len(pts)} corridor points)...", flush=True)
        track, msgs_all, legs, filt_m, bridged = build(pts, nogos=nogos)
        cats, hits = merge_audits(msgs_all)
        dist_km = haversine_total(track)
        climb_m = ascent(track)
        report(sid, cats, hits, dist_km, climb_m, len(track), filt_m)
        for a, b, km, isb in legs:
            mark = "  [PERMISSIVE PROFILE]" if isb else ""
            print(f"     {a:38s} -> {b:38s} {km:7.1f} km{mark}")
        slim = densify(simplify(track), DENSIFY_MAX_M)
        results.append({
            "id": sid, "name": sname, "desc": sdesc, "is_main": is_main,
            "optional": optional,
            "track": track, "slim": slim, "points": pts,
            "cats": cats, "hits": hits,
            "dist_km": dist_km, "climb_m": climb_m, "filt_m": filt_m,
            "climbs": detect_climbs(track),
            "bridged": bridged,
            "cues": cue_sheet(pts, track),
        })
        out = os.path.join(GPX_DIR, sid + ".gpx")
        write_gpx(out, [(sname, slim)], name=sname, desc=sdesc)
        print(f"   wrote {out}: {len(slim)} pts, {os.path.getsize(out)/1e6:.2f} MB")

    mains = [r for r in results if r["is_main"]]
    core = [r for r in mains if not r.get("optional")]
    # Two master files on purpose: the core three-day trip to Los Angeles, and the
    # same plus the optional San Diego extension. Keeping them separate means
    # loading the extension is a decision, not a surprise.
    if len(core) == 3:
        master = os.path.join(GPX_DIR, "pch_sf_la_master.gpx")
        write_gpx(master, [(r["name"], r["slim"]) for r in core],
                  name="San Francisco -> Los Angeles by the coast (3 stages)",
                  desc="Southbound Highway 1: SF -> Limekiln SP -> Refugio SB -> LA Union Station")
        print(f"\nwrote {master}: {sum(len(r['slim']) for r in core)} pts, "
              f"{os.path.getsize(master)/1e6:.2f} MB")
        print(f"CORE TOTAL {sum(r['dist_km'] for r in core):.1f} km, "
              f"+{sum(r['filt_m'] for r in core):.0f} m filtered")
    if len(mains) > len(core) and len(mains) >= 4:
        master = os.path.join(GPX_DIR, "pch_sf_sd_master.gpx")
        write_gpx(master, [(r["name"], r["slim"]) for r in mains],
                  name="San Francisco -> San Diego by the coast (4 stages)",
                  desc="Southbound Highway 1 extended: SF -> Limekiln SP -> Refugio SB "
                       "-> LA -> San Diego. Camp Pendleton bypassed on the "
                       "Caltrans-permitted I-5 shoulder (no base pass needed).")
        print(f"wrote {master}: {sum(len(r['slim']) for r in mains)} pts, "
              f"{os.path.getsize(master)/1e6:.2f} MB")
        print(f"EXTENDED TOTAL {sum(r['dist_km'] for r in mains):.1f} km, "
              f"+{sum(r['filt_m'] for r in mains):.0f} m filtered")
    for i in range(len(mains) - 1):
        g = haversine((mains[i]["track"][-1][0], mains[i]["track"][-1][1]),
                      (mains[i + 1]["track"][0][0], mains[i + 1]["track"][0][1]))
        print(f"seam {mains[i]['id']} -> {mains[i+1]['id']}: {g:.1f} m")

    # Merge into any existing summary rather than replacing it, so building a
    # single stage (`build_pch_route.py pch_day3_refugio_la`) cannot silently
    # throw away the other stages' audit data.
    summary_path = os.path.join(DATA_DIR, "pch_route_summary.json")
    summary = {"stages": []}
    if os.path.exists(summary_path):
        try:
            summary = json.load(open(summary_path))
        except (OSError, ValueError):
            summary = {"stages": []}
    summary["generated_utc"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    summary["profile"] = ("velo_pch_road.brf (BRouter, processUnusedTags=true) on "
                          "OpenStreetMap; PERMISSIVE_LEGS use velo_pch_road_bridge.brf")
    summary["simplify_tolerance_m"] = SIMPLIFY_TOL_M
    summary["densify_max_spacing_m"] = DENSIFY_MAX_M
    rebuilt = {r["id"] for r in results}
    summary["stages"] = [s for s in summary.get("stages", [])
                         if s.get("id") not in rebuilt]
    for r in results:
        c = r["cats"]
        tot = c["total"] or 1.0
        summary["stages"].append({
            "id": r["id"], "name": r["name"], "desc": r["desc"],
            "is_main_stage": r["is_main"],
            "optional_extension": r.get("optional", False),
            "distance_km": round(r["dist_km"], 1),
            "ascent_m_filtered": round(r["filt_m"]),
            "ascent_m_raw_srtm": round(r["climb_m"]),
            "points_raw": len(r["track"]), "points_saved": len(r["slim"]),
            "audit": {
                "bicycle_no_km": round(c["bicycle_no"] / 1000, 3),
                "access_permit_km": round(c["permit"] / 1000, 3),
                "motorway_km": round(c["motorway"] / 1000, 3),
                "motorway_bicycle_legal_km": round(c["motorway_legal"] / 1000, 3),
                "motorway_not_legal_km": round(c["motorway_illegal"] / 1000, 3),
                "ferry_km": round(c["ferry"] / 1000, 3),
                "steps_km": round(c["steps"] / 1000, 3),
                "unpaved_km": round(c["unpaved"] / 1000, 3),
                "unpaved_pct": round(100 * c["unpaved"] / tot, 3),
                "tunnel_km": round(c["tunnel"] / 1000, 3),
                "bridge_km": round(c["bridge"] / 1000, 3),
                "on_cyclenetwork_pct": round(100 * c["cyclenet"] / tot, 1),
                "road_mix_km": {k: round(c[k] / 1000, 1) for k in
                                ("trunk", "primary", "secondary", "tertiary",
                                 "residential", "cycleway", "path", "service")},
            },
            "flagged": {k: [{"lat": round(x[0], 5), "lon": round(x[1], 5),
                             "len_m": round(x[2]), "tags": x[3]}
                            for x in v if x[2] >= 50]
                        for k, v in r["hits"].items() if v},
            "climbs": r["climbs"],
            "permissive_legs_used": r["bridged"],
            "cue_sheet": r["cues"],
        })
    order = {sid: i for i, sid in enumerate(
        [s["id"] for s in STAGES] + [v["id"] for v in VARIANTS])}
    summary["stages"].sort(key=lambda s: order.get(s.get("id"), 999))
    json.dump(summary, open(summary_path, "w"), indent=1)
    print(f"\nwrote {summary_path} ({len(summary['stages'])} stages)")


if __name__ == "__main__":
    main()
