#!/usr/bin/env python3
"""
Condensation forecast for the campsites, for sleeping out with no tent.

The question this answers is NOT "will it be cold" - a 45 F bag has margin against
every low on this route. It is "will the bag get wet", and the number that decides
that is the **temperature-minus-dewpoint spread** at the overnight minimum, not the
low temperature and not the word "fog" in the forecast text.

Why the spread and not the temperature: dew forms on any surface whose skin
temperature falls below the air's dewpoint. A sleeping bag radiates to a clear night
sky and sits 1-3 F BELOW air temperature, so:

    spread > ~5 F   -> the shell stays above the dewpoint. Nothing deposits.
    spread 2-5 F    -> marginal. Radiative cooling alone can tip it over.
    spread 0-2 F    -> the air is AT saturation. Deposition is not a risk, it is
                       the forecast. Fog droplets land as well as dew condensing.

This distinction matters because the plain-language NWS forecast can read reassuring
("Patchy fog after 5am", "Partly cloudy") for a site whose grid data says RH 99-100%
and spread 0 F all night. Refugio is exactly that case. Read the numbers.

Source: NWS API. The `forecastGridData` endpoint carries dewpoint and
relativeHumidity, which the plain-language `forecast` endpoint does not.
Grid resolution is ~2.5 km, so a narrow canyon like Limekiln is represented by a
cell that is partly ridge - treat canyon sites as a floor, not a ceiling.

Usage:
    python3 scripts/check_camp_dewpoint.py [--nights 4] [--json]

Writes data/pch_camp_condensation.json when --json is given.
"""
import os
import sys
import json
import time
import argparse
import datetime
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(os.path.dirname(HERE), "data")
UA = "velo-planner/1.0 (github.com/kiankyars/velo)"

# The sites you would actually sleep at, in itinerary order.
SITES = [
    ("Limekiln SP (night 1, planned)", 36.00998, -121.51835,
     "Redwood canyon, ~200 m from the surf. Inside the marine layer."),
    ("Pfeiffer Big Sur SP (night 1, alt)", 36.25331, -121.78330,
     "Big Sur River valley, ridge between it and the ocean. Above/inland of the "
     "marine layer."),
    ("Refugio SB (night 2, planned)", 34.46243, -120.04830,
     "On the Gaviota coast shoreline, south-facing into the Santa Barbara Channel."),
]

# Hours (local) sampled for the overnight minimum window.
NIGHT_HOURS = (23, 1, 3, 5)
PDT_OFFSET = 7  # hours behind UTC in August


def get(url, tries=4):
    last = None
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=90) as r:
                return json.loads(r.read().decode())
        except Exception as e:                                       # noqa: BLE001
            last = e
            time.sleep(2 ** i)
    raise RuntimeError(f"{url}: {last}")


def c2f(c):
    return None if c is None else c * 9 / 5 + 32


def expand(grid, key):
    """NWS grid values carry ISO8601 durations; expand to one entry per hour."""
    out = {}
    for v in grid.get(key, {}).get("values", []):
        stamp, _, dur = v["validTime"].partition("/")
        dt = datetime.datetime.fromisoformat(stamp.replace("Z", "+00:00"))
        hours = 1
        if dur.startswith("PT") and dur.endswith("H"):
            hours = int(dur[2:-1] or 1)
        elif dur.startswith("P") and "DT" in dur:                    # e.g. P1DT2H
            d, _, h = dur[1:].partition("DT")
            hours = int(d.rstrip("D") or 0) * 24 + int(h.rstrip("H") or 0)
        for h in range(max(hours, 1)):
            out[dt + datetime.timedelta(hours=h)] = v["value"]
    return out


def verdict(spread_f):
    if spread_f is None:
        return "unknown", "no dewpoint data"
    if spread_f <= 2:
        return "SATURATED", "air is at saturation - the bag will wet out"
    if spread_f <= 5:
        return "marginal", "radiative cooling alone can tip the shell below dewpoint"
    return "dry", "shell stays above dewpoint - nothing deposits"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--nights", type=int, default=4)
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    today = datetime.datetime.now(datetime.timezone.utc).date()
    horizon = today + datetime.timedelta(days=args.nights)
    report = {"generated_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
              "source": "api.weather.gov forecastGridData (dewpoint + RH) and "
                        "forecast (fog wording)",
              "method": "temperature minus dewpoint at the overnight minimum; a bag "
                        "radiating to the sky sits 1-3 F below air temperature",
              "sites": []}

    for name, la, lo, note in SITES:
        pt = get(f"https://api.weather.gov/points/{la},{lo}")["properties"]
        grid = get(pt["forecastGridData"])["properties"]
        text = get(pt["forecast"])["properties"]["periods"]
        T, D, R = (expand(grid, k) for k in
                   ("temperature", "dewpoint", "relativeHumidity"))

        fog = [p["shortForecast"] for p in text if not p["isDaytime"]][:args.nights]
        rows, worst = [], None
        for k in sorted(T):
            local = k - datetime.timedelta(hours=PDT_OFFSET)
            if local.hour not in NIGHT_HOURS or local.date() > horizon:
                continue
            t, d, rh = T[k], D.get(k), R.get(k)
            if t is None:
                continue
            tf, df = c2f(t), c2f(d)
            sp = None if df is None else round(tf - df, 1)
            rows.append({"local": local.strftime("%a %Y-%m-%d %H:%M"),
                         "temp_f": round(tf, 1),
                         "dewpoint_f": None if df is None else round(df, 1),
                         "spread_f": sp, "rh_pct": rh})
            if sp is not None and (worst is None or sp < worst):
                worst = sp

        v, why = verdict(worst)
        print(f"\n=== {name} ===")
        print(f"    {note}")
        print(f"    forecast text: {'; '.join(dict.fromkeys(fog)) or 'n/a'}")
        for r in rows[: args.nights * len(NIGHT_HOURS)]:
            print(f"    {r['local']}  T {r['temp_f']:5.1f}F  Td "
                  f"{r['dewpoint_f'] if r['dewpoint_f'] is not None else '   ?':>5}F  "
                  f"spread {r['spread_f'] if r['spread_f'] is not None else '?':>5}F  "
                  f"RH {r['rh_pct'] if r['rh_pct'] is not None else '?'}%")
        print(f"    --> min spread {worst} F: {v} ({why})")
        report["sites"].append({"name": name, "lat": la, "lon": lo, "note": note,
                                "forecast_text": list(dict.fromkeys(fog)),
                                "min_spread_f": worst, "verdict": v,
                                "overnight_samples": rows})

    print("\nspread > 5 F = dry · 2-5 F = marginal · 0-2 F = the bag wets out")
    if args.json:
        os.makedirs(DATA_DIR, exist_ok=True)
        p = os.path.join(DATA_DIR, "pch_camp_condensation.json")
        json.dump(report, open(p, "w"), indent=1)
        print(f"wrote {p}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
