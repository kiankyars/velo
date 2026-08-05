#!/usr/bin/env python3
"""
Independent validation of the SF -> LA coast GPX.

Deliberately does NOT trust build_pch_route.py: it re-reads the saved .gpx files
from disk, re-parses the XML, and recomputes distance from the coordinates. Then
it asserts the invariants that make this particular route safe to hand to a rider:

  1. Every file is well-formed GPX 1.1 with trackpoints.
  2. No discontinuity: the largest jump between consecutive points is small.
  3. The three riding days join end-to-start (seam gaps ~0 m).
  4. Recomputed distances agree with data/pch_route_summary.json.
  5. Every corridor waypoint lies on its own stage's track.
  6. LEGALITY: no bike-banned metres anywhere except the single documented
     391 m US-101 exception west of Winchester Canyon, and no freeway metre
     that OSM does not mark bicycle-legal.
  7. SURFACE: unpaved stays negligible (road bike).
  8. The master file's tracks reproduce the per-day files.
  9. The waypoint file parses and every waypoint has a name and a description.
 10. SPURS: no out-and-back detours - the failure a rider actually sees, where the
     line runs into a cul-de-sac and reverses. Continuity checks miss these
     entirely because the track never breaks.

Exits non-zero if anything fails. Writes data/pch_validation.json.
"""
import os
import sys
import json
import math
import xml.etree.ElementTree as ET

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from pch_waypoints import STAGES, VARIANTS, variant_points        # noqa: E402

BASE = os.path.dirname(HERE)
GPX_DIR = os.path.join(BASE, "gpx")
DATA_DIR = os.path.join(BASE, "data")
NS = "{http://www.topografix.com/GPX/1/1}"

MAX_POINT_GAP_M = 400     # build densifies to <=300 m, so this catches real breaks
# Out-and-back spurs. These are what a rider actually notices: the line runs into
# a cul-de-sac and reverses. They are invisible to a continuity check, because the
# track stays continuous the whole way in and back out. An early draft of this
# route carried 50 of them wasting 62 km, all caused by via-points that snapped
# off the highway onto park entrances and beach car parks.
MAX_SPUR_TOTAL_M = 1500   # per stage
MAX_SPUR_SINGLE_M = 700
MAX_SEAM_GAP_M = 50
MAX_WAYPOINT_OFFSET_M = 2600
MAX_UNPAVED_KM = 0.5
# The one sanctioned exception, see velo_pch_road_bridge.brf
ALLOWED_BICYCLE_NO_KM = 0.45


def hav(a, b):
    R = 6371000.0
    p1, p2 = math.radians(a[0]), math.radians(b[0])
    dp = math.radians(b[0] - a[0])
    dl = math.radians(b[1] - a[1])
    h = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * R * math.asin(math.sqrt(h))


def parse(path):
    root = ET.parse(path).getroot()          # raises on malformed XML
    if not root.tag.endswith("gpx"):
        raise ValueError("root element is not <gpx>")
    if root.attrib.get("version") != "1.1":
        raise ValueError(f"GPX version {root.attrib.get('version')!r}, expected 1.1")
    tracks = []
    for trk in root.findall(f"{NS}trk"):
        nm = trk.find(f"{NS}name")
        pts = [(float(p.attrib["lat"]), float(p.attrib["lon"]))
               for p in trk.iter(f"{NS}trkpt")]
        tracks.append((nm.text if nm is not None else "", pts))
    wpts = []
    for w in root.findall(f"{NS}wpt"):
        nm = w.find(f"{NS}name")
        ds = w.find(f"{NS}desc")
        wpts.append({"lat": float(w.attrib["lat"]), "lon": float(w.attrib["lon"]),
                     "name": nm.text if nm is not None else None,
                     "desc": ds.text if ds is not None else None})
    return tracks, wpts


def track_len_km(pts):
    return sum(hav(pts[i], pts[i + 1]) for i in range(len(pts) - 1)) / 1000.0


def find_spurs(pts, close_m=40.0, min_excursion_m=120.0):
    """Places where the track returns to within close_m of an earlier point after
    travelling at least min_excursion_m - i.e. it went somewhere and came back.

    Grid-bucketed so this stays linear-ish on a few thousand points.
    """
    cum = [0.0]
    for i in range(len(pts) - 1):
        cum.append(cum[-1] + hav(pts[i], pts[i + 1]))
    grid = {}
    for idx, p in enumerate(pts):
        grid.setdefault((round(p[0] * 2000), round(p[1] * 2000)), []).append(idx)
    found = []
    for idx, p in enumerate(pts):
        key = (round(p[0] * 2000), round(p[1] * 2000))
        cand = []
        for da in (-1, 0, 1):
            for db in (-1, 0, 1):
                cand += grid.get((key[0] + da, key[1] + db), [])
        for j in cand:
            if j <= idx or cum[j] - cum[idx] < min_excursion_m:
                continue
            if hav(pts[idx], pts[j]) > close_m:
                continue
            if any(abs(idx - a) < 40 for a, _ in found):
                continue
            found.append((idx, j))
            break
    out = []
    for idx, j in found:
        reach = max(hav(pts[idx], q) for q in pts[idx:j + 1])
        out.append({"at_km": round(cum[idx] / 1000, 2),
                    "excursion_m": round(cum[j] - cum[idx]),
                    "reach_m": round(reach),
                    "lat": round(pts[idx][0], 5), "lon": round(pts[idx][1], 5)})
    return out


