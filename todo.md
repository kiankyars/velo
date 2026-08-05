# 📋 Trip Preparation Checklist

---

## 🇺🇸 IMMEDIATE — Highway 1 south, leaving 5–6 Aug 2026

Route is **built and validated**: 782.4 km over 3 days, GPX in `gpx/pch_*.gpx`,
write-up in **[BIG-SUR-GPX.md](./BIG-SUR-GPX.md)**. What's left is not routing:

- `[ ]` **DECIDE the camping question.** Two clean options, no middle ground:
  - *Book it:* Limekiln on ReserveCalifornia, **800-444-7275**. California State Parks states *"There are no first-come, first-served campsites"*, so without a reservation the booked plan has no bed on night 1. Hike/bike is $5, check-in 14:00, max 2 nights, arrive on foot/bike only.
  - *Camp wild:* removes the dependency entirely and lets you stop where you like. Dispersed camping on **Los Padres National Forest** land is allowed and needs no permit — but the strip along Highway 1 is mostly state park or private ranch where it is not, and the NF land (Ventana / Silver Peak) is east of and above the highway. **Campfires are banned until 31 Jan 2027** under a Forest Order effective 4 Jun 2026; a stove is fine with a free California Campfire Permit.
- `[ ]` **Check [Caltrans QuickMap](https://quickmap.dot.ca.gov) the morning you leave.** Rocky Creek Bridge runs one-way signal control 24/7 through 31 Aug, delays to 15 min — at km 235 of day 1.
- `[ ]` **Check the Vandenberg launch schedule** for your date — CA-1 past the base can close at a few hours' notice, and the only detour is US-101 inland.
- `[ ]` **Book the bike on the train home.** Coast Starlight roll-on space out of LA Union Station is limited, sells out, and is a separate reservation from your seat.
- `[ ]` **Get a free California Campfire Permit** if you are carrying a stove.
- `[ ]` **Carry food on day 2.** It has roughly a third the on-road resupply of the other days. Fill up in Lompoc at km 226 — the next 34 km over the Santa Rosa Hills has nothing.
- `[ ]` **Loaded shakedown ride** (20–30 km): confirm the bags don't foul braking or shifting before a 297 km day.
- `[x]` **GPX built** — 3 stages (782.4 km) + 1 variant + waypoint files; legality, surface, continuity and out-and-back spurs all audited (`python3 scripts/validate_pch_routes.py` → ALL CHECKS PASS). The first draft carried 62 km of via-point spurs; those are gone and a spur check now guards against them.

---

## 🇪🇺 The Frankfurt Loop — departure **June 13, 2026** (Edmonton) / **June 21, 2026** (Europe)

---

## 💳 Financial & Travel Cards
- `[ ]` **Get a credit card that pays for Nexus** (e.g., Chase Sapphire Reserve, Capital One Venture X, Amex Platinum) to cover the application fee.
- `[ ]` **Get statement credit then cancel** (Maximize benefits of a premium travel card, secure statement credits, and cancel before the next annual fee hits).

## 🚴 Gear Preparation
- `[ ]` **Aerobars:** Purchase, mount, and test aerobars on the bike. Get comfortable in the aero position for ultra-distance riding.
- `[ ]` **Cycling shorts:** Research and purchase 2-3 pairs of premium cycling shorts/bibs (e.g., Assos, Castelli, Rapha) for 150-200 km daily rides.
- `[ ]` **Bike lights & power:** High-output front and rear lights, dynamo or 20,000mAh external battery pack for GPS watch and phone charging.
- `[ ]` **Spares & tools:** Tubeless sealant, spare tubes, tire plugs, chain tool, multi-tool, spare chain link, derailleur hanger.

## ✈️ Bookings & Logistics
- `[x]` **Edmonton travel (SFO -> YEG):** Book SFO to YEG flight for June 13th (booked, lands 11:40 p.m.).
- `[ ]` **Europe travel (YEG -> FRA & FRA -> SFO):** Book flights: YEG to FRA (June 21st) and FRA to SFO (July 13th/14th).
- `[ ]` **Uncle coordination:** Coordinate for his 80th birthday on July 13th (plan to return to Frankfurt night of July 12th). Confirm dates and luggage storage.
- `[ ]` **Bike choice decision:** Finalize whether to:
  1. *Bring own bike:* Pay KLM fees ($250 round trip) + purchase bike transport box.
  2. *Rent in Frankfurt:* Contact local shops (e.g., Fahrradstation Frankfurt).
  3. *Buy & Resell:* Locate second-hand shops or online portals (Buycycle, Kleinanzeigen) in Germany.

## 🗺️ Route & GPS Sync
- `[x]` **GPX segments:** Built all 5 segments of the Frankfurt loop (EV15/EV17/EV8/EV7/EV6) → `gpx/*.gpx` + `velo_loop_master.gpx`. 4,172.7 km; the four EuroVelo legs aligned to the **official EuroVelo GPX** (verified within metres), EV8 bespoke; XML + continuity + alignment validated. See **[ROUTE-GPX.md](./ROUTE-GPX.md)**.
- `[ ]` **Load GPX to device:** Import `gpx/velo_loop_master.gpx` (or the 5 per-segment files) into Komoot/the Polar watch and spot-check the two flagged road tunnels (Menton coast, Oberalp).
- `[ ]` **Watch configuration:** Verify Strava/Komoot integration with your Polar watch and test route guidance on a local ride.
