#!/usr/bin/env python3
"""
Build the two candidate RETURN routes from Lagnieu (rider position, July 1 night)
to Mittelbuchen/Hanau, both 100% new terrain (no-repeat rule):

  A) return_a_mosel.gpx  - V50 Voie Bleue (Saone) -> Nancy/Metz -> Moselradweg
                           (Trier->Koblenz) -> Rhine Gorge (left bank) -> Mainz
                           -> north-bank Main -> Hanau/Mittelbuchen
  B) return_b_paris.gpx  - V50 -> EV6 (Canal du Centre/Loire) -> EV3 into Paris
                           -> EV3 Oise -> Picardy -> Arras -> DROCOURT (family)
                           -> RAVeL/Meuse EV19 (Namur->Liege) -> Aachen -> Cologne
                           -> Rhine (new: Cologne->Koblenz) -> Rhine Gorge -> Mainz
                           -> north-bank Main -> Hanau/Mittelbuchen

Geometry: BRouter trekking (audited profile) = every OSM node, then Douglas-
Peucker at 2.5 m so the line never deviates more than 2.5 m from the road
geometry while staying phone-importable. Safety tags audited (no motorway/
active rail/ferry). Prints per-leg + total distance/climb and writes gpx/.
"""
import os, sys, math
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from build_routes import brouter, analyze_brouter, haversine, haversine_total, GPX_DIR
import xml.sax.saxutils as sx

# (label, lat, lon) - major towns; BRouter snaps to the cycle network between them.
COMMON_RHINEGORGE = [
    ("Koblenz", 50.3605, 7.5892),
    ("Boppard", 50.2317, 7.5889),
    ("St. Goar", 50.1520, 7.7100),
    ("Oberwesel", 50.1070, 7.7270),
    ("Bacharach", 50.0580, 7.7690),
    ("Bingen", 49.9670, 7.8950),
    ("Ingelheim", 49.9740, 8.0560),
    ("Mainz", 49.9990, 8.2730),
    ("Frankfurt (north bank)", 50.1100, 8.6820),
    ("Hanau", 50.1329, 8.9170),
    ("Mittelbuchen", 50.1776, 8.8871),
]

ROUTE_A = [
    ("Lagnieu", 45.9020, 5.3410),
    ("Lyon", 45.7578, 4.8320),
    ("Trevoux", 45.9410, 4.7700),
    ("Macon", 46.3070, 4.8330),
    ("Tournus", 46.5670, 4.9070),
    ("Chalon-sur-Saone", 46.7800, 4.8540),
    ("Seurre", 47.0030, 5.1520),
    ("Auxonne", 47.1940, 5.3880),
    ("Gray", 47.4450, 5.5920),
    ("Port-sur-Saone", 47.6880, 6.0450),
    ("Corre", 47.9130, 5.9900),
    ("Epinal", 48.1740, 6.4490),
    ("Charmes", 48.3730, 6.2900),
    ("Nancy", 48.6920, 6.1840),
    ("Pont-a-Mousson", 48.9050, 6.0540),
    ("Metz", 49.1200, 6.1770),
    ("Thionville", 49.3580, 6.1680),
    ("Remich", 49.5450, 6.3670),
    ("Trier", 49.7560, 6.6410),
    ("Bernkastel-Kues", 49.9160, 7.0760),
    ("Zell (Mosel)", 50.0280, 7.1800),
    ("Cochem", 50.1460, 7.1660),
    ("Treis-Karden", 50.1800, 7.3000),
] + COMMON_RHINEGORGE

ROUTE_B = [
    ("Lagnieu", 45.9020, 5.3410),
    ("Lyon", 45.7578, 4.8320),
    ("Trevoux", 45.9410, 4.7700),
    ("Macon", 46.3070, 4.8330),
    ("Tournus", 46.5670, 4.9070),
    ("Chalon-sur-Saone", 46.7800, 4.8540),
    ("Chagny", 46.9100, 4.7500),
    ("Montchanin", 46.7470, 4.4740),
    ("Montceau-les-Mines", 46.6770, 4.3650),
    ("Paray-le-Monial", 46.4520, 4.1210),
    ("Digoin", 46.4810, 3.9800),
    ("Decize", 46.8300, 3.4620),
    ("Nevers", 46.9900, 3.1600),
    ("La Charite-sur-Loire", 47.1780, 3.0180),
    ("Cosne-Cours-sur-Loire", 47.4110, 2.9260),
    ("Briare", 47.6380, 2.7340),
    ("Montargis", 47.9970, 2.7320),
    ("Nemours", 48.2690, 2.6990),
    ("Moret-sur-Loing", 48.3720, 2.8170),
    ("Melun", 48.5400, 2.6600),
    ("Paris (Notre-Dame)", 48.8530, 2.3499),
    ("Saint-Denis", 48.9350, 2.3580),
    ("Creil", 49.2600, 2.4800),
    ("Compiegne", 49.4180, 2.8260),
    ("Noyon", 49.5800, 3.0000),
    ("Peronne", 49.9300, 2.9400),
    ("Bapaume", 50.1030, 2.8500),
    ("Arras", 50.2910, 2.7780),
    ("DROCOURT (family)", 50.3906, 2.9271),
    ("Douai", 50.3700, 3.0800),
    ("Valenciennes", 50.3600, 3.5200),
    ("Mons", 50.4540, 3.9520),
    ("Charleroi", 50.4110, 4.4440),
    ("Namur", 50.4670, 4.8700),
    ("Huy", 50.5200, 5.2400),
    ("Liege", 50.6450, 5.5730),
    ("Herve", 50.6400, 5.7900),
    ("Aachen", 50.7760, 6.0840),
    ("Dueren", 50.8000, 6.4800),
    ("Cologne", 50.9380, 6.9600),
    ("Bonn", 50.7350, 7.1000),
    ("Remagen", 50.5790, 7.2300),
    ("Andernach", 50.4400, 7.4000),
] + COMMON_RHINEGORGE


