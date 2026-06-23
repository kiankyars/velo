#!/usr/bin/env python3
"""
Build the Velo Journey 2026 "Frankfurt Loop" GPX from real cycle infrastructure.

For each segment, route through the ordered waypoints (route_waypoints.py) with
BRouter on OpenStreetMap data using the `trekking` profile (avoids motorways,
prefers signed cycle routes). The official EuroVelo backbone is reproduced by
following the real EV waypoint towns; the bespoke EV8 and the connectors are
routed the same way. BRouter's per-way tags are kept so we can verify there are
no motorways, locate every ferry/tunnel, and measure how much of each leg runs
on OSM's international/national/regional cycle network (route_bicycle_*cn).

Outputs (in gpx/):
  - one <seg>.gpx per segment, plus velo_loop_master.gpx (all five tracks)
Outputs (in data/):
  - route_summary.json  (distances, ascent, ferries, tunnels, network %)

Responses are cached under scripts/.cache so re-runs are free and reproducible.
"""
import os, sys, json, math, time, hashlib, urllib.request, urllib.parse
import xml.sax.saxutils as sx
import xml.etree.ElementTree as ET

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from route_waypoints import SEGMENTS
BASE = os.path.dirname(HERE)
GPX_DIR = os.path.join(BASE, "gpx")
DATA_DIR = os.path.join(BASE, "data")
CACHE = os.path.join(HERE, ".cache")
WP = json.load(open(os.path.join(DATA_DIR, "waypoints.json")))
os.makedirs(CACHE, exist_ok=True)

# We route on a copy of BRouter's stock "trekking" profile (avoids motorways,
# allows ferries, follows cycle routes) with processUnusedTags=true so every OSM
# tag - tunnel, bridge, ferry, motorroad - is echoed and can be validated.
PROFILE_FILE = os.path.join(HERE, "velo_trekking.brf")
PROFILE_CACHE_KEY = "velo_trekking"   # stable key (the server id is ephemeral)
_PROFILE_ID = None

OFFICIAL_EV15_URL = "https://en.eurovelo.com/route/get-gpx/36"
# Main continuous official EV15 line for this trip:
# Andermatt -> St Margrethen -> Konstanz -> Basel -> Alsace/Strasbourg ->
# Karlsruhe/Maxau -> Speyer -> Eich -> Mainz. The omitted track numbers are
# alternate bank variants or downstream sections beyond Mainz.
OFFICIAL_EV15_TRACKS = (
    list(range(1, 8)) + list(range(10, 17)) +
    list(range(22, 27)) + list(range(32, 37))
)

def get_profile_id():
    global _PROFILE_ID
    if _PROFILE_ID:
        return _PROFILE_ID
    body = open(PROFILE_FILE, "rb").read()
    req = urllib.request.Request("https://brouter.de/brouter/profile", data=body,
                                 headers={"User-Agent": "velo-planner/1.0"})
    with urllib.request.urlopen(req, timeout=60) as r:
        _PROFILE_ID = json.load(r)["profileid"]
    return _PROFILE_ID

def haversine(a, b):
    R = 6371000.0
    p1, p2 = math.radians(a[0]), math.radians(b[0])
    dp = math.radians(b[0] - a[0]); dl = math.radians(b[1] - a[1])
    h = math.sin(dp/2)**2 + math.cos(p1)*math.cos(p2)*math.sin(dl/2)**2
    return 2*R*math.asin(math.sqrt(h))

def brouter(latlons):
    lonlats = "|".join(f"{lon:.6f},{lat:.6f}" for lat, lon in latlons)
    key = hashlib.md5((PROFILE_CACHE_KEY + "|" + lonlats).encode()).hexdigest()
    cf = os.path.join(CACHE, f"brouter_{key}.json")
    if os.path.exists(cf):
        return json.load(open(cf))
    url = "https://brouter.de/brouter?" + urllib.parse.urlencode({
        "lonlats": lonlats, "profile": get_profile_id(), "alternativeidx": "0", "format": "geojson"})
    for attempt in range(5):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "velo-planner/1.0"})
            with urllib.request.urlopen(req, timeout=150) as r:
                d = json.load(r)
            json.dump(d, open(cf, "w"))
            return d
        except Exception as e:
            sys.stderr.write(f"  brouter retry {attempt}: {e}\n"); time.sleep(3*(attempt+1))
    raise RuntimeError("brouter failed")

