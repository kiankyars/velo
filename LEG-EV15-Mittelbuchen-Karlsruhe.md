> **Update (2026-06-23):** this Mainz→Karlsruhe clip is now the opening stretch of the **full** `gpx/ev15_rhine.gpx` (Mittelbuchen → Andermatt, 843.9 km) built and validated in **[ROUTE-GPX.md](./ROUTE-GPX.md)**. This page is kept for the detailed waypoint table + figure of the first leg.

# 📐 EV15 Leg — Mittelbuchen → Karlsruhe (mapped from the GPX)

Computed from the **official EuroVelo 15 (Rhine) GPX track** (26,639 pts, Andermatt→Hook of Holland, with elevation), clipped to your leg. *(EuroVelo.com itself is blocked from this sandbox, so I sourced the identical EV15 track from a public GitHub mirror — `FabriziodelaRusta/eurovelo_gpx` / `VeloFactory/VeloMap` — verified to match the EV15 extent.)*

## Headline figures

| Part | Distance | Elevation | Notes |
|---|---:|---|---|
| **Connector:** Mittelbuchen (Hanau) → Mainz (join EV15) | **~45–50 km** | ~flat | Off-route: down the **Main** (Hanau → Frankfurt → Mainz). Straight-line is 53 km; by river path ≈ 45–50 km |
| **EV15 on-route:** Mainz → Karlsruhe (Maxau) | **159.8 km** | **flat** (~80–110 m) | Riverside, paved, traffic-light. *The GPX shows +785/−760 m cumulative, but that's GPS/elevation-sensor noise on flat ground — net change ≈ 0* |
| **TOTAL Mittelbuchen → Karlsruhe** | **≈ 205–210 km** | flat | A 1-day ultra ride for you, or a relaxed 2 days |

> ⚠️ **Mittelbuchen is ~50 km east of the Rhine**, so it is *not* on EV15. You first ride a connector to the river (Mainz is the natural join), then follow EV15 south. The 159.8 km figure is the pure EV15 portion; budget ~205–210 km door-to-door.

## Waypoints & cumulative distance (along the EV15 clip)

| Town | km from Mainz | On-route |
|---|---:|---|
| **Mainz** (join the Rhine) | 0.0 | 0.5 km |
| Oppenheim | 21.3 | 0.7 km |
| **Worms** | 56.1 | 0.7 km |
| Ludwigshafen / Mannheim | 86.1 | 3.5 km |
| **Speyer** (Romanesque cathedral) | 109.2 | 0.3 km |
| Germersheim | 130.7 | 0.4 km |
| **Karlsruhe (Maxau / Rhine bridge)** | 159.8 | 0.1 km |

*Karlsruhe city centre sits ~8 km east of the Rhine; EV15 passes the river at **Maxau**. Add a short hop east into the city.*

## Files
- **GPX (ready for Komoot/Polar):** [`gpx/ev15_mittelbuchen-mainz_to_karlsruhe.gpx`](./gpx/ev15_mittelbuchen-mainz_to_karlsruhe.gpx) — the 159.8 km Mainz→Karlsruhe EV15 clip (1,769 points, with elevation).
- **Figure (map + elevation profile):** [`gpx/ev15_mittelbuchen_karlsruhe.png`](./gpx/ev15_mittelbuchen_karlsruhe.png)

## How this fits the trip
This is the **opening stretch of Segment 1 (EV15 Rhine)** of your Frankfurt Loop ([ITINERARY.md](./ITINERARY.md)). From Karlsruhe, EV15 continues south to **Strasbourg → Basel → the Alpine Rhine toward Andermatt**. Re-run `python3 scripts/planner.py routes` after dropping the GPX into `gpx/` to fold it into your aggregate stats.

*Method: official EV15 GPX → nearest-point clip between Mainz (50.000, 8.271) and Karlsruhe/Maxau (49.037, 8.301) → haversine distance + elevation integration. The ~50 km connector is estimated (routing APIs are blocked here); confirm it in Komoot/cycle.travel.*
