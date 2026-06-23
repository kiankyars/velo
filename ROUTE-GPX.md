# 🛰️ Frankfurt Loop — the built GPX (route, validation, distances)

This is the routing deliverable: **five continuous GPX tracks** that close a loop
out of Mittelbuchen (Hanau, Frankfurt) and back, plus a combined master track.
The four EuroVelo legs (EV15/EV17/EV7/EV6) are built from the **official
eurovelo.com GPX**; BRouter/OSM routing is used only for the bespoke EV8 and for
the connectors that aren't part of any signed EuroVelo route. Everything here is
generated and checked by scripts in [`scripts/`](./scripts) so it can be
reproduced and re-verified.

> **Loop total: `4,172.7 km`, `≈ 42,600 m` of climbing, 5 segments.**
> Backbone = official **EuroVelo** GPX (EV15 → EV17 → EV7 → EV6); the
> Mediterranean leg is the **bespoke EV8** that was requested; the seams are
> joined by routed connectors. Every segment joins the next to within **0.0 m**
> and the loop closes on itself to within **0.0 m**.

---

## The segments

| # | File | EV | From → To | Distance | Climb | On cycle-network |
|---|------|----|-----------|---------:|------:|-----------------:|
| 1 | [`gpx/ev15_rhine.gpx`](./gpx/ev15_rhine.gpx) | **EV15** | Mittelbuchen → Mainz → Basel → **Andermatt** | **874.7 km** | 9,206 m | 99% (94% EV-signed) |
| 2 | [`gpx/ev17_rhone.gpx`](./gpx/ev17_rhone.gpx) | **EV17** | Andermatt → Furka → Rhône → **Port-Saint-Louis** | **947.4 km** | 9,605 m | 100% (100% EV-signed) |
| 3 | [`gpx/ev8_med.gpx`](./gpx/ev8_med.gpx) | **EV8\*** | Med → Manosque → Draguignan → Liguria → Turchino → **Piacenza** | **874.5 km** | 12,521 m | 50% (bespoke) |
| 4 | [`gpx/ev7_central.gpx`](./gpx/ev7_central.gpx) | **EV7** | Piacenza → Mantua → Adige → Bolzano → Brenner → **Passau** | **765.5 km** | 6,676 m | 92% (55% EV-signed) |
| 5 | [`gpx/ev6_danube.gpx`](./gpx/ev6_danube.gpx) | **EV6** | Passau → Regensburg → Nürnberg → Würzburg → **Mittelbuchen** | **710.6 km** | 4,572 m | 92% (57% EV-signed) |
| | [`gpx/velo_loop_master.gpx`](./gpx/velo_loop_master.gpx) | — | the whole loop in one file (5 tracks) | **4,172.7 km** | ~42,600 m | — |

*EV8\* = a **custom** Mediterranean route, not the signed EuroVelo 8; see below.*
*"On cycle-network" = share of the leg on an official EuroVelo GPX backbone or on
OSM ways tagged `route_bicycle_icn/ncn/rcn/lcn`. "EV-signed" is the international
(`icn`) / official-EuroVelo share specifically — EV17 is 100% because the entire
leg is the official EuroVelo 17 GPX.*

```
Mittelbuchen ─EV15─▶ Andermatt ─EV17─▶ Med (Port-St-Louis)
     ▲                                        │
     │                                       EV8*  (Manosque ▸ Draguignan ▸
    EV6                                        │    Ligurian coast ▸ Turchino)
     │                                         ▼
  Passau ◀────────────── EV7 ────────────── Piacenza
```

## How each leg is sourced

| Leg | Official EuroVelo GPX | BRouter connector(s) |
|-----|-----------------------|----------------------|
| EV15 | Mainz → Andermatt (route 36) | Mittelbuchen → Mainz |
| EV17 | **whole leg** Andermatt → Port-Saint-Louis (route 37) | — (just seam links) |
| EV7 | Mantua → Adige → Bolzano (route 30, tracks 95–98) | Piacenza → Mantua; Bolzano → Brenner → Inn → Passau |
| EV6 | Passau → Regensburg → Kelheim (route 29, tracks 79–83) | Kelheim → Main-Donau canal → Main → Mittelbuchen |
| EV8 | — (no official EV8 variant exists for this route) | whole leg (bespoke, see below) |

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

- **Mittelbuchen → Mainz** — down the Main (Hanau → Frankfurt → Rüsselsheim) to
  join EV15. *(~40 km, flat.)*
- **Piacenza → Mantua** — across the Po plain (via Cremona) to pick up the
  official EV7 line on the Adige.
- **Bolzano → Passau** — over the **Brenner** and down the **Inn cycleway**
  (Bressanone, Innsbruck, Kufstein, Rosenheim, Braunau, Schärding). EV7 itself
  leaves Bolzano *east* through the Pustertal, so the run to Passau is a routed
  connector, not EV7.