def classify(waytags):
    """Return set of flags for a way-tag string."""
    t = waytags or ""
    flags = set()
    if "highway=motorway" in t or "motorway_link" in t:
        flags.add("motorway")
    if "highway=trunk" in t or "trunk_link" in t:
        flags.add("trunk")
    if "motorroad=yes" in t:
        flags.add("motorroad")
    if "route=ferry" in t or " ferry=" in (" " + t):
        flags.add("ferry")
    if "tunnel=" in t and "tunnel=no" not in t:
        flags.add("tunnel")
    # Active railway only - rail-trails are tagged railway=abandoned/disused/razed
    if (("railway=rail" in t or "railway=light_rail" in t or "railway=subway" in t or
         "railway=tram" in t or "railway=funicular" in t)
            and not any(x in t for x in ("railway=abandoned", "railway=disused",
                                         "railway=razed", "railway=dismantled"))):
        flags.add("rail")
    if ("route_bicycle_icn=yes" in t or "route_bicycle_ncn=yes" in t or
            "route_bicycle_rcn=yes" in t or "route_bicycle_lcn=yes" in t):
        flags.add("cyclenet")
    if "route_bicycle_icn=yes" in t:
        flags.add("icn")
    return flags

def tunnel_is_bikepath(tags):
    """True if a tunnel is on a dedicated cycle/foot way (legal & normal for bikes)."""
    return ("highway=cycleway" in tags or "highway=path" in tags or
            "highway=footway" in tags or "bicycle=designated" in tags or
            "tunnel=building_passage" in tags)

def build_segment(seg):
    pts = [(WP[q]["lat"], WP[q]["lon"]) for _, q in seg["waypoints"]]
    d = brouter(pts)
    feat = d["features"][0]
    coords = feat["geometry"]["coordinates"]          # [lon,lat,(ele)]
    msgs = feat["properties"]["messages"]
    hdr = msgs[0]
    iLon, iLat = hdr.index("Longitude"), hdr.index("Latitude")
    iDist = hdr.index("Distance"); iWT = hdr.index("WayTags")
    iEle = hdr.index("Elevation")

    # Track points (lat, lon, ele). BRouter coords may be 2D; take ele from messages.
    track = []
    for c in coords:
        lon, lat = c[0], c[1]
        ele = c[2] if len(c) > 2 else None
        track.append([lat, lon, ele])

    # Per-way analysis
    cats = {"motorway": 0.0, "trunk": 0.0, "motorroad": 0.0, "rail": 0.0,
            "ferry": 0.0, "tunnel": 0.0, "tunnel_road": 0.0, "cyclenet": 0.0, "icn": 0.0}
    total_m = 0.0
    ferries, tunnels, motorways = [], [], []
    for row in msgs[1:]:
        seg_m = float(row[iDist])
        total_m += seg_m
        lon = int(row[iLon]) / 1e6; lat = int(row[iLat]) / 1e6
        fl = classify(row[iWT])
        for k in cats:
            if k in fl:
                cats[k] += seg_m
        if "tunnel" in fl and not tunnel_is_bikepath(row[iWT]):
            cats["tunnel_road"] += seg_m
        if "ferry" in fl:
            ferries.append((lat, lon, seg_m, row[iWT]))
        if "tunnel" in fl:
            tunnels.append((lat, lon, seg_m, row[iWT]))
        if "motorway" in fl or "trunk" in fl or "motorroad" in fl:
            motorways.append((lat, lon, seg_m, row[iWT]))

    # Merge consecutive ferry/tunnel rows into single features
    def merge(rows):
        out = []
        for lat, lon, m, wt in rows:
            if out and abs(out[-1][0]-lat) < 0.02 and abs(out[-1][1]-lon) < 0.02:
                out[-1][2] += m
            else:
                out.append([lat, lon, m, wt])
        return out
    ferries, tunnels, motorways = merge(ferries), merge(tunnels), merge(motorways)

    # Elevation gain from track (smoothed: only count rises)
    eles = [p[2] for p in track if p[2] is not None]
    gain = sum(max(0, eles[i+1]-eles[i]) for i in range(len(eles)-1)) if len(eles) > 1 else 0
    dist_km = haversine_total(track)
    return {
        "seg": seg, "track": track,
        "brouter_len_km": float(feat["properties"]["track-length"]) / 1000.0,
        "dist_km": dist_km, "ascent_m": gain,
        "n_points": len(track), "total_m": total_m,
        "cats": cats, "ferries": ferries, "tunnels": tunnels, "motorways": motorways,
    }

