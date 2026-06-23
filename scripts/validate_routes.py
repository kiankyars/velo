#!/usr/bin/env python3
"""
Independent validation of the built GPX (does not trust build_routes.py).

Checks, per segment file and for the whole loop:
  1. XML is well-formed and is GPX 1.1 with trackpoints.
  2. Continuity: largest jump between consecutive trackpoints (within a track),
     and the gap at every segment seam + the loop-closure gap.
  3. Distance recomputed straight from the saved coordinates (haversine).
  4. Tunnel/ferry/motorway findings carried from data/route_summary.json.

Writes data/validation_report.json and prints a pass/fail table.
"""
import os, sys, json, math
import xml.etree.ElementTree as ET
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from route_waypoints import SEGMENTS
BASE = os.path.dirname(HERE)
GPX_DIR = os.path.join(BASE, "gpx")
DATA_DIR = os.path.join(BASE, "data")

# Thresholds
MAX_POINT_GAP_M = 600     # a single jump larger than this = suspicious discontinuity
MAX_SEAM_GAP_M = 50       # segments should join essentially exactly

def haversine(a, b):
    R = 6371000.0
    p1, p2 = math.radians(a[0]), math.radians(b[0])
    dp = math.radians(b[0]-a[0]); dl = math.radians(b[1]-a[1])
    h = math.sin(dp/2)**2 + math.cos(p1)*math.cos(p2)*math.sin(dl/2)**2
    return 2*R*math.asin(math.sqrt(h))

def parse_gpx(path):
    tree = ET.parse(path)                 # raises on malformed XML
    root = tree.getroot()
    ns = "{http://www.topografix.com/GPX/1/1}"
    pts = [(float(p.attrib["lat"]), float(p.attrib["lon"]))
           for p in root.iter(f"{ns}trkpt")]
    return pts

def main():
    report = {"segments": [], "seams": [], "ok": True, "problems": []}
    seg_pts = {}
    for seg in SEGMENTS:
        path = os.path.join(GPX_DIR, seg["id"] + ".gpx")
        entry = {"id": seg["id"], "file": os.path.basename(path)}
        try:
            pts = parse_gpx(path)
        except ET.ParseError as e:
            entry["xml_valid"] = False; entry["error"] = str(e)
            report["ok"] = False; report["problems"].append(f"{seg['id']}: bad XML")
            report["segments"].append(entry); continue
        entry["xml_valid"] = True
        entry["n_points"] = len(pts)
        if len(pts) < 2:
            report["ok"] = False; report["problems"].append(f"{seg['id']}: <2 points")
        gaps = [haversine(pts[i], pts[i+1]) for i in range(len(pts)-1)]
        dist_km = sum(gaps)/1000.0
        maxgap = max(gaps) if gaps else 0
        n_big = sum(1 for g in gaps if g > MAX_POINT_GAP_M)
        entry["distance_km"] = round(dist_km, 1)
        entry["max_point_gap_m"] = round(maxgap, 1)
        entry["jumps_over_threshold"] = n_big
        entry["continuous"] = n_big == 0
        if n_big:
            report["ok"] = False
            report["problems"].append(f"{seg['id']}: {n_big} jump(s) > {MAX_POINT_GAP_M} m (max {maxgap:.0f} m)")
        seg_pts[seg["id"]] = pts
        report["segments"].append(entry)

    # Seams (loop order) + loop closure
    order = [s["id"] for s in SEGMENTS]
    total = 0.0
    for e in report["segments"]:
        total += e.get("distance_km", 0)
    for i in range(len(order)):
        a_id = order[i]; b_id = order[(i+1) % len(order)]
        if a_id not in seg_pts or b_id not in seg_pts:
            continue
        gap = haversine(seg_pts[a_id][-1], seg_pts[b_id][0])
        kind = "loop-close" if i == len(order)-1 else "seam"
        ok = gap <= MAX_SEAM_GAP_M
        report["seams"].append({"from": a_id, "to": b_id, "kind": kind,
                                "gap_m": round(gap, 1), "ok": ok})
        if not ok:
            report["ok"] = False
            report["problems"].append(f"{kind} {a_id}->{b_id}: {gap:.0f} m gap")
    report["total_km"] = round(total, 1)

    # Carry safety findings from the build summary, if present
    sp = os.path.join(DATA_DIR, "route_summary.json")
    if os.path.exists(sp):
        s = json.load(open(sp))
        report["safety"] = {
            "motorway_km": round(sum(x["motorway_km"] for x in s["segments"]), 3),
            "trunk_km": round(sum(x.get("trunk_km", 0) for x in s["segments"]), 3),
            "motorroad_km": round(sum(x.get("motorroad_km", 0) for x in s["segments"]), 3),
            "active_rail_km": round(sum(x.get("rail_km", 0) for x in s["segments"]), 3),
            "ferry_km": round(sum(x["ferry_km"] for x in s["segments"]), 2),
            "tunnel_km": round(sum(x["tunnel_km"] for x in s["segments"]), 2),
            "road_tunnel_km": round(sum(x.get("tunnel_road_km", 0) for x in s["segments"]), 2),
        }

    json.dump(report, open(os.path.join(DATA_DIR, "validation_report.json"), "w"), indent=1)

    # Print
    print(f"{'segment':<16}{'XML':<5}{'pts':>7}{'km':>9}{'maxgap_m':>11}{'cont':>6}")
    for e in report["segments"]:
        print(f"{e['id']:<16}{'ok' if e.get('xml_valid') else 'BAD':<5}"
              f"{e.get('n_points',0):>7}{e.get('distance_km',0):>9}"
              f"{e.get('max_point_gap_m',0):>11}{'yes' if e.get('continuous') else 'NO':>6}")
    print(f"\nTotal distance: {report['total_km']} km")
    print("Seams (m):", [f"{x['from'][:5]}->{x['to'][:5]}:{x['gap_m']}" for x in report["seams"]])
    if "safety" in report:
        print("Safety:", json.dumps(report["safety"]))
    print("\nRESULT:", "ALL CHECKS PASS ✔" if report["ok"] else "PROBLEMS: " + "; ".join(report["problems"]))
    sys.exit(0 if report["ok"] else 1)

if __name__ == "__main__":
    main()
