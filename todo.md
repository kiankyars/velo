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
- `[ ]` **⚠️ MEASURE YOUR SLEEPING PAD'S R-VALUE BEFORE BUYING ANYTHING.** This is the one unmeasured input and it outweighs everything else here. ISO 23537 rates bags with the manikin on an **R-4.8 pad** (cl. 5.1.6), so Comfort 56 °F / Limit 49 °F *already assume* good ground insulation. An uninsulated summer air mattress is **R 0–1**, worth an effective **15–20 °F** penalty — 3–10× the gap the bag is short by, and ground conduction is 25–40% of heat loss lying down. If yours is uninsulated, the bag is not the binding constraint at Limekiln and **Refugio at 61–65 °F stops being safe either**. If it's a NeoAir-class insulated mat (R 4–5), the bag at 50–54 °F is unremarkable and you need much less.
- `[ ]` **Free ~10 °F before you spend a dollar: sleep in your cycling layers.** More than any purchase below, zero grams, already in the bags.
- `[ ]` **Pfeiffer for night 1 is a TRADE, not a free fix — correction.** An earlier version of this list said it costs "41 km off day 1." Wrong: Pfeiffer sits at **km 255.2 of the day-1 track, 41.8 km _short_ of Limekiln** (27 km of latitude north of it), so the distance is **deferred to day 2, not saved**. Day 2 from Pfeiffer is **322.4 km / +2,945 m** (`pch_day2_pfeiffer_refugio.gpx`, now built and audited) against 279.4 km / +2,148 m from Limekiln — **over your 300 km ceiling**, and it moves the 73 km cell dead zone into the first hour of the day. Still the only dry night available (spread 11–21 °F vs 0–2 °F); just cost it honestly, and load **both** Pfeiffer files if you take it.
- `[ ]` **Do NOT buy a bivy expecting warmth at Limekiln.** A bivy's 4–10 °F comes from blocking wind and sky radiation; Limekiln is **0–3 mph under fog under redwood canopy**, so both channels are already closed and you get the bottom of the range. Worse, at a 0–2 °F spread a waterproof-breathable membrane has **no vapour gradient to work with**, so it can dampen the bag as readily as protect it. Logistics agree: REI's whole bivy category is 6 SKUs, **5 are pre-order at ~30 days**, and the Outdoor Research Helium UL is the worst-reviewed item in it (3.3/5, an owner reports a wet bag *with the entry fully open*).
- `[ ]` **If you do buy, buy in this order** — all worth confirming by phone at REI SF Brannan, **(415) 934-1938**, since online stock ≠ shelf stock:
  1. **Sea to Summit Reactor liner, Midweight or Fleece-weight** — $75–95, 210–420 g. Claimed +10/+15 °F (discount it), but it adds insulation *inside* the bag and creates **no condensation surface**. In stock online; good odds in store. The only item that attacks the actual problem cleanly.
  2. **Closed-cell foam pad (Therm-a-Rest Z Lite Sol)** — ~$50, 285–400 g, +R 2.0, immune to moisture, and it dries instantly. **Only if the mattress is uninsulated.** Bulky, must go outside the bags, doesn't care that it gets soaked. Almost certainly in stock; also at Sports Basement/Big 5.
  3. **SOL Escape Bivy with Hood** — $86.50, 207 g. Air-permeable spunbond, not a membrane: bench-measured **0.67 CFM vs 0.5 CFM for eVent**, so it breathes better than the WPB options in saturated air. Caveat: **1,336 mm hydrostatic head, below the 1,500 mm rainproof threshold** — water-resistant only, and it leaks under a knee or elbow point load. Pre-order online, so this one needs a shelf.
  - **Skip:** the orange SOL *Emergency* Bivvy (zero breathability — it will pump your own sweat into the fill; carry it unopened as a 108 g backstop, don't sleep in it), Nikwax TX.Direct (the wetting here is condensation, not rain, and it needs a washing machine), and any WPB bivy at $300–430 on 30-day pre-order.
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