def download_official_ev15():
    cf = os.path.join(CACHE, "official_ev15.gpx")
    if os.path.exists(cf):
        return cf
    req = urllib.request.Request(OFFICIAL_EV15_URL, headers={"User-Agent": "velo-planner/1.0"})
    with urllib.request.urlopen(req, timeout=90) as r:
        data = r.read()
    open(cf, "wb").write(data)
    return cf

def parse_gpx_track_numbers(path, track_numbers):
    ns = "{http://www.topografix.com/GPX/1/1}"
    root = ET.parse(path).getroot()
    wanted = set(track_numbers)
    parts = []
    for idx, trk in enumerate(root.findall(f"{ns}trk"), start=1):
        if idx not in wanted:
            continue
        part = []
        for p in trk.iter(f"{ns}trkpt"):
            ele = p.find(f"{ns}ele")
            part.append([
                float(p.attrib["lat"]),
                float(p.attrib["lon"]),
                float(ele.text) if ele is not None and ele.text else None,
            ])
        parts.append((idx, part))
    missing = sorted(wanted - {idx for idx, _ in parts})
    if missing:
        raise RuntimeError(f"Official EV15 GPX missing track(s): {missing}")
    return parts

def route_between(a, b):
    d = brouter([(a[0], a[1]), (b[0], b[1])])
    coords = d["features"][0]["geometry"]["coordinates"]
    return [[c[1], c[0], c[2] if len(c) > 2 else None] for c in coords]

def append_official_part(track, part, label):
    if not part:
        return
    if not track:
        track.extend(part)
        return
    gap = haversine((track[-1][0], track[-1][1]), (part[0][0], part[0][1]))
    if gap < 100:
        track.extend(part[1:])
    elif gap <= 5000:
        print(f"  official EV15 connector before track {label}: {gap:.0f} m", flush=True)
        connector = route_between(track[-1], part[0])
        track.extend(connector[1:-1])
        track.extend(part)
    else:
        raise RuntimeError(f"Official EV15 track {label} is disconnected by {gap:.0f} m")