- **Kelheim → Mittelbuchen** — leave the Danube at Kelheim, follow the **Altmühl /
  Main-Donau canal** to Nürnberg, then the **Main cycleway** (Bamberg → Würzburg →
  Aschaffenburg → Hanau) home.
- **Seam links** — short BRouter hops pin each leg exactly to the next at
  Andermatt, Port-Saint-Louis, Piacenza, Passau and Mittelbuchen (0.0 m seams).

---

## Validation results

Re-read independently from the saved GPX by
[`scripts/validate_routes.py`](./scripts/validate_routes.py):

| Check | Result |
|-------|--------|
| **XML well-formed** (GPX 1.1, parses cleanly) | ✅ all 5 files |
| **Continuity within each track** (largest jump) | ✅ ≤ 150 m everywhere |
| **Seam gaps** (end of one leg → start of next) | ✅ 0.0 m × 4 |
| **Loop closure** (EV6 finish → EV15 start) | ✅ 0.0 m |
| **Motorways / motorroads** | ✅ 0.0 km |
| **Trunk roads** | ✅ 0.0 km |
| **Active railway / train** | ✅ 0.0 km (the `railway=abandoned` hits are rail-*trails*) |
| **Ferries** | ✅ 0.0 km (every water crossing uses a bridge) |
| **Tunnels** | 17.3 km total; **none prohibit bikes** on the BRouter-tagged portions |

And the official-alignment check
([`scripts/validate_route_alignment.py --compare-official`](./scripts/validate_route_alignment.py)),
which measures how far each backbone leg sits from the official EuroVelo line:

| Leg | Max drift from official | 
|-----|------------------------:|
| EV15 (Mainz–Maxau stage) | **1.9 m** |
| EV17 (whole leg) | **17 m** |
| EV7 (Mantua–Bolzano) | **24 m** |
| EV6 (Passau–Kelheim) | **0 m** |

EV15 also passes the Rhine checkpoints (Mainz, Worms, Speyer, Maxau) and stays
**2.2 km clear of the inland Osthofen** short-cut the first generated route took.

### About the tunnels
Almost all tunnel distance is **dedicated cycleway** — chiefly the old-railway
tunnels of the Ligurian seaside cycle path (legal, lit, scenic). Only **5.0 km**
runs through shared road tunnels, all on the bespoke EV8 leg and none tagged
`bicycle=no` (the router refuses bike-prohibited tunnels). The two worth knowing
before you ride them:

| Where | Length | Road type | Note |
|-------|-------:|-----------|------|
| Menton ↔ Ventimiglia coast (43.7845, 7.5396) | 1,135 m | primary | busy border-coast tunnel; daylight + lights advised |
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
2. **Routing** — [`scripts/build_routes.py`](./scripts/build_routes.py) downloads
   the official EuroVelo GPX for EV15/EV17/EV7/EV6 from eurovelo.com, selects the
   main-line tracks, stitches them, and pins the ends to the seam waypoints. The
   bespoke EV8 and every connector are routed with **BRouter** on OpenStreetMap
   using a copy of the stock **`trekking`** profile
   ([`scripts/velo_trekking.brf`](./scripts/velo_trekking.brf)) with
   `processUnusedTags = true`, so OSM tags (tunnel, bridge, ferry, motorroad,
   railway, cycle-network) are returned and can be audited. Tracks are densified
   to ≤ 150 m spacing for clean device rendering.
3. **Validation** — [`scripts/validate_routes.py`](./scripts/validate_routes.py)
   re-reads the GPX and re-checks XML, continuity, seams and distance;
   [`scripts/validate_route_alignment.py`](./scripts/validate_route_alignment.py)
   (`--compare-official`) checks every backbone leg against the official EuroVelo
   GPX and confirms EV15 avoids Osthofen.

```bash
python3 scripts/geocode.py        # data/waypoints.json   (internet)
python3 scripts/build_routes.py   # gpx/*.gpx + data/route_summary.json (internet)
python3 scripts/validate_routes.py
python3 scripts/validate_route_alignment.py --compare-official
python3 scripts/planner.py routes # aggregate distance/elevation
```

### Caveats
- The four EuroVelo legs use EuroVelo's own GPX geometry (verified to within a
  few metres above). The bespoke EV8 and the connectors are BRouter routes on OSM
  cycle infrastructure.
- Tunnel/ferry/motorway tag auditing comes from BRouter output, so it covers the
  bespoke EV8 and the connectors. The official EuroVelo backbones are
  alignment- and continuity-checked but their GPX carries no OSM way tags; as
  signed cycle routes, any tunnels on them are bike-legal by definition.
- Elevation is BRouter/EuroVelo elevation data; treat climb totals as ±5–10%.
- Re-confirm daily stages, the two notable road tunnels, and Alpine pass opening
  (Furka/Oberalp open ~June) against live conditions before riding.