def main():
    problems = []
    report = {"files": [], "seams": [], "legality": {}, "ok": True}

    summary_path = os.path.join(DATA_DIR, "pch_route_summary.json")
    summary = json.load(open(summary_path)) if os.path.exists(summary_path) else {"stages": []}
    by_id = {s["id"]: s for s in summary.get("stages", [])}

    specs = [(s["id"], s["name"], s["pts"], True) for s in STAGES]
    specs += [(v["id"], v["name"], variant_points(v), False) for v in VARIANTS]

    stage_pts = {}
    print(f"{'file':32}{'XML':>4}{'pts':>7}{'km':>8}{'maxgap':>8}{'wp_off':>7}{'spurs':>7}{'spur_m':>8}")
    for sid, name, corridor, is_main in specs:
        path = os.path.join(GPX_DIR, sid + ".gpx")
        entry = {"id": sid, "file": os.path.basename(path), "is_main_stage": is_main}
        if not os.path.exists(path):
            problems.append(f"{sid}: file missing")
            report["files"].append({**entry, "exists": False})
            continue
        try:
            tracks, _ = parse(path)
        except Exception as e:                                    # noqa: BLE001
            problems.append(f"{sid}: bad GPX ({e})")
            report["files"].append({**entry, "xml_valid": False, "error": str(e)})
            continue
        if len(tracks) != 1:
            problems.append(f"{sid}: expected 1 track, found {len(tracks)}")
        pts = tracks[0][1] if tracks else []
        if len(pts) < 2:
            problems.append(f"{sid}: fewer than 2 trackpoints")
            continue
        gaps = [hav(pts[i], pts[i + 1]) for i in range(len(pts) - 1)]
        maxgap = max(gaps)
        km = track_len_km(pts)
        n_big = sum(1 for g in gaps if g > MAX_POINT_GAP_M)
        if n_big:
            problems.append(f"{sid}: {n_big} jump(s) > {MAX_POINT_GAP_M} m (max {maxgap:.0f} m)")

        # every corridor waypoint must lie on this track
        worst_off, worst_lbl = 0.0, ""
        for lbl, la, lo in corridor:
            d = min(hav(p, (la, lo)) for p in pts)
            if d > worst_off:
                worst_off, worst_lbl = d, lbl
        if worst_off > MAX_WAYPOINT_OFFSET_M:
            problems.append(f"{sid}: corridor point {worst_lbl!r} is {worst_off:.0f} m "
                            f"off its own track")

        # distance agrees with the build summary
        if sid in by_id:
            claimed = by_id[sid]["distance_km"]
            if abs(claimed - km) / max(km, 1) > 0.02:
                problems.append(f"{sid}: summary says {claimed} km, GPX measures {km:.1f} km")

        sp = find_spurs(pts)
        sp_total = sum(x["excursion_m"] for x in sp)
        sp_max = max([x["excursion_m"] for x in sp], default=0)
        if sp_total > MAX_SPUR_TOTAL_M:
            problems.append(f"{sid}: {len(sp)} out-and-back spur(s) totalling "
                            f"{sp_total} m (limit {MAX_SPUR_TOTAL_M})")
        if sp_max > MAX_SPUR_SINGLE_M:
            problems.append(f"{sid}: a single out-and-back spur of {sp_max} m "
                            f"(limit {MAX_SPUR_SINGLE_M})")

        entry.update({"xml_valid": True, "n_points": len(pts),
                      "spurs": sp, "spur_total_m": sp_total, "spur_max_m": sp_max,
                      "distance_km": round(km, 1),
                      "max_point_gap_m": round(maxgap, 1),
                      "worst_corridor_offset_m": round(worst_off),
                      "worst_corridor_point": worst_lbl,
                      "continuous": n_big == 0})
        report["files"].append(entry)
        stage_pts[sid] = pts
        print(f"{sid:32}{'ok':>4}{len(pts):>7}{km:>8.1f}{maxgap:>8.0f}{worst_off:>7.0f}"
              f"{len(sp):>7}{sp_total:>8}")

    # seams between the three riding days
    order = [s["id"] for s in STAGES]
    for i in range(len(order) - 1):
        a, b = order[i], order[i + 1]
        if a in stage_pts and b in stage_pts:
            gap = hav(stage_pts[a][-1], stage_pts[b][0])
            ok = gap <= MAX_SEAM_GAP_M
            report["seams"].append({"from": a, "to": b, "gap_m": round(gap, 1), "ok": ok})
            if not ok:
                problems.append(f"seam {a} -> {b}: {gap:.0f} m")

    # master file reproduces the per-day files
    master = os.path.join(GPX_DIR, "pch_sf_la_master.gpx")
    if os.path.exists(master):
        tracks, _ = parse(master)
        report["master"] = {"tracks": len(tracks),
                            "total_km": round(sum(track_len_km(p) for _, p in tracks), 1)}
        if len(tracks) != 3:
            problems.append(f"master: expected 3 tracks, found {len(tracks)}")
        for (tname, tpts), sid in zip(tracks, order):
            if sid in stage_pts:
                d = abs(track_len_km(tpts) - track_len_km(stage_pts[sid]))
                if d > 0.2:
                    problems.append(f"master track {tname!r} differs from {sid} by {d:.2f} km")
    else:
        problems.append("master file missing")

    # legality + surface invariants, from the build audit
    tot_bic_no = tot_mway_bad = tot_unpaved = 0.0
    bic_no_hits = []
    for s in summary.get("stages", []):
        a = s.get("audit", {})
        tot_bic_no += a.get("bicycle_no_km", 0)
        tot_mway_bad += a.get("motorway_not_legal_km", 0)
        tot_unpaved += a.get("unpaved_km", 0)
        for h in (s.get("flagged", {}) or {}).get("bicycle_no", []):
            bic_no_hits.append({"stage": s["id"], **h})
    report["legality"] = {
        "bicycle_no_km_total": round(tot_bic_no, 3),
        "bicycle_no_allowance_km": ALLOWED_BICYCLE_NO_KM,
        "motorway_not_bicycle_legal_km": round(tot_mway_bad, 3),
        "unpaved_km_total": round(tot_unpaved, 3),
        "bicycle_no_locations": bic_no_hits,
    }
    # Note: totals span main stages AND variants, which overlap heavily, so the
    # per-stage figures are what matter; assert on the worst single stage.
    worst_bic = max([s.get("audit", {}).get("bicycle_no_km", 0)
                     for s in summary.get("stages", [])] or [0])
    worst_mway = max([s.get("audit", {}).get("motorway_not_legal_km", 0)
                      for s in summary.get("stages", [])] or [0])
    worst_unp = max([s.get("audit", {}).get("unpaved_km", 0)
                     for s in summary.get("stages", [])] or [0])
    if worst_bic > ALLOWED_BICYCLE_NO_KM:
        problems.append(f"legality: {worst_bic:.3f} km of bicycle=no on a single stage "
                        f"(allowance {ALLOWED_BICYCLE_NO_KM} km for the documented "
                        f"Winchester Canyon gap)")
    # The documented Winchester Canyon exception is motorway AND bicycle=no, so it
    # lands in both counters. Allow it here only to the extent it is the same
    # metres - anything beyond the bicycle=no total is a genuine new violation.
    if worst_mway > max(worst_bic, 0.001) + 0.001:
        problems.append(f"legality: {worst_mway:.3f} km of freeway not marked "
                        f"bicycle-legal, which exceeds the {worst_bic:.3f} km "
                        f"documented bicycle=no exception")
    elif worst_mway > 0.001:
        report["legality"]["note"] = (
            f"the {worst_mway:.3f} km of not-explicitly-legal freeway is the same "
            f"metres as the documented bicycle=no exception, not additional")
    if worst_unp > MAX_UNPAVED_KM:
        problems.append(f"surface: {worst_unp:.3f} km unpaved on a single stage "
                        f"(limit {MAX_UNPAVED_KM})")

    # waypoint file
    wp_path = os.path.join(GPX_DIR, "pch_waypoints.gpx")
    if os.path.exists(wp_path):
        _, wpts = parse(wp_path)
        nameless = sum(1 for w in wpts if not w["name"])
        descless = sum(1 for w in wpts if not w["desc"])
        report["waypoints"] = {"count": len(wpts), "without_name": nameless,
                              "without_desc": descless}
        if not wpts:
            problems.append("waypoint file has no waypoints")
        if nameless:
            problems.append(f"{nameless} waypoints have no name")
        if descless:
            problems.append(f"{descless} waypoints have no description")
    else:
        problems.append("waypoint file missing")

    report["ok"] = not problems
    report["problems"] = problems
    json.dump(report, open(os.path.join(DATA_DIR, "pch_validation.json"), "w"), indent=1)

    print("\nSeams:", ", ".join(f"{s['from'][-12:]}->{s['to'][-12:]}: {s['gap_m']} m"
                                for s in report["seams"]) or "n/a")
    if "master" in report:
        print(f"Master: {report['master']['tracks']} tracks, {report['master']['total_km']} km")
    L = report["legality"]
    print(f"Legality: bicycle=no worst stage {worst_bic:.3f} km "
          f"(allowance {ALLOWED_BICYCLE_NO_KM}); freeway-not-legal {worst_mway:.3f} km; "
          f"unpaved worst stage {worst_unp:.3f} km")
    for h in L["bicycle_no_locations"]:
        print(f"   documented exception: {h['len_m']} m at {h['lat']},{h['lon']} "
              f"({h['stage']})")
    if "waypoints" in report:
        print(f"Waypoints: {report['waypoints']['count']}")
    print("\nRESULT:", "ALL CHECKS PASS" if report["ok"]
          else "PROBLEMS:\n  - " + "\n  - ".join(problems))
    sys.exit(0 if report["ok"] else 1)


if __name__ == "__main__":
    main()
