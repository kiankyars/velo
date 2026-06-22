# 🚲 Velo Journey 2026: SFO → Edmonton → Europe

Welcome to the agent-native repository for planning and executing the 2026 ultra-distance bike tour.

---

## 📅 Trip Timeline & Overview

### 1. Leg 1: Remote Work in Edmonton 🇨🇦
* **Dates:** June 13, 2026 – June 20, 2026
* **Details:** Working remotely from Edmonton (no PTO required).

### 2. Leg 2: Transatlantic Bike Tour (The Frankfurt Loop) 🇪🇺
* **Dates:** June 21, 2026 – July 13, 2026
* **Format:** Multi-city KLM booking starting/ending in Frankfurt (FRA).
* **Target:** ~3,000 to 5,000 km in 22 days (averaging 150–200 km/day).

```
[San Francisco] ──(June 13)──> [Edmonton] ──(June 20)──> [SFO Layover]
                                                             │
                                                         (June 21)
                                                             ▼
[San Francisco] <──(July 13)── [Frankfurt Loop (EV15/17/8/7/6)]
```

---

## 🗺️ Route Itinerary (Proposed)

We are using a **modular segment routing approach** instead of pre-generating fixed daily routes:
* **Segment 1 (EV15 - Rhine Route):** Frankfurt → Andermatt (Switzerland). Climbing up the Rhine source.
* **Segment 2 (EV17 - Rhône Route):** Andermatt → Mediterranean Coast (France). Scenic downhills.
* **Segment 3 (EV8 - Med Route):** French Riviera east to Italy.
* **Segment 4 (EV7 - Central Europe Route):** Italy heading north through the Alps.
* **Segment 5 (EV6 / Passau Link):** Connecting through Austria/Germany and heading back to Frankfurt.

---

## 📂 Repository Structure

* `todo.md` – Unified atomic task manager for travel, gear, cards, and logistics.
* `trip_config.json` – Machine-readable metadata (flights, contacts, routes, gear checklist).
* `scripts/` – Python CLI automation helpers for routes, checklist tracking, and stats.
* `transcripts/` – Transcripts of the 2025 900-km Rockies trip (5-day tour) for gear and pacing references.
* `gpx/` – Modular GPX route segments synced to your Polar navigation device.

---

## 🤖 Agent Instructions

If you are an AI assistant helping Kian prepare for this trip:
1. **Always read** [todo.md](file:///Users/kian/Developer/v%C3%A9lo/todo.md) and [trip_config.json](file:///Users/kian/Developer/v%C3%A9lo/trip_config.json) first to check current task status.
2. Use the CLI tool `python3 scripts/planner.py` to view task categories or print countdown status.
3. Help Kian process GPX files by loading them into the `gpx/` folder and running `python3 scripts/planner.py routes` to calculate aggregate statistics (distance, elevations).
4. Update `todo.md` directly as tasks are completed.
