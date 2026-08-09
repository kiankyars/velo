# 🛰️ San Francisco → Los Angeles by the coast — the built GPX

The routing deliverable for the southbound Highway 1 run: **three continuous
riding days**, San Francisco to Los Angeles via Big Sur, finishing at LA Union
Station because that is where the train home leaves from.

Built the same way as the Frankfurt loop in [ROUTE-GPX.md](./ROUTE-GPX.md) —
BRouter on OpenStreetMap, every OSM way tag echoed back and audited, distances
recomputed from the saved coordinates by a validator that does not trust the
builder — with a purpose-built road-bike profile, because the stock trekking
profile gets this coast badly wrong (see [below](#the-profile-and-why-the-stock-one-fails-here)).

> **Total: `782.4 km`, `+5,648 m`, 3 stages.** Stages join to within **1.2 m**.
> **Zero** unpaved metres on days 1 and 3, 48 m on day 2. **1,955 m** of
> out-and-back across the whole route, largest single jog 622 m (down from 62 km). One documented
> 391 m legal exception at Winchester Canyon.
>
> `python3 scripts/validate_pch_routes.py` → **ALL CHECKS PASS**.

| # | File | From → To | Distance | Climb |
|---|------|-----------|---------:|------:|
| 1 | [`pch_day1_sf_limekiln.gpx`](./gpx/pch_day1_sf_limekiln.gpx) | 426 Fell St, SF → **Limekiln SP** | **297.2 km** | +2,889 m |
| 2 | [`pch_day2_limekiln_refugio.gpx`](./gpx/pch_day2_limekiln_refugio.gpx) | Limekiln SP → **Refugio SB** | **279.5 km** | +2,148 m |
| 3 | [`pch_day3_refugio_la.gpx`](./gpx/pch_day3_refugio_la.gpx) | Refugio SB → **LA Union Station** | **205.7 km** | +611 m |
| | [`pch_sf_la_master.gpx`](./gpx/pch_sf_la_master.gpx) | all three in one file | **782.4 km** | +5,648 m |
| | [`pch_day1_alt_pfeiffer.gpx`](./gpx/pch_day1_alt_pfeiffer.gpx) | short day 1, stop in Big Sur Village | 256.1 km | +2,151 m |
| | [`pch_waypoints_essential.gpx`](./gpx/pch_waypoints_essential.gpx) | — | the readable waypoint set | — |
| | [`pch_waypoints.gpx`](./gpx/pch_waypoints.gpx) | — | every harvested POI | — |
| | `pch_day*_annotated.gpx` | per day | track **+ its own waypoints** | — |

Climb figures are BRouter's noise-filtered ascent. The raw point-to-point SRTM
sum is roughly double because it counts sampling noise on cliff faces as
climbing; it is kept in `data/pch_route_summary.json` only for comparison.

---

## ⚠️ Correction to the previous version of this file

**The earlier build was wrong, and it was wrong in a way that mattered.** It
reported day 1 as 326.4 km and said the planning transcript's 280–290 km estimate
was "about 40 km light."

That 326 km was inflated by **my own routing defects**. Via-points placed on
landmarks that sit *off* Highway 1 — Point Sur, Point Lobos, Carmel River State
Beach, Emma Wood, Leo Carrillo, Zuma, Avila Beach, Vandenberg Village — made the
router turn off the highway, run down an access road or into a car park, and come
straight back out. Fifty of those spurs, **62 km of pure out-and-back**, spread
across the three days. On a device it reads exactly as it sounds: the line runs
into a cul-de-sac and reverses.

With them removed the route is **782.4 km**, and **day 1 is 297.2 km** — so the
transcript's 280–290 km estimate was roughly right, and my correction of it was
not. The real remaining gap between the estimate and the measurement is about
7–17 km, not 40.

| | Day 1 | Day 2 | Day 3 | Total |
|---|---:|---:|---:|---:|
| Previous (with spurs) | 326.4 km | 302.7 km | 229.5 km | 858.6 km |
| **Now** | **297.2 km** | **279.5 km** | **205.7 km** | **782.4 km** |

The fix was two-part: **prune the corridor to genuine decision points** (Highway 1
from Carmel to Limekiln is 78 km on which there is no other road, so it now gets
two via-points instead of thirteen), and **turn on BRouter's
`correctMisplacedViaPoints`**, which the stock profile leaves off and which exists
precisely to discard "going back and forth on the same route" detours.

There is now a **spur check in the validator** so this cannot come back quietly.
Continuity checks are blind to it — the track never breaks, it just goes somewhere
and returns.

| | Spurs | Wasted |
|---|---:|---:|
| Before | 50 | 62,235 m |
| After | 8 | **1,955 m** (largest single 622 m) |

The survivors are small junction jogs of 100–620 m near Capitola, Seaside,
Winchester Canyon and Malibu, at road layouts where passing a point, turning, and
crossing back past it is what the road actually does.

### Also corrected: Devil's Slide

You were right. San Mateo County publishes hours for the **parking lots** only —
*"Parking is open from sunrise to sunset year-round"* — and the trail regulations
page lists fourteen rules without a single one restricting hours or mentioning a
gate on the trail itself. There is **no published closure of the Devil's Slide
Trail**, so a pre-dawn arrival is very likely fine; it is the car parks that shut,
which does not affect a cyclist riding through.

The earlier version overstated this as "may be gated shut" and shipped an inland
Skyline/CA-92 bypass file for it. **That bypass file is deleted** — it was
insurance against a problem that the sources do not actually support. Bicycles
remain banned from the Tom Lantos Tunnels, so the route still uses the trail;
that part was never in doubt.
([hours](https://www.smcgov.org/parks/devils-slide-trail-hours),
[regulations](https://www.smcgov.org/parks/devils-slide-trail-regulations))

---

## Fewer files, on purpose

The previous version shipped eight alternative overnight endpoints (Lucia, Ragged
Point, San Simeon, Gaviota, El Capitán, 17-Mile Drive, the inland bypass). With
the destination fixed at Los Angeles and the plan being to stop where you feel
like stopping rather than at a booked campground, alternative *endpoints* are
noise — it is the same road either way and you can stop anywhere along it.

One variant survives, because it changes the shape of a day rather than its last
kilometre: **`pch_day1_alt_pfeiffer.gpx`**, day 1 cut to 256 km by stopping in
Big Sur Village. That is the decision point for whether you descend the Big Sur
cliffs in the dark, and the village has food, water and a campground in one place.

## If you are camping wild rather than booking

It changes the plan for the better in one respect: **the Limekiln reservation
stops being a blocker.** California State Parks is explicit that Limekiln has
*"no first-come, first-served campsites"*, so without a reservation the booked
plan has no bed on night 1. Camping wild removes that dependency entirely.

Two things worth knowing before you rely on it, both sourced:

- **Dispersed camping on Los Padres National Forest land is allowed and needs no
  permit.** That is the legal version of "stop wherever" on this coast. The catch
  is geography: the strip immediately along Highway 1 through Big Sur is mostly
  state park or private ranch, where it is prohibited. The National Forest land —
  Ventana and Silver Peak Wilderness — is largely *east* of the highway and
  uphill, so it means getting off Highway 1 and climbing.
- **Campfires are banned outright until 31 January 2027.** A Forest Order
  effective **4 June 2026** prohibits campfire use at backcountry camps across
  Los Padres, including Ventana and Silver Peak. A **stove** is fine with a free
  California Campfire Permit. August is peak fire season and restrictions tighten
  further at short notice — check before you go.
  ([Forest Service](https://www.fs.usda.gov/r05/lospadres/alerts/los-padres-fire-use-and-firearm-restrictions))

The GPX does not change either way — the waypoint files still carry every
campground, water tap and store, which is more useful when you are improvising a
stop than when you have one booked.

### Sleeping bag and no tent: the bag is 2–6 °F short at Limekiln, and the air is saturated

NWS point forecasts for the actual places you'd sleep, pulled for the ride window:

| Where | Overnight lows | Sky | Wind |
|---|---|---|---|
| **Limekiln (night 1)** | **54 / 53 / 51 / 50 °F** | **"Areas of fog" every night, 9pm–5am** | 0–3 mph NW |
| Gorda | 60 / 60 / 58 / 57 °F | partly–mostly cloudy | 1–8 mph NW |
| **Pfeiffer Big Sur (valley)** | **62 / 60 / 58 / 56 °F** | **mostly clear** | 0–5 mph NW |
| Refugio (night 2) | 62 / 61 / 61 / 62 °F | patchy fog after 5am | 0–5 mph |

#### ⚠️ Correction: the bag does *not* have temperature margin here

An earlier version of this section said a 45 °F bag "is enough on temperature" with
"5–9 °F of margin," conditional on 45 °F being the **comfort** rating. **The
condition failed.** The bag is a **[Marmot NanoWave 45](https://www.rei.com/product/146503/marmot-nanowave-45-sleeping-bag-mens)**,
and REI publishes its tested ratings as **EN/ISO Comfort 56 °F, Lower Limit 49 °F** —
so even the "45" on the label is optimistic against the bag's own test.

| Site | Forecast lows | vs Comfort 56 °F | vs Limit 49 °F |
|---|---|---|---|
| **Limekiln** | 54 / 53 / 51 / 50 °F | **2–6 °F below** | 1–5 °F above |
| Pfeiffer Big Sur | 62 / 60 / 58 / 56 °F | at or above | fine |
| Refugio | 62 / 61 / 61 / 62 °F | 5–6 °F above | fine |

EN/ISO 23537's two figures are referenced to different sleepers: **Comfort** to a
standard woman lying relaxed, **Lower Limit** to a standard man lying *curled up* on
the edge of shivering. For a male sleeper the Limit is the conventionally applicable
number — which puts Limekiln's 50–54 °F **inside** the bag's rated band, 1–5 °F above
the Limit and 2–6 °F below Comfort.

So the honest verdict is **marginal, not inadequate**: a cool night at the bottom
edge of the bag's range, not an unusable bag. What decides whether it's merely cool or
genuinely cold is **the sleeping pad**, not the bag — see below. But the earlier claim
of "5–9 °F of margin" was wrong in the wrong direction, and the damp penalty below eats
what margin there is.

Two things follow. **Limekiln is the only site with a temperature problem** — Pfeiffer
and Refugio are both at or above the comfort rating. And the *bag* is one of the
strongest arguments for Pfeiffer that exists, independent of the fog.

#### The condensation problem, separately

Measured by dewpoint spread rather than by the word "fog"
(`python3 scripts/check_camp_dewpoint.py`):

| Site | Temp | Dewpoint | **Spread** | RH | Verdict |
|---|---:|---:|---:|---:|---|
| **Limekiln** | 53–56 °F | 53–56 °F | **0–2 °F** | 93–99% | **saturated** |
| **Refugio** | 61–65 °F | 61–65 °F | **0–3 °F** | 91–100% | **saturated** |
| **Pfeiffer** | 61–68 °F | 44–52 °F | **11–21 °F** | 48–68% | **dry** |

A bag radiating to the night sky sits 1–3 °F *below* air temperature, so at a 0 °F
spread deposition isn't a risk, it's the forecast. Note that **Refugio is saturated
too** — its forecast text reads only "Patchy fog after 5am," but the grid data says
RH 99–100%. The planned itinerary is **two consecutive saturation nights with no
dry-out between them**, which is the case where moisture compounds.

Limekiln also sits in a **redwood canyon**, and coast redwoods strip fog into drip —
under the canopy is wetter than open ground, not drier.

**The bag being synthetic (Marmot Spirafil polyester) is worth about 10–13 °F here —
but for a different reason than the marketing gives.** "Synthetic is warm when wet"
does not survive measurement; the one independent controlled test concludes synthetic
"will **not** keep you warm when it is wet — perhaps when it is **damp**." Water
conducts heat **23× better than air** (0.6 vs 0.026 W/m·K), so liquid in the loft is a
thermal short circuit whatever the polymer.

The mechanism that actually matters in saturated air is **moisture regain from humid
air**, and there the gap is enormous:

| Fill | Regain at 95% RH | Insulation lost |
|---|---:|---:|
| Polyester (his) | **0.4%** | ~0% |
| Untreated down | **11.0%** | **−33% R** |

Down's thermal conductivity rises 0.032 → 0.048 W/m·°C from humid air *alone*, and its
compression modulus collapses 280 → 117 Pa, so it physically cannot re-loft while
damp. In a down bag this trip's air would raise the effective lower limit from 49 °F to
roughly **62 °F** — a ~13 °F penalty before a single drop landed. **That penalty
essentially doesn't happen to a polyester fill.** He accidentally owns the right bag.

The residual damp penalty for polyester is smaller but real — estimated **3–8 °F**,
which is enough to matter given the margin above:

| Site | Dry margin vs 49 °F limit | After a 3–8 °F damp penalty |
|---|---|---|
| **Limekiln** | +1 to +5 °F | **−2 to −7 °F (below limit)** |
| Refugio | +12 to +16 °F | +4 to +13 °F (absorbed) |

So Limekiln is where damp and cold compound, and Refugio is where they don't.

#### What to actually do about it — the bivy is *not* the answer

An earlier version of this doc called a bivy "the highest-value single item you could
add." **Three findings say otherwise**, and they point somewhere cheaper.

**1. A bivy's warmth comes from blocking wind and sky radiation — and Limekiln has
neither channel open.** The quoted 4–10 °F gain is not a fabric property; it comes
from stopping convective loss to moving air and radiative loss to open sky. Limekiln
is **0–3 mph under fog under a redwood canopy** — both loss paths are already largely
closed, so you get the bottom of that range, not the top. The tidy match between "a
few °F short" and "bivies add 5–10 °F" is coincidence.

**2. Saturated air is exactly where a waterproof-breathable membrane stops working.**
A membrane moves vapour down a vapour-pressure gradient. At a **0–2 °F spread and
93–99% RH there is no gradient**, and the shell sits at or below the dewpoint. So a
bivy in this airmass can dampen the bag as readily as it protects it — the two
effects fight rather than add.

**3. Almost none of them are buyable in time.** REI's entire bivy category is six
SKUs, and five are **pre-order at ~30 days**. Only the Black Diamond Spotlight
($209.73, 669 g, REI Outlet closeout, zero reviews) is in stock. The Outdoor Research
Helium UL is the **worst-reviewed item in the category at 3.3/5**, with an owner
reporting the sleeping bag got wet *with the entry fully open*.

**The better buys, in order:**

| Item | Price | Weight | What it does |
|---|---:|---:|---|
| **Clothing you already carry** | **$0** | **0 g** | **~10 °F.** Sleep in the cycling layers. Beats everything below. |
| Sea to Summit Reactor liner (Midweight / Fleece) | $75–95 | 210–420 g | Claimed +10/+15 °F, realistically less — but it adds insulation *inside* the bag and creates **no condensation surface**. In stock. |
| Closed-cell foam pad (Z Lite Sol) | ~$50 | 285–400 g | +R 2.0, and **immune to moisture**. Only worth it if the mattress is uninsulated — see below. |
| SOL Escape Bivy with Hood | $86.50 | 207 g | Air-permeable, not a membrane: 0.67 CFM vs 0.5 CFM for eVent on the bench. But 1,336 mm hydrostatic head — water-*resistant*, and it leaks under a knee or elbow. |

#### The pad: a Klymit Static V, and it is the binding constraint

The pad is a **Klymit Static V — R 1.3**, ASTM F3340-18 (Klymit's EU page labels the
original pad's 1.3 as ASTM explicitly), 530 g, $49.95. The non-insulated model.

ISO 23537-1:2022 **clause 5.1.4 ("Artificial ground")** specifies the manikin lying on
a mattress of Rct = 0.85 ± 0.06 m²K/W — **R 4.8** — so Comfort 56 °F / Limit 49 °F
already *assume* good ground insulation. The bag checks out exactly against the
standard: ISO Table 1 at Rc(1) = 0.620 m²K/W gives 13.3 °C / 9.7 °C, matching Marmot's
published 56.1 °F / 49.6 °F to a tenth of a degree.

**Correction to an earlier figure here: the penalty is 5–7 °F, not 15–20 °F.** The
15–20 °F number is real and it is REI's own measurement — but it was taken on a
**Magma 15** (ISO Limit 16 °F), and the penalty scales with how warm the bag is,
because a thin bag already loses most of its heat upward. Calibrated against REI's
four published points (RMS 0.29 °F, and the model reproduces their 17 °F on the Magma
independently):

| Bag ISO Limit | R 4.8 → R 1.3 penalty |
|---|---:|
| **49 °F (NanoWave 45)** | **+5.8 °F** |
| 30 °F | +11.3 °F |
| 16 °F (Magma 15) | +16.3 °F |
| 0 °F | +22.8 °F |

So on the Static V the effective figures become roughly **Comfort 61–63 °F, Limit
55–58 °F** (the wider end allows for saturated soil, which conducts far better than
the lab's plywood-over-air-cavity: effective ground R swings from 2.55 dry duff to
0.72 saturated, worth ~4.5 °F in this bag).

| Site | Effective Comfort / Limit | Forecast lows | Verdict |
|---|---|---|---|
| **Limekiln** | 63 / 58 °F | 50–54 °F | **4–8 °F below limit — this is the night that breaks** |
| Pfeiffer, in the open | 66 / 60 °F | 56–62 °F | marginal (clear sky costs ~6 °F radiatively) |
| **Pfeiffer, under canopy** | **60 / 54 °F** | **56–62 °F** | **works — the best spot on the route** |
| Refugio | 63 / 58 °F | 61–65 °F | at/above limit, near comfort — acceptable |

Two things fall out that aren't obvious. **Fog is thermally helpful**: a clear sky
costs a tentless sleeper ~6 °F of radiative loss, and fog or canopy cuts that to ~0.
Pfeiffer is the dry site but the *clear* one, so sleeping **under trees at Pfeiffer**
gets the dry airmass *and* blocks the sky — better than either site in the open.
And measured coastal August soil is **warmer** than the nocturnal air minimum
(Bodega Bay 60.6 °F at 5 cm against a 52.5 °F air min), which trims the penalty.

**The fix, and one trap.** Stacked pad R-values **are** additive — Therm-a-Rest and
NEMO both state it explicitly for this exact configuration ("layering that Z-Lite
under your inflatable pad will boost your overall R-Value by 2.0"), and the
second-order error is under 0.5 °F. Static V + Z Lite Sol ≈ **R 3.3**, which moves
Limekiln from Comfort 63 / Limit 58 to **58 / 52** — recovering 5–6 °F and turning the
worst night from *cold* into *break-even*.

**The trap is coverage, not conductance.** Area-weighted, a torso-length pad at 47%
coverage yields **R 1.96, not R 3.3 — 41% short of nominal.** Buy full length. Note
also the real weights: the full-length Z Lite Sol is **397–415 g**, not 300 g; 283 g
buys only the 130 cm torso version. And a **$15 half-inch blue foam roll (~R 1.4,
~320 g) captures roughly 85% of the benefit** of the $50 pad.

What a pad *cannot* do: since the rating was measured on R 4.8, a pad can only
**restore** the bag toward 56/49 °F — never past it. R 3.3 is still 31% short of the
rated baseline.

Failing all of it, sleep under a **solid roof**
(picnic shelter, restroom eave, the lee of a building) — **not** under the redwoods,
which is the opposite of shelter here: coast redwoods strip fog into drip and are
wetter beneath than open ground. Prefer a synthetic or hydrophobic-down bag over
untreated down. Put a groundsheet under the pad; dew comes from below too.

#### "Can't I just flap the water off in the morning and pack it up?"

Partly. It's worth the 30 seconds, and it is **not** the whole answer. Three
physically different kinds of water end up in the bag, and flapping only reaches one:

| Where the water is | Can flapping remove it? |
|---|---|
| **(a)** Beaded on the outer shell, DWR intact | **Yes** — flicks off cleanly |
| **(b)** Wetted *into* the shell fabric after hours in saturated air | No — flapping redistributes it |
| **(c)** Condensed **inside the baffles**, from your own overnight vapour hitting its dew point near the cold outer shell | No — it's behind a layer of fabric |

Quantified for one night in this airmass:

| | Amount |
|---|---:|
| Total overnight weight gain | **150–300 g** (≈350 g worst case) |
| External dew deposition (shell area 2.46 m², ~1.23 m² sky-exposed) | 25–320 g, mean ~172 g |
| Your own body moisture entering the bag | 80–120 g/night, ~50–100 g retained |
| **Removable by flapping** | **30–80 g** |

So flapping recovers roughly **a quarter** of what the night puts in. The rest needs
evaporation, and evaporation is exactly what this forecast switches off:

| Drying 200 g of water | Time |
|---|---:|
| Lashed on the bike, dry moving air (20 km/h, 20 °C, 50% RH) | **~21 min** |
| Sitting in the marine layer (15 °C, 95% RH) | **~4.7 h** |
| At 99–100% RH — Limekiln and Refugio overnight | **effectively never** |

A 13× airmass ratio. That is why the mid-day inland stretch matters and the campsite
morning does not: **open the bag out in direct sun at a stop around San Luis Obispo /
Santa Maria for 30–45 minutes.** Opened and lofted for half an hour beats eight hours
strapped to a rack compressed, because compressed insulation in moving air dries from
the outside in.

Rack-drying through **Lompoc (day 2, km 226: 74–82 °F, spread 10–22 °F, RH 47–72%)**
does work on the *shell* — but km 226 of 279 is 81% through the day, roughly
16:00–18:00, and you then arrive at Refugio where the spread is 0 °F again. You'd be
re-wetting what you just dried.

**Packing it damp is fine for a day.** Mould needs 24–48 h on damp surfaces (EPA), as
fast as 8–12 h on soiled wet textiles in warm humid air — so a damp bag stuffed at
07:00 and unpacked at 19:00 is not at risk. Three consecutive damp days without a
real dry-out is where it turns.

**The working sequence:** flap off the beads → pack → open it out in the sun at a
mid-day stop → and don't count on the campsite morning for anything.

#### ⚠️ Second correction: Pfeiffer is a trade, not a free fix

Pfeiffer Big Sur in the valley is **mostly clear at 56–62 °F with a dewpoint spread
of 11–21 °F**, while Limekiln is **fogged in at 50–54 °F with a spread of 0–2 °F** —
a different airmass, not a marginal improvement, and the only night on the itinerary
where the bag is at its comfort rating *and* the air isn't saturated.

An earlier version of this doc then said that costs "41 km off day 1." **That was
wrong, and it was wrong on arithmetic that was already in this repo.** Pfeiffer sits
at **km 255.2 of the day-1 track, 363 m off the line, 41.8 km *short* of Limekiln** —
it is 27 km of latitude *north* of Limekiln, a waypoint on the way, not a destination
off to one side. The 41.8 km is **deferred to day 2, not saved:**

| Pairing | Day 1 | Day 2 | Day 2 climb |
|---|---:|---:|---:|
| Limekiln (standard) | 297.0 km / +2,889 m | **279.4 km** | +2,148 m |
| Pfeiffer (variant) | 255.9 km / +2,151 m | **322.4 km** | **+2,945 m** |

That pushes day 2 **over the 300 km/day ceiling**, and the deferred kilometres are
the Big Sur south coast — the section this doc documents as a **73 km cell dead zone
with no bail-out**, which the Pfeiffer pairing moves into the *first* hour of day 2
instead of the last hour of day 1.

The variant was also incomplete: there was no day-2-from-Pfeiffer file, so the option
could not be costed. There is now — **`pch_day2_pfeiffer_refugio.gpx`, 322.4 km,
+2,945 m**, audited clean (0 km `bicycle=no`, 0% unpaved, all freeway
bicycle-legal). Take Pfeiffer for the dry night if you want it, but take it knowing
it buys a 322 km day 2, and load both files.

And the honest point in favour of your plan: **no tent is better for camping wild.**
Low profile, nothing visible from the road, and you can be packed and moving in two
minutes.

### Cell coverage: about 73 km of nothing, with your campsite in the middle

Big Sur is a genuine dead zone, not a weak-signal zone. **No carrier has service
south of Nepenthe**; Deetjen's has none from any provider; there are long stretches
with nothing at all between Big Sur Village and Lucia. Verizon and AT&T have towers
south of the Big Sur valley at the top of the grade, and AT&T has one at Point Sur
that only works with line of sight to it.

In route terms:

| | |
|---|---|
| Last reliable signal | **~km 260 of day 1** (Nepenthe) |
| Signal returns | **~km 36 of day 2** (Ragged Point / San Simeon) |
| Offline stretch | **≈ 73 km** |
| Where you sleep | **km 297 of day 1 — inside it** |

Everything else on the route is fine: days 3 and 4 are urban or suburban end to
end. So this is one specific 73 km window, and it happens to contain the night.

What to do about it:

- **Load the GPX and offline maps before you leave.** Do not plan to fetch anything
  on the road — you cannot check the Caltrans traffic control, a campground, or a
  weather update from inside that stretch.
- **Tell someone your plan and your expected arrival**, because a missed check-in is
  the only alarm that will work.
- **Know your phone's satellite messaging before you need it.** iPhone 14 and later
  support Emergency SOS via satellite, and recent iOS versions add Messages via
  satellite; a dedicated satellite messenger is the belt-and-braces version. Big
  Sur is exactly the terrain those were built for.
- The waypoint files already carry every water tap, store and campground in that
  window, which is the point of having them on the device rather than in a browser.

---

## ⚠️ There is an official route, and I should have started from it

**US Bicycle Route 95 is AASHTO-designated the length of California — Crescent
City to the Mexican border** — and Adventure Cycling publishes the USBRS digital
maps for free ([advcy.link/causbr](https://www.adventurecycling.org/routes-and-maps/adventure-cycling-route-network/pacific-coast/)).
OSM carries it as nine `route=bicycle, network=ncn, ref=95` relations.

This repo's own method, written down in [ROUTE-GPX.md](./ROUTE-GPX.md), is: use the
official GPX as the backbone and reserve BRouter for the connectors that aren't part
of any signed route. That is exactly how the Frankfurt loop was built — EV15, EV17,
EV7 and EV6 come from the official EuroVelo files. **I did not check for an official
backbone before building this one.** That was a process miss, not a judgement call.

[`scripts/validate_usbr95_alignment.py`](./scripts/validate_usbr95_alignment.py)
now fetches USBR 95 and measures the built route against it, so the official line
is a permanent reference rather than something to rediscover.

### How much difference did it make? Less than you'd fear

| Stage | within 100 m | 250 m | 500 m | median offset |
|---|---:|---:|---:|---:|
| Day 1 SF → Limekiln | **83.0%** | 86.9% | 88.7% | **0 m** |
| Day 2 Limekiln → Refugio | **83.4%** | 87.5% | 89.9% | **0 m** |
| Day 3 Refugio → LA | **75.0%** | 80.6% | 86.0% | **0 m** |
| Day 4 LA → San Diego | **64.5%** | 71.0% | 77.2% | **0 m** |

Measured against 107,508 official reference nodes. It's largely the same road,
which is what you'd expect on a coast where Highway 1 is often the only option.

### Every divergence over 1.5 km, and why

Three of them are deliberate and would not be fixed by using the official file,
because USBR 95 doesn't know where you live or which train you're catching:

| Stage | km | Length | What it is |
|---|---|---:|---|
| 1 | 0 → 3 | 3.0 km | **Your front door.** USBR 95 doesn't start at 426 Fell St. |
| 3 | 179 → 206 | 26.8 km | **Santa Monica → LA Union Station.** Deliberate: the train home. USBR 95 stays coastal. |
| 4 | 0 → 30 | 30.4 km | **Union Station → Long Beach** on the LA River path. USBR 95's LA section starts in Santa Monica. |

The rest are genuine alignment differences worth knowing about:

| Stage | km | Length | Where | Official route does |
|---|---|---:|---|---|
| 1 | 146 → 166 | 19.3 km | Pajaro Valley | a different crossing than my San Andreas Rd line |
| 1 | 125 → 135 | 10.5 km | Santa Cruz | the coastal side rather than Mission St / Soquel Dr |
| 2 | 205 → 228 | 21 km | Vandenberg / Lompoc | a different line through the base's edge |
| **3** | **15 → 28** | **12.9 km** | **Goleta** | **the Obern Trail — see below** |
| **4** | **133 → 145** | **12.0 km** | **Camp Pendleton** | **goes through the base — see below** |
| 4 | 203 → 218 | 15.2 km | into downtown San Diego | a different approach to Santa Fe Depot |

### Two things the official route taught me

**1. Goleta: the Obern Trail.** USBR 95 routes through Goleta on the **Obern
Trail** — 586 mapped nodes of `highway=cycleway, bicycle=designated` — plus
Hollister Ave, Calle Real and the Modoc Road Multiuse Path. My line uses the
arterials instead. Routed both:

| | Distance | Separated path |
|---|---:|---:|
| My line (Winchester → Goleta → Santa Barbara) | 21.93 km | 0 km |
| Via the Obern Trail | **25.22 km** | **9.11 km** |

**+3.3 km buys 9.1 km off the arterials.** For a 200 km day that's a real trade in
either direction — the trail is safer, a shared-use path along a slough is slower.
Not forced into the GPX; noted so it's your call.

Also worth recording: the official designated route itself includes a short run of
`El Camino Real [motorway] bicycle=no` at Goleta. **The national route makes the
same compromise I did** with the 391 m Winchester Canyon exception, which is mild
vindication that the exception reflects the road rather than a routing error.

**2. Camp Pendleton — and a correction.** USBR 95 goes **through the base**, on
**Old Pacific Highway** (`bicycle=yes`) and the **Pacific Coast Bikeway**
(`highway=cycleway, bicycle=yes`), continuing into Oceanside on North Pacific
Street and Harbor Drive.

So an earlier claim in [EXTENSIONS.md](./EXTENSIONS.md) was **wrong**: I wrote that
the bikeway "dead-ends southbound." It doesn't — it runs right through to Oceanside,
and a national route is designated along it. What's true is narrower: **it is
gated**, and has needed a DBIDS pass since 1 October 2018. BRouter can't route it
without passing the 80 m `access=permit` link, which is what produced the dead-end
impression. The I-5 bypass remains the correct pass-free line; the reasoning for it
was right, the description of the alternative was not.

---

## The profile, and why the stock one fails here

Geometry comes from BRouter using [`scripts/velo_pch_road.brf`](./scripts/velo_pch_road.brf),
a retuned copy of the stock `trekking` profile. Every change was forced by an
actual wrong route observed while building:

1. **Highway 1 *is* the cycle route.** Trekking charges 10.0 for a trunk road and
   3.0 for a primary without a bike hint. CA-1 is variously trunk, primary and
   secondary along its length, so those penalties push the line onto inland farm
   roads. Here all three sit near 1.0, just above a cycleway so a parallel bike
   path still wins in town.
2. **No elevation avoidance.** With `consider_elevation` on, the cheapest way to
   flatten San Francisco → Los Angeles is to abandon the coast for the Salinas
   Valley.
3. **Freeway in three tiers**, keyed on OSM's bicycle tag: `bicycle=no` excluded,
   `bicycle=yes` 2.0, untagged 2.6. That middle tier is not optional — with
   untagged freeway banned outright, the router answered the 5 km hop from El
   Capitán to Goleta by crossing the Santa Ynez Mountains: 75 km, +1,504 m, over
   a 695 m pass, with 5.3 km of unpaved track.
4. **Pavement only.** Gravel, dirt, sand, grass and tracktype grade2+ penalised
   hard, and the cycle-route bonus withheld from unpaved ways — otherwise a dirt
   path tagged `lcn` gets a flat cost of 1.0 and beats the paved highway.
5. **`correctMisplacedViaPoints = true`**, unlike stock. See the correction above.

`bicycle=no` is **excluded outright**, not discounted. Stock trekking charges only
4 when a bike-banned way still allows pedestrians ("you may push your bike"),
which routed this trip through the Tom Lantos Tunnels. Making it merely expensive
instead of forbidden immediately put 510 m of bike-banned trail inside Point Lobos
into day 1 — hence the hard ban.

> **A trap for whoever edits the profile next:** every tag *value* must exist in
> BRouter's `lookups.dat`, or the profile is rejected at route time with a bare
> **HTTP 500 and an empty body**. `chipseal`, `concrete:plates`, `concrete:lanes`,
> `unhewn_cobblestone` and `woodchips` are **not** in it. `smoothness=very_good` is.
>
> And: bump `PROFILE_CACHE_KEY` in `build_pch_route.py` whenever a `.brf` changes,
> or cached geometry from the old profile comes straight back at you.

### The 391 m at Winchester Canyon

OSM starts the US-101 `bicycle=no` run about 1 km west of the Winchester Canyon
off-ramp (196 US-101 ways tagged `bicycle=no` between Gaviota and Ventura,
westernmost at `34.4339,-119.9147`). Taken literally there is no legal bicycle
path at all from the Gaviota coast into Goleta, and the router's answer is the
85 km mountain crossing.

So one leg — named in `pch_waypoints.PERMISSIVE_LEGS` — is routed with
[`velo_pch_road_bridge.brf`](./scripts/velo_pch_road_bridge.brf), identical but for
allowing `bicycle=no` at cost 8. It uses **391 m** of disputed freeway and saves
77 km. It is the Adventure Cycling Pacific Coast alignment and riders use that
shoulder; leave 101 at the Winchester Canyon off-ramp for Calle Real / Hollister
Ave. Everywhere else the ban holds — US-101 genuinely is closed to bicycles from
Santa Barbara to Ventura, and day 3 routes around it with zero bike-banned metres.

---

## Validation

[`scripts/validate_pch_routes.py`](./scripts/validate_pch_routes.py) re-reads the
saved GPX, re-parses the XML and recomputes distance from the coordinates.

| Check | Result |
|-------|--------|
| XML well-formed, GPX 1.1, has trackpoints | ✅ all 4 stage files |
| Continuity (largest single jump) | ✅ **299 m** — simplified to 2.5 m then re-densified to ≤ 300 m |
| **Out-and-back spurs** | ✅ ≤ **1,178 m** per stage, largest single **622 m** |
| Seam day 1 → 2 / day 2 → 3 | ✅ **1.2 m** / **0.0 m** |
| Recomputed distance vs. build summary | ✅ within 2% |
| Every corridor waypoint on its own track | ✅ worst offset 771 m (Orcutt town centre) |
| Master reproduces the three per-day files | ✅ 3 tracks, 782.0 km |
| `bicycle=no` | ✅ **0.391 km**, all of it the documented Winchester Canyon gap |
| Freeway not marked bicycle-legal | ✅ the same 391 m, not additional |
| Unpaved (worst stage) | ✅ **0.048 km** |
| Ferries / steps | ✅ 0.0 km |

Machine-readable: [`data/pch_route_summary.json`](./data/pch_route_summary.json)
and [`data/pch_validation.json`](./data/pch_validation.json).

### Bugs caught while building

- **50 out-and-back spurs, 62 km** — the big one; see the correction above.
- **Garrapata State Park** — geocoded centroid sits 1.2 km inland at 540 m; as a
  via-point it dragged the line 6.8 km up Garrapata Canyon (+585 m).
- **Piedras Blancas light station** — routing to it fails outright (`no track
  found`): the headland access road is a disconnected private way in OSM.
- **Three via-points snapped onto dirt** — Piedras Blancas (1,964 m), the elephant
  seal vista car park (349 m), San Simeon Acres (2,590 m of `surface=dirt`).
- **A cue-sheet scanner bug** that silently pinned every day-3 waypoint to km 2.8.

Geocoders are hostile on this corridor, which is why
[`scripts/pch_waypoints.py`](./scripts/pch_waypoints.py) carries explicit
coordinates: *"Monterey, California"* resolves 10 km from the city, *"San Luis
Obispo, California"* lands **41 km inland**, *"Harmony, California"* comes back
**434 km away** in San Diego County, and every Amtrak query collapses onto
Guadalupe.

---

## The climbs, measured from the route's own elevation profile

Detected by walking the smoothed profile, not from memory — which is how the
summit of Hurricane Point fell out at `36.3583,-121.9006` without being told it
exists.

| Day | km | Climb | Length | Gain | Summit |
|-----|---:|-------|-------:|-----:|-------:|
| 1 | 8.1 → 18.9 | out of San Francisco over the ridge | 10.85 km | +185 m | 191 m |
| 1 | 29.9 → 32.2 | **Devil's Slide Trail** | 2.25 km | +141 m | 142 m |
| 1 | 198.2 → 209.3 | Monterey Bay to Carmel | 11.12 km | +171 m | 183 m |
| 1 | 233.7 → 236.5 | **Hurricane Point** (after Bixby Bridge) | 2.79 km | +130 m | 164 m |
| 1 | 244.6 → 259.0 | **Grimes Point / Nepenthe** — day 1's biggest | 14.43 km | +255 m | 298 m |
| 2 | 19.7 → 27.1 | south of Gorda toward Ragged Point | 7.42 km | +200 m | 243 m |
| 2 | 29.7 → 32.4 | the **Ragged Point** climb | 2.69 km | +143 m | 244 m |
| 2 | 207.8 → 213.8 | CA-1 out of the Santa Maria valley | 6.00 km | +193 m | 296 m |
| 2 | 231.8 → 252.5 | **CA-1 over the Santa Rosa Hills** (Lompoc → Las Cruces) | 20.72 km | +272 m | 328 m |
| 3 | — | nothing over 110 m all day | — | +611 m total | — |

Gains are SRTM-derived. Treat gradients on the Big Sur cliffs with suspicion —
SRTM's 30–90 m posting misreads a road cut into a cliff face.

---

## Water and food — where you actually run dry

`harvest_pch_pois.py` queries Overpass with an `around` clause against the routed
line, so everything returned is genuinely beside the road, then measures the
longest run with no water and no shop, counting only POIs within 400 m.

Day 2 is the one to carry food on. Its worst dry stretch is **43.0 km from
km 179.9 — Guadalupe through the dunes to Lompoc** — and the next-worst is the
climb out of Lompoc over the Santa Rosa Hills to Las Cruces, which reproduces from
OSM data alone exactly what touring cyclists say about that road: *"there are very
few opportunities for water or food between Lompoc and Santa Barbara. The rest stop
at Gaviota is the best place to water up."* Fill up in **Guadalupe (km 180)** and
again in **Lompoc (km 226)**.

Big Sur is **not** day 1's problem — Big Sur Village, Big Sur Station, Nepenthe,
Lucia and the campgrounds keep those gaps under 30 km. The San Mateo coast between
Half Moon Bay and Santa Cruz is worse, because Pescadero and San Gregorio sit
inland off the highway. Current figures per stage are in
[`data/pch_pois.json`](./data/pch_pois.json).

## Two live hazards worth knowing

**PCH through Malibu is an active fire-rebuild corridor.** The last ~50 km of day 3
runs through the Palisades Fire reconstruction. Caltrans District 7 has a
rock-slope-protection and pavement rebuild near Ratner Beach due to finish **Fall
2026**, and a second project covering about five miles from just south of the
California Incline to Topanga Creek due **end of 2026**. After the fire, PCH
reopened with **one lane each way at 25 mph**. The route leaves PCH at Santa
Monica Pier and turns inland via Culver City, so the exposure is Malibu → Santa
Monica only.
([source](https://dot.ca.gov/caltrans-near-me/district-7/district-7-projects/pch-palisades-fire-repairs))

**Vandenberg can close the road at short notice.** Launch operations close roads
around the base — one case shut CA-246 between CA-1 and Mission Gate Road for five
hours on 2 March 2026 for a launch that then scrubbed. That was CA-246, not this
route's CA-1 line, but CA-1 has been closed here for base incidents and carries
ongoing roadwork. The only detour is US-101 inland via Santa Maria.

## Big Sur road status

Highway 1 reopened through Regent's Slide on **14 January 2026**, ~90 days early,
after an $82 million repair; Caltrans calls the slope stable and monitors it
continuously. As of August 2026 there is **one-way, signal-controlled traffic at
Rocky Creek Bridge, 24/7 through 31 August, delays to 15 minutes** — that is
**km 234.8 of day 1**, and you will be stopped in it. Check
[QuickMap](https://quickmap.dot.ca.gov) the morning you leave.
([reopening](https://www.gov.ca.gov/2026/01/14/governor-newsom-announces-early-reopening-of-highway-1-through-big-sur/),
[conditions](https://www.bigsurcalifornia.org/highway-1-conditions/))

## Reproduce

```bash
python3 scripts/build_pch_route.py      # gpx/pch_*.gpx + data/pch_route_summary.json
python3 scripts/harvest_pch_pois.py     # gpx/pch_waypoints*.gpx + data/pch_pois.json
python3 scripts/validate_pch_routes.py  # data/pch_validation.json, non-zero exit on failure
```

BRouter and Overpass responses are cached under `scripts/.cache/`. Overpass's main
instance times out almost always; the harvester falls through a mirror list.

### Caveats

- Geometry is OpenStreetMap via BRouter; tag auditing is only as good as OSM's
  tagging, which is why the Winchester Canyon exception exists and is documented.
- Live conditions were checked on **4 August 2026** and are perishable.
- The per-person hike/bike rate at Refugio and Gaviota is not published on either
  park page — phone **(805) 968-1033** if you end up wanting a legal site.