def build_official_ev15_segment(seg):
    """Use official EuroVelo 15 geometry for the Rhine backbone.

    BRouter's waypoint route cut inland near Osthofen between Mainz and Worms.
    The official EV15 GPX follows the Rhine-side line via Eich, so Segment 1 is
    assembled as: Mittelbuchen->Mainz connector by BRouter, then official EV15
    GPX from Mainz back to Andermatt for our southbound direction.
    """
    connector_seg = {**seg, "waypoints": seg["waypoints"][:5]}
    connector = build_segment(connector_seg)

    official_northbound = []
    for idx, part in parse_gpx_track_numbers(download_official_ev15(), OFFICIAL_EV15_TRACKS):
        append_official_part(official_northbound, part, idx)
    official_southbound = list(reversed(official_northbound))

    track = connector["track"]
    gap = haversine(
        (track[-1][0], track[-1][1]),
        (official_southbound[0][0], official_southbound[0][1]),
    )
    if gap < 100:
        track = track[:-1]
    elif gap <= 5000:
        print(f"  connector to official EV15 at Mainz: {gap:.0f} m", flush=True)
        link = route_between(track[-1], official_southbound[0])
        track.extend(link[1:-1])
    else:
        raise RuntimeError(f"Mittelbuchen connector is {gap:.0f} m from official EV15")
    track.extend(official_southbound)
    andermatt = WP["Andermatt, Switzerland"]
    target = [andermatt["lat"], andermatt["lon"], track[-1][2]]
    gap = haversine((track[-1][0], track[-1][1]), (target[0], target[1]))
    if gap > 1:
        print(f"  official EV15 to EV17 Andermatt seam: {gap:.0f} m", flush=True)
        link = route_between(track[-1], target)
        track.extend(link[1:])

    dist_km = haversine_total(track)
    eles = [p[2] for p in track if p[2] is not None]
    gain = sum(max(0, eles[i+1]-eles[i]) for i in range(len(eles)-1)) if len(eles) > 1 else 0

    cats = {k: float(v) for k, v in connector["cats"].items()}
    official_m = haversine_total(official_southbound) * 1000.0
    cats["cyclenet"] += official_m
    cats["icn"] += official_m
    return {
        "seg": seg, "track": track,
        "brouter_len_km": connector["brouter_len_km"],
        "dist_km": dist_km, "ascent_m": gain,
        "n_points": len(track), "total_m": connector["total_m"] + official_m,
        "cats": cats, "ferries": connector["ferries"], "tunnels": connector["tunnels"],
        "motorways": connector["motorways"],
        "source": "Mittelbuchen->Mainz by BRouter; Mainz->Andermatt official EuroVelo 15 GPX",
    }

def haversine_total(track):
    s = 0.0
    for i in range(len(track)-1):
        s += haversine((track[i][0], track[i][1]), (track[i+1][0], track[i+1][1]))
    return s/1000.0

def densify(track, max_m=150.0):
    """Insert interpolated points so consecutive points are <= max_m apart.
    Faithful on straight spans (tunnels/bridges/canal paths) where OSM has no
    intermediate nodes; curved ways already carry their shape nodes from OSM."""
    out = []
    for i in range(len(track)):
        out.append(track[i])
        if i == len(track) - 1:
            break
        a, b = track[i], track[i+1]
        d = haversine((a[0], a[1]), (b[0], b[1]))
        if d > max_m:
            n = int(d // max_m)
            for k in range(1, n + 1):
                f = k / (n + 1)
                lat = a[0] + (b[0]-a[0]) * f
                lon = a[1] + (b[1]-a[1]) * f
                ele = None
                if a[2] is not None and b[2] is not None:
                    ele = a[2] + (b[2]-a[2]) * f
                out.append([lat, lon, ele])
    return out

def write_gpx(path, segments):
    """segments: list of (name, track[[lat,lon,ele],...])"""
    lines = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<gpx version="1.1" creator="velo-build_routes" '
             'xmlns="http://www.topografix.com/GPX/1/1">']
    for name, track in segments:
        lines.append(f'  <trk><name>{sx.escape(name)}</name><trkseg>')
        for lat, lon, ele in track:
            if ele is not None:
                lines.append(f'   <trkpt lat="{lat:.6f}" lon="{lon:.6f}"><ele>{ele:.1f}</ele></trkpt>')
            else:
                lines.append(f'   <trkpt lat="{lat:.6f}" lon="{lon:.6f}"></trkpt>')
        lines.append('  </trkseg></trk>')
    lines.append('</gpx>')
    open(path, "w").write("\n".join(lines) + "\n")