def perp_m(p, a, b):
    lat0 = math.radians(a[0])
    bx = (b[1]-a[1])*math.cos(lat0)*111320; by = (b[0]-a[0])*110540
    px = (p[1]-a[1])*math.cos(lat0)*111320; py = (p[0]-a[0])*110540
    if bx == 0 and by == 0:
        return math.hypot(px, py)
    t = max(0, min(1, (px*bx+py*by)/(bx*bx+by*by)))
    return math.hypot(px-t*bx, py-t*by)


def simplify(track, tol_m=2.5):
    keep = [False]*len(track); keep[0] = keep[-1] = True
    st = [(0, len(track)-1)]
    while st:
        s, e = st.pop(); dmax = 0; idx = -1
        for i in range(s+1, e):
            d = perp_m(track[i], track[s], track[e])
            if d > dmax:
                dmax = d; idx = i
        if dmax > tol_m and idx > 0:
            keep[idx] = True; st.append((s, idx)); st.append((idx, e))
    return [p for i, p in enumerate(track) if keep[i]]


def build(name, wps, batch=8):
    track = []
    cats_sum = {}
    legs = []
    i = 0
    while i < len(wps)-1:
        chunk = wps[i:i+batch+1]
        pts = [(lat, lon) for _, lat, lon in chunk]
        a = analyze_brouter(brouter(pts))
        seg = a["track"]
        if track and haversine((track[-1][0], track[-1][1]), (seg[0][0], seg[0][1])) < 50:
            seg = seg[1:]
        track += seg
        for k, v in a["cats"].items():
            cats_sum[k] = cats_sum.get(k, 0) + v
        legs.append((chunk[0][0], chunk[-1][0], a["brouter_len_km"]))
        i += batch
    dist = haversine_total(track)
    eles = [p[2] for p in track if p[2] is not None]
    gain = sum(max(0, eles[j+1]-eles[j]) for j in range(len(eles)-1))
    gaps = [haversine((track[j][0], track[j][1]), (track[j+1][0], track[j+1][1]))
            for j in range(len(track)-1)]
    print(f"\n== {name}: {dist:.1f} km, +{gain:.0f} m, {len(track)} raw pts, "
          f"max stitch gap {max(gaps):.0f} m")
    for a_, b_, km in legs:
        print(f"   {a_:<22} -> {b_:<22} {km:6.1f} km")
    print(f"   safety: motorway {cats_sum.get('motorway',0)/1000:.2f} km, "
          f"trunk {cats_sum.get('trunk',0)/1000:.2f}, rail {cats_sum.get('rail',0)/1000:.2f}, "
          f"ferry {cats_sum.get('ferry',0)/1000:.2f}, "
          f"tunnel {cats_sum.get('tunnel',0)/1000:.2f} (road {cats_sum.get('tunnel_road',0)/1000:.2f})")
    slim = simplify(track, 2.5)
    out = os.path.join(GPX_DIR, name + ".gpx")
    L = ['<?xml version="1.0" encoding="UTF-8"?>',
         '<gpx version="1.1" creator="velo-return" xmlns="http://www.topografix.com/GPX/1/1">',
         f'  <trk><name>{sx.escape(name)}</name><trkseg>']
    for lat, lon, ele in slim:
        if ele is not None:
            L.append(f'   <trkpt lat="{lat:.6f}" lon="{lon:.6f}"><ele>{ele:.1f}</ele></trkpt>')
        else:
            L.append(f'   <trkpt lat="{lat:.6f}" lon="{lon:.6f}"></trkpt>')
    L += ['  </trkseg></trk>', '</gpx>']
    open(out, "w").write("\n".join(L) + "\n")
    print(f"   wrote {out}: {len(slim)} pts ({os.path.getsize(out)/1e6:.2f} MB, <=2.5 m deviation)")
    return dist, gain


if __name__ == "__main__":
    a = build("return_a_mosel", ROUTE_A)
    b = build("return_b_paris", ROUTE_B)
    print(f"\nSUMMARY  A (Mosel): {a[0]:.0f} km +{a[1]:.0f} m   "
          f"B (Paris/Drocourt): {b[0]:.0f} km +{b[1]:.0f} m")
