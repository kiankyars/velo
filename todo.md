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
- `[ ]` **⚠️ The bag is 2–6 °F short at Limekiln — this is a correction.** The **Marmot NanoWave 45** tests at **EN/ISO Comfort 56 °F, Lower Limit 49 °F**, so even the "45" on the label is optimistic. Limekiln's lows of 54/53/51/50 °F are **below the comfort rating every night**, and the coldest is 1 °F above the *limit* rating — which EN defines as "curled up, on the edge of shivering." An earlier version of this list said the bag had 5–9 °F of margin; it does not. Pfeiffer (56–62 °F) and Refugio (61–62 °F) are both fine.
- `[ ]` **Both saturation nights are measured, not guessed** (`python3 scripts/check_camp_dewpoint.py`). Limekiln spread **0–2 °F**, RH 93–99%. Refugio spread **0–3 °F**, RH 91–100% — saturated too, despite its forecast text saying only "patchy fog." That's two consecutive wetting nights with no dry-out between. Good news: the bag is **synthetic** (Spirafil), which keeps loft damp and dries fast, so this is an inconvenience rather than a lost night.
- `[ ]` **Strongest single move: take Pfeiffer instead of Limekiln for night 1.** Spread **11–21 °F**, RH 48–68%, lows 56–62 °F — a different airmass, inland of the marine layer. It is the **only** night on the itinerary where the bag is at its comfort rating *and* the air isn't saturated. Fixes the cold and the wet together, costs 41 km off day 1 (`pch_day1_alt_pfeiffer.gpx`, 256 km) and no purchase.
- `[ ]` **Morning routine that actually works:** flap the beaded water off the shell (30 seconds, genuinely effective on surface dew), pack it, then **open the bag out in direct sun at a mid-day stop** around San Luis Obispo / Santa Maria for 30–45 min. Flapping cannot reach water inside the baffles — your own overnight vapour condenses there — so the mid-day airing is the part that matters. Drying it strapped to the rack through Lompoc (km 226, 74–82 °F, spread 10–22 °F) works on the shell only, and arrives too late in the day to help.
- `[ ]` **Load the GPX + offline maps before you leave, and tell someone your ETA.** There is **no cell signal for ~73 km**, from Nepenthe (km 260 of day 1) to Ragged Point (km 36 of day 2) — no carrier has service south of Nepenthe — and **Limekiln, where you sleep, is in the middle of it**. Know your phone's satellite messaging before you need it.
- `[ ]` **Loaded shakedown ride** (20–30 km): confirm the bags don't foul braking or shifting before a 297 km day.
- `[ ]` **Also load the official USBR 95 file as a cross-check.** This coast is a designated national route (**US Bicycle Route 95**, Crescent City → Mexican border); Adventure Cycling publishes the USBRS digital maps **free** — grab the California file and keep it on the phone alongside the GPX. The built route already sits within 100 m of it for 83.0% of day 1, 83.4% of day 2, 75.0% of day 3 and 64.5% of day 4 (median offset 0 m), so it's a sanity reference, not a second route. Re-measure any time with `python3 scripts/validate_usbr95_alignment.py`.
- `[ ]` **DECIDE the Goleta question (day 3, km 15–28).** The official route uses the **Obern Trail**; mine uses the arterials. Measured: **21.93 km with 0 km of path vs 25.22 km with 9.11 km of separated path**. +3.3 km buys 9.1 km off Hollister Ave. Say the word and it goes into `pch_day3_refugio_la.gpx`.
- `[ ]` **Decide about San Diego — but not now.** Day 4 is built and audited (218.2 km, +685 m) and needs no advance booking, so you can decide at Los Angeles once you know how your legs are. That flexibility is its main advantage. If you take it: ride it in ONE day (hiker/biker sites at San Onofre, San Clemente and South Carlsbad are reported eliminated), and use the default `pch_day4_la_sandiego.gpx` unless you already hold a Camp Pendleton DBIDS pass. Reasoning and the alternatives in **[EXTENSIONS.md](./EXTENSIONS.md)**.
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
