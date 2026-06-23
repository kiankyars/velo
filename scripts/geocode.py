#!/usr/bin/env python3
"""Geocode route waypoints via Photon (komoot), cache to data/waypoints.json (resumable)."""
import os, sys, json, time, urllib.request, urllib.parse
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from route_waypoints import SEGMENTS
BASE = os.path.dirname(HERE)
OUT = os.path.join(BASE, "data", "waypoints.json")

# Hand-verified coordinates for points geocoders tend to misplace (mountain passes).
OVERRIDES = {
    "Oberalppass, Switzerland": (46.6597, 8.6710),
    "Furkapass, Switzerland": (46.5723, 8.4150),
    "Gletsch, Switzerland": (46.5616, 8.3640),
    "Passo del Turchino, Italy": (44.5527, 8.7560),
    "Brennero, Italy": (47.0023, 11.5063),
    # Photon returned province/area centroids or hill-town namesakes for these;
    # pin them to the actual city centres on the Po plain / Adige valley.
    "Bolzano, Italy": (46.4983, 11.3548),
    "Mantova, Italy": (45.1564, 10.7914),
    "Cremona, Italy": (45.1335, 10.0245),
    "Piacenza, Italy": (45.0526, 9.6929),
}

def geocode(q):
    if q in OVERRIDES:
        return (*OVERRIDES[q], "override")
    url = "https://photon.komoot.io/api/?" + urllib.parse.urlencode({"q": q, "limit": 1})
    req = urllib.request.Request(url, headers={"User-Agent": "velo-planner/1.0"})
    with urllib.request.urlopen(req, timeout=25) as r:
        d = json.load(r)
    feats = d.get("features") or []
    if not feats:
        return None
    lon, lat = feats[0]["geometry"]["coordinates"]
    p = feats[0]["properties"]
    return lat, lon, f"{p.get('name','')},{p.get('country','')}"[:60]

cache = {}  # rebuild fresh with Photon for consistency
queries, seen = [], set()
for seg in SEGMENTS:
    for label, q in seg["waypoints"]:
        if q not in seen:
            seen.add(q); queries.append((label, q))

print(f"{len(queries)} unique queries")
for label, q in queries:
    for attempt in range(4):
        try:
            res = geocode(q)
            if res is None:
                print(f"  !! NO RESULT: {q}"); break
            lat, lon, name = res
            cache[q] = {"label": label, "lat": lat, "lon": lon, "src": name}
            print(f"  {lat:.4f},{lon:.4f}  {label}")
            if name != "override": time.sleep(0.4)
            break
        except Exception as e:
            print(f"  retry {q}: {e}"); time.sleep(2*(attempt+1))
json.dump(cache, open(OUT, "w"), indent=1, ensure_ascii=False)
missing = [q for _,q in queries if q not in cache]
print(f"\nWrote {len(cache)} to {OUT}. MISSING({len(missing)}): {missing}")
