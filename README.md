# 🚲 Velo Journey 2026

Planning hub for Kian's ultra-distance riding. **Two trips live here now:**

| Trip | When | Distance | Where it's documented |
|------|------|---------:|----------------------|
| 🇺🇸 **Southbound Highway 1 — San Francisco → Los Angeles** | **leaving 5–6 Aug 2026** | **782.4 km / 3 days** | ⭐ **[BIG-SUR-GPX.md](./BIG-SUR-GPX.md)** |
| 🇪🇺 The Frankfurt Loop | 21 Jun – 12 Jul 2026 | 4,172.7 km / ~22 days | [ROUTE-GPX.md](./ROUTE-GPX.md) |

## 🇺🇸 The immediate one: SF → Big Sur → LA

Three riding days down the coast to Los Angeles. Built, audited and validated —
GPX in [`gpx/pch_*.gpx`](./gpx), full write-up in **[BIG-SUR-GPX.md](./BIG-SUR-GPX.md)**.

| Day | From → To | Distance | Climb |
|---|---|---:|---:|
| 1 | 426 Fell St, SF → **Limekiln SP** | **297.2 km** | +2,889 m |
| 2 | Limekiln SP → **Refugio SB** | **279.5 km** | +2,148 m |
| 3 | Refugio SB → **LA Union Station** | **205.7 km** | +611 m |

Plus one variant — `pch_day1_alt_pfeiffer.gpx`, day 1 cut to 256 km by stopping in
Big Sur Village — and the waypoint files.

**What the build found:**

- **50 out-and-back spurs wasting 62 km** in the first draft, caused by via-points
  placed on landmarks that sit off Highway 1 (Point Sur, Point Lobos, Emma Wood,
  Leo Carrillo…). The router turned off the highway, ran down an access road and
  came back out. Fixed, and now guarded by a spur check in the validator — this is
  invisible to a continuity check because the track never breaks.
- Consequently the earlier "day 1 is 326 km" figure was **wrong**; it is **297.2 km**,
  so the original 280–290 km estimate was roughly right.
- **Highway 1 is open** (reopened 14 Jan 2026) but there's a one-way signal control
  at **Rocky Creek Bridge, 24/7 through 31 Aug**, up to 15 min, at km 235 of day 1.
- **Limekiln has no first-come-first-served sites** — book it, or camp wild, which
  removes the dependency entirely. Dispersed camping on Los Padres NF land is legal
  and permit-free, but **campfires are banned until 31 Jan 2027** (stove OK with a
  free permit).

---

## 🇪🇺 The Frankfurt Loop

A **loop out of Frankfurt** through Germany, Switzerland, France, Italy and Austria.

> **Ride window:** **21 Jun → 12–13 Jul 2026** (~22 days) · back in Frankfurt the night of **12 Jul** for your **uncle's 80th (13 Jul)**
> **Flights (KLM):** SFO→YEG 13 Jun · remote work in Edmonton 13–20 Jun · **YEG→FRA 21 Jun** · **FRA→SFO 13–14 Jul**
> **Route:** **4,172.7 km** (built & measured, official EuroVelo GPX backbone) — EV15 Rhine → EV17 Rhône → **bespoke EV8** Med → EV7 Central → EV6 Danube → back to Frankfurt · **150–200 km/day**, road bike + aerobars, credit-card (hostel) style · GPX in [`gpx/`](./gpx), details in **[ROUTE-GPX.md](./ROUTE-GPX.md)**
> **Traveller:** Canadian citizen, experienced solo ultra-cyclist (2025 Rockies tour)

---

## ✅ Status of your three asks

1. **"Watch the parts video → concrete list."** ✅ Done. You pushed the transcripts to `main`; I read **"My Gear for 900 km through the Canadian Rockies"** (`g2AvZq_XQsE`) and extracted the **verbatim gear list** → **[GEAR-FROM-VIDEOS.md](./GEAR-FROM-VIDEOS.md)**.
2. **"Look through all videos/transcripts → a concise list."** ✅ Done. All **7 Cycling-playlist** transcripts analysed (gear + the lessons: ~200 km/day ceiling, no night riding, hostels > camping, bar-end mirror, cycling palsy, disc brakes, nutrition, AirTag) → same file.
3. **"Extremely deep research on every axis."** ✅ **[DEEP-RESEARCH.md](./DEEP-RESEARCH.md)** + the route work below.

---

## 📑 What's in this folder

