# 🗓️ Itinerary — The Frankfurt Loop (your real plan)

Rebuilt from your own **`trip_config.json`**, **`README.md`**, and **`todo.md`** on `main` — replacing my earlier (wrong) Amsterdam guess.

> **The actual plan:** a **loop starting and ending in Frankfurt** (your uncle's — his **80th birthday is 13 July**, you return to FRA the **night of 12 July**). **Ultra-distance, credit-card style, road bike + aerobars.**

## ✈️ Flights (from `trip_config.json`)
| Leg | Route | Date | Status |
|---|---|---|---|
| 1 | **SFO → YEG** (Edmonton) | **13 Jun 2026** | ✅ booked (lands ~23:40) |
| — | Remote work in Edmonton | 13–20 Jun | — |
| 2 | **YEG → FRA** (Frankfurt, direct, KLM) | **21 Jun 2026** | ⏳ pending — *book this* |
| 3 | **FRA → SFO** | **13–14 Jul 2026** | ⏳ pending — *book this* |

## 🔁 The route — 5 modular EuroVelo segments (from `trip_config.json`)
| # | Segment | EV | From → To | ~km |
|---|---|----|-----------|----:|
| 1 | **Rhine** | EV15 | Frankfurt → **Andermatt** (CH, Rhine source/Alps) | ~500 |
| 2 | **Rhône** | EV17 | Andermatt → **Mediterranean coast** (FR) | ~1,115 |
| 3 | **Mediterranean** | EV8 | Med coast → **Italy link** | ~600 |
| 4 | **Central Europe** | EV7 | Italy → **Passau** (north through/along the Alps) | ~1,200 |
| 5 | **Danube** | EV6 | Passau → **Frankfurt** | ~600 |
| | **Total** | | **Frankfurt loop** | **~4,000** |

## 📏 Reality check on pace (grounded in your own riding)
- **~4,000 km in ~22 days ≈ 180 km/day, essentially every day**, and it **crosses the Alps** (Rhine source at Andermatt; EV17 descends the Rhône; EV7 climbs back north). Your `README` target of "3,000–5,000 km, 150–200 km/day" matches this.
- Your **transcripts set your tested ceiling at ~200 km/day**, and that was with big climbs leaving you wrecked. So this loop is **at the very top of your proven range with near-zero slack** — it's a genuine ultra-endurance objective, not a touring holiday.
- **Honest recommendation:** treat the full loop as a *stretch* goal and pre-plan **2–3 escape hatches** where a **train** closes a gap so a bad-weather or bad-legs day doesn't end the trip:
  - **Andermatt ↔ Rhône valley** (Matterhorn-Gotthard / SBB) if the Alps bite.
  - **Med coast → north** (French/Italian rail) if EV8/EV7 runs long.
  - **Passau → Frankfurt** (ÖBB/DB) as a guaranteed way to be back for the **12 Jul** deadline.
- **Build in the uncle buffer:** plan to be within an easy **train hop of Frankfurt by ~10 Jul** so the 80th birthday is never at risk.

## 🗺️ Segment notes & where to resupply/sleep
- **Seg 1 — EV15 Rhine (Frankfurt → Andermatt, ~500 km):** down the Rhine to Basel, then *up* toward the Alpine source. Mostly flat until the final climb into the Alps. Towns dense → easy hostels/Gasthöfe. *Switzerland = CHF, not euros, and pricey — carry a card + some francs.*
- **Seg 2 — EV17 Rhône (Andermatt → Mediterranean, ~1,115 km):** the big one. Furka/Rhône-glacier start, long descent through the Valais (Brig, Sion, Martigny), Lake Geneva, then down the French Rhône (Lyon, Avignon, Arles) to the sea. Largely downhill-trending after the top → your fastest segment.
- **Seg 3 — EV8 Mediterranean (~600 km):** coastal France → Italy (Riviera). Hotter, busier, more climbing on the headlands; hydrate hard (your heat/electrolyte playbook).
- **Seg 4 — EV7 Central Europe (Italy → Passau, ~1,200 km):** north back across/around the Alps toward Austria/Bavaria — the second serious climbing block. Hardest re-entry leg; this is the one to shorten with a train if you're behind.
- **Seg 5 — EV6 Danube (Passau → Frankfurt, ~600 km):** gentle, famous, well-signed Danube path then the link back to Frankfurt — a fitting easy-ish finish before the birthday.

## 🧳 Bookend logistics
- **Bike:** decision still open in `todo.md` — **bring own** (KLM ~$250 round-trip + transport box; YEG→FRA is direct, good for the bike) / **rent in Frankfurt** / **buy & resell** (Buycycle, Kleinanzeigen). If bringing own, box it for YEG→FRA and **store the box at your uncle's** in Frankfurt for the return (this is *why* a Frankfurt loop is logistically clean — start = finish = box storage).
- **Uncle in Frankfurt:** confirm dates + luggage/box storage; back in FRA night of **12 Jul** for the **13 Jul** 80th.
- **EES** biometrics on arrival at FRA (allow time); **ETIAS not required** yet. (Details in [DEEP-RESEARCH.md](./DEEP-RESEARCH.md#-entry-borders--paperwork-canadian-citizen-2026).)

## 🌍 "Germany and elsewhere in Europe" — delivered in full
This loop touches **Germany → Switzerland → France → (Italy) → Austria → Germany** — far more of Europe than a single-river route, which is exactly the brief.

---

*Built from `trip_config.json` (flights, segments, distances), `README.md` (loop concept), and `todo.md` (open decisions) on `main`; pace calibrated to your Rockies transcripts. The segment EV-code mapping is your own modular plan — confirm each GPX in `gpx/` with `python3 scripts/planner.py routes`, and verify daily stages against live lodging before booking.*
