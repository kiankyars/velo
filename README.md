# Velo Recovery Watch

Local tooling for watching stolen-bike marketplace candidates, scoring them
against your bike profile, and exporting evidence packets.

The system is intentionally local-first. It stores candidates in SQLite, accepts
alert emails, URLs, screenshots, and listing-photo crops, and runs optional OCR
and image similarity when Pillow/Tesseract are installed.

## Quick Start

```bash
uv run velo-watch init
uv run velo-watch serve
```

Then open http://127.0.0.1:8765.

The three canonical marketplace searches live in `config/watchlist.yml`:

- OfferUp: https://offerup.com/search?q=cannondale
- Craigslist: https://sfbay.craigslist.org/search/bia?query=cannondale#search=2~gallery~0
- Facebook Marketplace: https://www.facebook.com/marketplace/sanfrancisco/search/?query=cannondale

## Browserbase Scan

Put Browserbase credentials in `~/.env`:

```bash
BROWSERBASE_API_KEY=...
# Optional:
BROWSERBASE_PROJECT_ID=...
```

Then run:

```bash
uv run velo-watch scan
```

`scan` loads `~/.env`, opens each saved marketplace search in one Browserbase
session, extracts visible listing links, captures a search-page screenshot,
records listing text, scores each listing, and adds or updates candidates in the
local dashboard. By default it keeps only listings posted after `2026-05-04`,
checks the top 8 listings per search, and captures a per-listing card image.
Tune these in `~/.env` with `VELO_POSTED_AFTER_DATE`, `VELO_SCAN_WAIT_MS`,
`VELO_DETAIL_WAIT_MS`, `VELO_DETAIL_TIMEOUT_MS`, and `VELO_MAX_LISTINGS_PER_SEARCH`.

## Candidate Ingest

The CLI has one ingest command:

```bash
uv run velo-watch add "https://sfbay.craigslist.org/..."
uv run velo-watch add ~/Downloads/craigslist-alert.eml
uv run velo-watch add ~/Desktop/listing-screenshot.png
uv run velo-watch add ~/Desktop/listing-notes.txt
```

Use the dashboard for editing status, notes, or detailed listing fields.

Other commands:

```bash
uv run velo-watch scan
uv run velo-watch list
uv run velo-watch export 1
uv run velo-watch delete 1
```

## Automation

Install the LaunchAgent to run a scan every 6 hours:

```bash
mkdir -p ~/Library/LaunchAgents
cp launchd/com.kian.velo-watch.scan.plist ~/Library/LaunchAgents/
launchctl unload ~/Library/LaunchAgents/com.kian.velo-watch.scan.plist 2>/dev/null || true
launchctl load ~/Library/LaunchAgents/com.kian.velo-watch.scan.plist
```

Logs go to `data/logs/scan.log`.

## Optional Vision/OCR

Install optional dependencies if you want screenshot OCR and image hashing:

```bash
uv sync --extra vision
```

OCR also needs the `tesseract` binary installed on the machine. Without these
dependencies, the app still works from manually pasted text, copied URLs, and
attached screenshots.

## High-Agency Recovery Checklist

- File the SFPD report and add the report number to `config/bike_profile.yml`.
- Create a Bike Index listing and add its URL to `config/bike_profile.yml`.
- Keep Project 529 active, and consider Project 529 Detective if you want paid
  marketplace monitoring.
- Screenshot candidate listings before any contact.
- Do not meet a seller alone; coordinate with SFPD/non-emergency if there is a
  likely match.
