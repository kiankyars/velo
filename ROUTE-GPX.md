# 🛰️ Frankfurt Loop — the built GPX (route, validation, distances)

This is the routing deliverable: **five continuous GPX tracks** that close a loop
out of Mittelbuchen (Hanau, Frankfurt) and back, plus a combined master track,
all routed on **real OpenStreetMap cycle infrastructure** with **no trains, no
motorways, no ferries**. Everything here is generated and checked by scripts in
[`scripts/`](./scripts) so it can be reproduced and re-verified.

> **Loop total: `4,018.7 km`, `≈ 39,500 m` of climbing, 5 segments.**
> Backbone = official **EuroVelo** corridors (EV15 → EV17 → EV7 → EV6); the
> Mediterranean leg is the **bespoke EV8** that was requested; the seams are
> joined by routed connectors. Every segment joins the next to within **0.0 m**
> and the loop closes on itself to within **0.0 m**.

---

## The segments

| # | File | EV | From → To | Distance | Climb | On OSM cycle-network |
|---|------|----|-----------|---------:|------:|---------------------:|
| 1 | [`gpx/ev15_rhine.gpx`](./gpx/ev15_rhine.gpx) | **EV15** | Mittelbuchen → Mainz → Basel → **Andermatt** | **843.9 km** | 7,756 m | 88% (28% EV-signed) |
| 2 | [`gpx/ev17_rhone.gpx`](./gpx/ev17_rhone.gpx) | **EV17** | Andermatt → Furka → Rhône → **Port-Saint-Louis** | **846.6 km** | 8,450 m | 80% (45% EV-signed) |
| 3 | [`gpx/ev8_med.gpx`](./gpx/ev8_med.gpx) | **EV8\*** | Med → Manosque → Draguignan → Liguria → Turchino → **Piacenza** | **874.5 km** | 12,521 m | 50% (bespoke) |
| 4 | [`gpx/ev7_central.gpx`](./gpx/ev7_central.gpx) | **EV7** | Piacenza → Mantova → Brenner → Innsbruck → **Passau** | **764.8 km** | 6,369 m | 90% (39% EV-signed) |
| 5 | [`gpx/ev6_danube.gpx`](./gpx/ev6_danube.gpx) | **EV6** | Passau → Regensburg → Nürnberg → Würzburg → **Mittelbuchen** | **688.9 km** | 4,413 m | 84% (39% EV-signed) |
| | [`gpx/velo_loop_master.gpx`](./gpx/velo_loop_master.gpx) | — | the whole loop in one file (5 tracks) | **4,018.7 km** | 39,509 m | — |

*EV8\* = a **custom** Mediterranean route, not the signed EuroVelo 8; see below.*
*"On cycle-network" = share of the leg whose OSM ways carry a
`route_bicycle_icn/ncn/rcn/lcn` tag — i.e. an international/national/regional
signed cycle route. "EV-signed" is the `icn` (international) share specifically.*

```
Mittelbuchen ─EV15─▶ Andermatt ─EV17─▶ Med (Port-St-Louis)
     ▲                                        │
     │                                       EV8*  (Manosque ▸ Draguignan ▸
    EV6                                        │    Ligurian coast ▸ Turchino)
     │                                         ▼
  Passau ◀────────────── EV7 ────────────── Piacenza
```

## The bespoke EV8 (Mediterranean)

The standard EuroVelo 8 hugs the busy Côte d'Azur. The requested route instead
goes **inland through Provence, then rejoins the coast in Liguria and climbs
away from the Genoa seafront over a pass**:

> Port-Saint-Louis (EV17 finish) → Arles → Salon-de-Provence → Aix-en-Provence →
> **Manosque** → Gréoux-les-Bains → Riez → Quinson → Aups → Salernes →
> **Draguignan** → Le Muy → Fréjus *(back to the coast)* → Cannes → Antibes →
> Nice → Monaco → Menton → **Ventimiglia** → Sanremo → Imperia → Albenga →
> Savona → Varazze → Genova-Voltri → Mele → **Passo del Turchino** → Masone →
> Ovada → Novi Ligure → Tortona → Voghera → **Piacenza**.

The Ligurian stretch deliberately follows the **Pista Ciclabile del Ponente
Ligure** (the Sanremo–Imperia–Albenga seaside cycleway built on the old coastal
railway), which is why the leg passes through a string of lit former-railway
tunnels (see validation). The **Passo del Turchino** (532 m) is the classic
Apennine crossing that takes you off the coast and down to the Po plain.

## Connectors (routed, not signed EuroVelo)

These are the bits that aren't on a single EuroVelo route and were routed to
stitch the backbone together — all on cycle-friendly roads/paths:

- **Mittelbuchen → Mainz** — down the Main (Hanau → Frankfurt → Rüsselsheim) to
  join EV15. *(~40 km, flat.)*
