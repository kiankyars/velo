#!/usr/bin/env python3
"""Make a dense GPX from your current position to the end of a loop segment.

Finds the nearest point on the chosen segment's official line, routes a short
connector from where you are onto it (BRouter), then takes the segment from
there to its end and simplifies it (Douglas-Peucker, keeping every turn) so the
file stays small enough to import into phone apps like Ride with GPS / OsmAnd.

Usage:
    python3 scripts/gpx_from_here.py LAT LON [segment_id] [tolerance_m]
    # e.g. python3 scripts/gpx_from_here.py 49.012944 8.365083 ev15_rhine 5

Writes gpx/<segment_id>_from_here.gpx.
"""
import os, sys, math, json, urllib.request, urllib.parse
import xml.etree.ElementTree as ET
import xml.sax.saxutils as sx

HERE = os.path.dirname(os.path.abspath(__file__))
GPX_DIR = os.path.join(os.path.dirname(HERE), "gpx")
NS = "{http://www.topografix.com/GPX/1/1}"


def hav(a, b):
    R = 6371000.0
    p1, p2 = math.radians(a[0]), math.radians(b[0])
    dp = math.radians(b[0]-a[0]); dl = math.radians(b[1]-a[1])
    h = math.sin(dp/2)**2 + math.cos(p1)*math.cos(p2)*math.sin(dl/2)**2
    return 2*R*math.asin(math.sqrt(h))


def load(path):
    root = ET.parse(path).getroot()
    ns = NS if root.tag.startswith("{") else ""
    out = []
    for p in root.iter(f"{ns}trkpt"):
        e = p.find(f"{ns}ele")
        out.append([float(p.attrib["lat"]), float(p.attrib["lon"]),
                    float(e.text) if e is not None and e.text else None])
    return out


def perp_m(p, a, b):
    """Perpendicular distance (metres) of p from segment a-b (equirectangular)."""
    lat0 = math.radians(a[0])
    bx = (b[1]-a[1]) * math.cos(lat0) * 111320; by = (b[0]-a[0]) * 110540
    px = (p[1]-a[1]) * math.cos(lat0) * 111320; py = (p[0]-a[0]) * 110540
    if bx == 0 and by == 0:
        return math.hypot(px, py)
    t = max(0, min(1, (px*bx + py*by) / (bx*bx + by*by)))
    return math.hypot(px - t*bx, py - t*by)


def simplify(track, tol_m):
    """Douglas-Peucker: drop near-collinear points but keep every turn that
    deviates more than tol_m. Yields a small, app-importable file."""
    keep = [False]*len(track); keep[0] = keep[-1] = True
    stack = [(0, len(track)-1)]
    while stack:
        s, e = stack.pop(); dmax = 0; idx = -1
        for i in range(s+1, e):
            d = perp_m(track[i], track[s], track[e])
            if d > dmax:
                dmax = d; idx = i
        if dmax > tol_m and idx > 0:
            keep[idx] = True; stack.append((s, idx)); stack.append((idx, e))
    return [p for i, p in enumerate(track) if keep[i]]


def brouter(latlons):
    lonlats = "|".join(f"{lon:.6f},{lat:.6f}" for lat, lon in latlons)
    url = "https://brouter.de/brouter?" + urllib.parse.urlencode(
        {"lonlats": lonlats, "profile": "trekking", "alternativeidx": "0", "format": "geojson"})
    d = json.load(urllib.request.urlopen(
        urllib.request.Request(url, headers={"User-Agent": "velo/1.0"}), timeout=90))
    return [[c[1], c[0], c[2] if len(c) > 2 else None]
            for c in d["features"][0]["geometry"]["coordinates"]]


def write_gpx(path, name, track):
    L = ['<?xml version="1.0" encoding="UTF-8"?>',
         '<gpx version="1.1" creator="velo-gpx_from_here" xmlns="http://www.topografix.com/GPX/1/1">',
         f'  <trk><name>{sx.escape(name)}</name><trkseg>']
    for lat, lon, ele in track:
        if ele is not None:
            L.append(f'   <trkpt lat="{lat:.6f}" lon="{lon:.6f}"><ele>{ele:.1f}</ele></trkpt>')
        else:
            L.append(f'   <trkpt lat="{lat:.6f}" lon="{lon:.6f}"></trkpt>')
    L += ['  </trkseg></trk>', '</gpx>']
    open(path, "w").write("\n".join(L) + "\n")


def main():
    if len(sys.argv) < 3:
        print(__doc__); sys.exit(1)
    lat, lon = float(sys.argv[1]), float(sys.argv[2])
    seg = sys.argv[3] if len(sys.argv) > 3 else "ev15_rhine"
    tol_m = float(sys.argv[4]) if len(sys.argv) > 4 else 5.0  # turn-keeping tolerance

    track = load(os.path.join(GPX_DIR, seg + ".gpx"))
    i = min(range(len(track)), key=lambda j: hav((track[j][0], track[j][1]), (lat, lon)))
    off = hav((track[i][0], track[i][1]), (lat, lon))
    print(f"{seg}: nearest point #{i}/{len(track)} is {off:.0f} m from you")

    if off > 30:
        print("routing connector onto the route...", flush=True)
        connector = brouter([(lat, lon), (track[i][0], track[i][1])])
        forward = connector[:-1] + track[i:]
    else:
        forward = [[lat, lon, track[i][2]]] + track[i+1:]

    out_track = simplify(forward, tol_m)   # small + app-importable, keeps every turn
    km = sum(hav((forward[k][0], forward[k][1]), (forward[k+1][0], forward[k+1][1]))
             for k in range(len(forward)-1)) / 1000
    out = os.path.join(GPX_DIR, f"{seg}_from_here.gpx")
    write_gpx(out, f"{seg} from current position to end", out_track)
    print(f"wrote {out}: {len(out_track)} pts, {km:.0f} km, {os.path.getsize(out)/1e6:.2f} MB "
          f"(turns kept within {tol_m:.0f} m)")


if __name__ == "__main__":
    main()
