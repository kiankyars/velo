# 🔎 What the `velo` repo actually is — and recovery next-steps

When I "looked through the Velo directory," the `main` branch turned out to be a software project, **not** a trip plan. Documenting it here so the picture is complete, and adding the high-leverage recovery actions your own README points to.

## The project: `Velo Recovery Watch`

A local-first tool you built to **recover a stolen bike** by monitoring marketplaces, scoring listings against your bike profile, and exporting evidence packets.

**On `main` (`origin/main`):**
- `velo_watch/` — Python package (`browserbase_scan.py`, `matching.py`, `vision.py`, `dashboard.py`, `db.py`, `ingest.py`, …) + tests
- `config/` — `bike_profile.yml`, `bikes.json`, `watchlist.yml`
- `data/candidates.sqlite` — **278 scraped listings**; `data/review_sheet.html`; scan logs
- `captures/` — **1,666 marketplace screenshots** (OfferUp/Craigslist/Facebook), May 2026 onward
- `launchd/…plist` — a LaunchAgent to auto-scan every 6 hours
- `bike.jpg` + `vélo.jpg` — reference photos of the bike

## The bike (from `config/bike_profile.yml` + the photos)

| Field | Value |
|---|---|
| Bike | **2021 Cannondale Quick 5** (hybrid / fitness) |
| Finish | Matte **black** with **white** accents, aluminium frame, **Large**, 700c |
| Drivetrain | Shimano 2× (front double + rear cassette) — *per photos* |
| Brakes | Mechanical **disc** brakes — *per photos* |
| Tyres | Schwalbe Spicer 700c — *per photos* |
| Accessories | water-bottle holder, **kickstand**, flat bar w/ bar-end grips + bell |
| **Stolen** | **2026-05-05 14:27**, 426 Fell St, San Francisco 94102 ("in our garage the day I bought it") |
| Serial | **Unspecified** ⚠️ |
| Project 529 | https://project529.com/garage/bikes/pannier-crank-aero-helmet/ |
| Bike Index | *(empty)* ⚠️ |
| Police report # | *(empty)* ⚠️ |
| Also watching | **Trek Fuel EX 7** (mountain) |

## Candidate database — current state (snapshot)

- **278 candidates**, **all status `new`** (none triaged yet): Craigslist 117 · Facebook 103 · OfferUp 58.
- Matched to: Cannondale Quick 5 = 244 · Trek Fuel EX 7 = 34.
- Highest scores are **Trek Fuel EX 7** exact-text matches (86) — but those are *other people's* Trek listings, not necessarily yours.
- **No exact "Cannondale Quick 5" listing has surfaced yet.** Closest Cannondale hits are different models (Quick CX 3, Quick 6, Trail 5/7, Bad Boy, CAAD). The thief's relisting hasn't appeared in the watch as of this data.

## 🎯 High-leverage recovery next-steps (gaps in your own profile)

1. **Get the serial number.** It's `Unspecified` — the single biggest recovery lever. You bought the bike right before it was stolen, so the **purchase receipt / original seller listing** likely has it. Add it to `bike_profile.yml`.
2. **File / record the SFPD report number** (currently empty). Required for recovery hand-off *and* any insurance/theft claim. Add it to the profile.
3. **Create a Bike Index listing** (currently empty). It's the registry pawn shops and buyers actually check — add the URL to the profile. (You already have Project 529 set up — keep it active.)
4. **Triage the 278 candidates.** Open the dashboard (`uv run velo-watch serve` → http://127.0.0.1:8765) and mark/dismiss. Prioritise **Cannondale Quick-series, Large, matte black, in SF, low price** (theft quick-flips are often $150–400).
5. **Turn on OCR/vision** (`uv sync --extra vision` + `tesseract`) — the scorer is currently flagging "OCR unavailable," so it's matching on titles only and missing detail in listing photos/screenshots.
6. **Keep the twice-daily scan running** (the LaunchAgent) through the summer — relistings often appear weeks later.

> ⚠️ Safety (from your own README): screenshot listings before any contact; **don't meet a seller alone** — coordinate with SFPD non-emergency if there's a likely match.

## How this connects to the Europe trip

Your main bike was stolen **~5 weeks before** the 22 Jun departure. So the **trip bike is an open question** — recovered, replaced, or rented? That's the one input that sharpens the packing list (rim vs disc spares, whether you fly with your own bike at all, etc.). See [PACKING-LIST.md](./PACKING-LIST.md#-your-actual-bike-from-your-own-records).

*Repo contents read directly from `origin/main` of `kiankyars/velo` (the one repo in my allowed GitHub scope). Bike spec from `config/bike_profile.yml` + `bike.jpg`/`vélo.jpg`; candidate stats from `data/candidates.sqlite`.*