- **Piacenza → Mantova** — across the Po plain (via Cremona) to pick up the EV7
  corridor.
- **Innsbruck → Passau** — the **Inn cycleway** (Kufstein → Rosenheim → Mühldorf
  → Braunau → Schärding), since EV7 itself does not run to Passau.
- **Kelheim → Nürnberg → Bamberg → Mittelbuchen** — leave the Danube at Kelheim,
  follow the **Altmühl / Main-Donau canal** to Nürnberg, then the **Main
  cycleway** (Bamberg → Würzburg → Aschaffenburg → Hanau) home.

---

## Validation results

Run independently from the saved GPX by
[`scripts/validate_routes.py`](./scripts/validate_routes.py):

| Check | Result |
|-------|--------|
| **XML well-formed** (GPX 1.1, parses cleanly) | ✅ all 5 files |
| **Continuity within each track** (largest jump) | ✅ ≤ 150 m everywhere |
| **Seam gaps** (end of one leg → start of next) | ✅ 0.0 m × 4 |
| **Loop closure** (EV6 finish → EV15 start) | ✅ 0.0 m |
| **Motorways / motorroads** | ✅ 0.0 km |
| **Trunk roads** | 0.07 km (a couple of bridge/junction crossings) |
| **Active railway / train** | ✅ 0.0 km (the `railway=abandoned` hits are rail-*trails*) |
| **Ferries** | ✅ 0.0 km (every water crossing uses a bridge) |
| **Tunnels** | 21.6 km total; **none prohibit bikes** |

### About the tunnels
Most tunnel distance is **dedicated cycleway** — chiefly the old-railway tunnels
of the Ligurian seaside cycle path (legal, lit, scenic). Only **7.8 km** runs
through shared road tunnels, none of which are tagged `bicycle=no` (the router
refuses bike-prohibited tunnels). The handful worth knowing about before you
ride them:

| Where | Length | Road type | Note |
|-------|-------:|-----------|------|
| Menton ↔ Ventimiglia coast (43.7845, 7.5396) | 1,135 m | primary | busy border-coast tunnel; daylight + lights advised |
| Oberalp approach near Andermatt (46.6599, 8.6566) | 733 m | primary | mountain avalanche gallery on EV15 |
| Ligurian coast near Borghetto (43.9571, 8.1730) | 575 m | primary | parallel old road exists if preferred |

Full machine-readable detail (every tunnel/ferry/trunk hit with coordinates and
OSM tags) is in [`data/route_summary.json`](./data/route_summary.json); the
pass/fail report is in [`data/validation_report.json`](./data/validation_report.json).

---

## How it was built (and how to regenerate)

1. **Waypoints** — ordered EuroVelo corridor towns + the bespoke EV8 chain +
   connectors are defined in
   [`scripts/route_waypoints.py`](./scripts/route_waypoints.py) and geocoded with
   [`scripts/geocode.py`](./scripts/geocode.py) (Photon/OSM, hand-checked
   overrides for mountain passes and a few mis-geocoded Italian cities) →
   [`data/waypoints.json`](./data/waypoints.json).
2. **Routing** — [`scripts/build_routes.py`](./scripts/build_routes.py) routes
   each segment through its waypoints with **BRouter** on OpenStreetMap, using a
   copy of BRouter's stock **`trekking`** profile
   ([`scripts/velo_trekking.brf`](./scripts/velo_trekking.brf)) with
   `processUnusedTags = true` so every OSM tag (tunnel, bridge, ferry, motorroad,
   railway, cycle-network) is returned and can be audited. The profile avoids
   motorways and follows signed cycle routes, so feeding it the real EuroVelo
   towns reproduces the signed line (confirmed by the high `icn/ncn` share above).
   Tracks are densified to ≤ 150 m spacing for clean device rendering.
3. **Validation** — [`scripts/validate_routes.py`](./scripts/validate_routes.py)
   re-reads the GPX from disk and re-checks XML, continuity, seams and distance.

```bash
python3 scripts/geocode.py        # data/waypoints.json   (internet)
python3 scripts/build_routes.py   # gpx/*.gpx + data/route_summary.json (internet)
python3 scripts/validate_routes.py
python3 scripts/planner.py routes # aggregate distance/elevation
```

### Caveats
- The backbone follows the EuroVelo **corridor** on current OSM cycle
  infrastructure; it is faithful to the signed route but is not a byte-copy of
  eurovelo.com's own GPX (which isn't cleanly downloadable, and whose OSM
  relations carry many bank/variant/ferry options that don't stitch into one
  clean line).
- Elevation is BRouter's SRTM-based data; treat climb totals as ±5–10%.
- Re-confirm daily stages, the two notable road tunnels, and Alpine pass opening
  (Furka/Oberalp open ~June) against live conditions before riding.