| File | What it covers |
|------|----------------|
| **[BIG-SUR-GPX.md](./BIG-SUR-GPX.md)** | ⭐ **The SF → LA coast route.** Three riding days (782.4 km), the road-bike routing profile and why the stock one fails on this coast, the legality/surface/spur audit, the detected climbs, the water-and-food gaps, and the corrections the build forced on the plan. |
| **[GEAR-FROM-VIDEOS.md](./GEAR-FROM-VIDEOS.md)** | ⭐ Asks #1 & #2 — the **verbatim gear list** from your parts video, your own stated regrets (no bibs/tights, bad gloves, leaky pump, broken saddle bag), and the **lessons distilled from all 7 transcripts**. |
| **[CHECKLIST.md](./CHECKLIST.md)** | The **concise one-pager** to read before you leave. |
| **[PACKING-LIST.md](./PACKING-LIST.md)** | Full checkbox packing list, merging your real video kit with trip essentials (German light law, EES, insurance, Alpine cold). |
| **[ROUTE-GPX.md](./ROUTE-GPX.md)** | ⭐ **The built route.** All 5 GPX segments (EV15/EV17/EV8/EV7/EV6), **4,172.7 km**; the four EuroVelo legs built from the **official EuroVelo GPX**, EV8 bespoke; XML + continuity + alignment + tunnels/ferries validated, distances recomputed. |
| **[ITINERARY.md](./ITINERARY.md)** | The **Frankfurt Loop** day-by-day from your `trip_config.json` — 5 segments, ~4,173 km, pace reality + emergency escape-hatches. |
| **[ROUTES.md](./ROUTES.md)** | The EuroVelo building blocks (Rhine/Danube/Rhône/etc.) and fallbacks if the full loop is too much. |
| **[DEEP-RESEARCH.md](./DEEP-RESEARCH.md)** | Multi-axis dossier: EES/ETIAS, flying with a bike, German/EU trains, weather, accommodation & camping law, money (incl. Swiss CHF), connectivity, navigation, theft, insurance, nutrition, comfort, pacing, timeline. |
| **[VIDEOS.md](./VIDEOS.md)** | All your YouTube videos enumerated (Cycling + Germany Vlogs), how they were reached, and the gear video. |
| **[VELO-REPO-NOTES.md](./VELO-REPO-NOTES.md)** | Notes on your stolen **Cannondale Quick 5** (taken 5 May; you bought a replacement the same day) and recovery angle. |

---

## 🧩 How the real trip was reconstructed

- **Your repo `main`** is the source of truth: `trip_config.json` (flights, the 5 EuroVelo segments + distances, gear status), `todo.md` (open decisions), `scripts/planner.py`, and `transcripts/` (the 7 Rockies videos).
- **Your homepage journals** (`kiankyars.github.io`, read via the allowlisted `raw.githubusercontent.com`/`codeload`) corroborate it: *"Bought a bike → bike stolen → bought another"* (4–5 May), *"First draft of the Europe bike-trip route"* (15 May), the **KLM** booking saga (29 May).
- **Calendar/Slack** (work workspace) confirmed the OOO window and Alberta origin.
- **YouTube** videos enumerated via the InnerTube API; **transcripts** then supplied directly by you on `main`.

### Open decision (from your `todo.md`)
**Which bike crosses the Atlantic** is still unresolved: (1) **bring your own** road bike (KLM ~$250 round-trip + a transport box, stored at your uncle's for the loop), (2) **rent in Frankfurt**, or (3) **buy & resell** (Buycycle / Kleinanzeigen). The packing list's spares assume a **road bike with disc brakes + tubeless** (as in your videos); tell me the final bike + drivetrain speed and I'll pin exact part numbers.

---

## 📂 Repository internals (the `main` toolkit you pushed)

* `todo.md` – atomic task manager for travel, gear, cards, and logistics.
* `trip_config.json` – machine-readable metadata (flights, contacts, routes with **recomputed distances/ascent**, loop totals, gear checklist).
* `scripts/planner.py` – Python CLI: `status` (countdowns + flights + segments), `todo`, `check <term>`, `routes` (aggregate GPX distance/elevation; paths now resolve relative to the repo).
* `scripts/route_waypoints.py`, `scripts/geocode.py`, `scripts/build_routes.py`, `scripts/validate_routes.py`, `scripts/validate_route_alignment.py`, `scripts/velo_trekking.brf` – the **route builder**: define waypoints → geocode → build (official EuroVelo GPX for EV15/EV17/EV7/EV6, BRouter for EV8 + connectors) → validate. See [ROUTE-GPX.md](./ROUTE-GPX.md).
* `data/` – generated artefacts: `waypoints.json`, `route_summary.json` (per-leg distances, tunnels/ferries, network %), `validation_report.json`.
* `transcripts/` – the 2025 900-km Rockies trip transcripts (gear + pacing references).
* `gpx/` – the built loop: `ev15_rhine.gpx`, `ev17_rhone.gpx`, `ev8_med.gpx`, `ev7_central.gpx`, `ev6_danube.gpx`, plus `velo_loop_master.gpx` (whole loop) for your Polar device.

## 🤖 Agent instructions (for the next assistant)

1. **Read `todo.md` and `trip_config.json` first** to check current task status.
2. Run `python3 scripts/planner.py status` (or `todo`) for countdowns and open tasks.
3. To rebuild/verify the route: `python3 scripts/geocode.py` → `python3 scripts/build_routes.py` → `python3 scripts/validate_routes.py` → `python3 scripts/validate_route_alignment.py --compare-official` → `python3 scripts/planner.py routes` (needs internet). Details in [ROUTE-GPX.md](./ROUTE-GPX.md).
4. Update `todo.md` as tasks complete.

---

*Last updated: 2026-06-22. Earlier drafts in git history assumed an Amsterdam arrival / leisure pace before `trip_config.json` + the transcripts landed — corrected to the real Frankfurt Loop.*