def main():
    results = []
    for seg in SEGMENTS:
        print(f"Routing {seg['id']} ({len(seg['waypoints'])} wp)...", flush=True)
        r = build_official_ev15_segment(seg) if seg["id"] == "ev15_rhine" else build_segment(seg)
        results.append(r)
        c = r["cats"]; tot = r["total_m"] or 1
        print(f"  {r['dist_km']:.1f} km  ascent {r['ascent_m']:.0f} m  "
              f"cyclenet {100*c['cyclenet']/tot:.0f}% (icn {100*c['icn']/tot:.0f}%)  "
              f"ferry {c['ferry']/1000:.1f}km  tunnel {c['tunnel']/1000:.1f}km "
              f"(road {c['tunnel_road']/1000:.2f})  motorway {c['motorway']/1000:.3f} "
              f"trunk {c['trunk']/1000:.2f} motorroad {c['motorroad']/1000:.2f} rail {c['rail']/1000:.2f}km")

    # Densify tracks (<=150 m spacing) for clean device rendering & continuity
    for r in results:
        r["track"] = densify(r["track"])
    # Per-segment GPX
    for r in results:
        write_gpx(os.path.join(GPX_DIR, r["seg"]["id"] + ".gpx"),
                  [(r["seg"]["name"], r["track"])])
    # Master GPX
    write_gpx(os.path.join(GPX_DIR, "velo_loop_master.gpx"),
              [(r["seg"]["name"], r["track"]) for r in results])

    # Seam continuity (end of seg i vs start of seg i+1)
    seams = []
    for i in range(len(results)-1):
        a = results[i]["track"][-1]; b = results[i+1]["track"][0]
        gap = haversine((a[0], a[1]), (b[0], b[1]))
        seams.append({"from": results[i]["seg"]["id"], "to": results[i+1]["seg"]["id"],
                      "gap_m": round(gap, 1)})
    # loop closure
    a = results[-1]["track"][-1]; b = results[0]["track"][0]
    loop_gap = haversine((a[0], a[1]), (b[0], b[1]))

    summary = {
        "profile": "trekking (BRouter, processUnusedTags=true) on OpenStreetMap",
        "generated_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "total_km": round(sum(r["dist_km"] for r in results), 1),
        "total_ascent_m": round(sum(r["ascent_m"] for r in results)),
        "loop_closure_gap_m": round(loop_gap, 1),
        "seams": seams,
        "segments": [],
    }
    for r in results:
        c = r["cats"]; tot = r["total_m"] or 1
        summary["segments"].append({
            "id": r["seg"]["id"], "name": r["seg"]["name"], "ev": r["seg"]["ev"],
            "desc": r["seg"]["desc"],
            "source": r.get("source", "BRouter trekking profile on OpenStreetMap"),
            "distance_km": round(r["dist_km"], 1),
            "ascent_m": round(r["ascent_m"]),
            "n_points": r["n_points"],
            "on_cyclenetwork_pct": round(100*c["cyclenet"]/tot, 1),
            "on_eurovelo_icn_pct": round(100*c["icn"]/tot, 1),
            "motorway_km": round(c["motorway"]/1000, 3),
            "trunk_km": round(c["trunk"]/1000, 3),
            "motorroad_km": round(c["motorroad"]/1000, 3),
            "rail_km": round(c["rail"]/1000, 3),
            "ferry_km": round(c["ferry"]/1000, 2),
            "tunnel_km": round(c["tunnel"]/1000, 2),
            "tunnel_road_km": round(c["tunnel_road"]/1000, 2),
            "ferries": [{"lat": round(x[0],5), "lon": round(x[1],5),
                         "len_m": round(x[2]), "tags": x[3]} for x in r["ferries"]],
            "tunnels": [{"lat": round(x[0],5), "lon": round(x[1],5),
                         "len_m": round(x[2]), "bikepath": tunnel_is_bikepath(x[3]),
                         "tags": x[3]} for x in r["tunnels"]],
            "motorway_hits": [{"lat": round(x[0],5), "lon": round(x[1],5),
                               "len_m": round(x[2]), "tags": x[3]} for x in r["motorways"]],
        })
    json.dump(summary, open(os.path.join(DATA_DIR, "route_summary.json"), "w"), indent=1)
    print(f"\nTOTAL {summary['total_km']} km, ascent {summary['total_ascent_m']} m")
    print("seam gaps (m):", [s["gap_m"] for s in seams], " loop close:", summary["loop_closure_gap_m"])

if __name__ == "__main__":
    main()
