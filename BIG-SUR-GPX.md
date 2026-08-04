# 🛰️ San Francisco → Los Angeles by the coast — the built GPX

The routing deliverable for the southbound Highway 1 camping run: **three
continuous riding days**, San Francisco to Los Angeles via Big Sur, with the
Limekiln and Refugio hike/bike sites as the two overnights, plus every
alternative endpoint the plan leaves open as its own loadable file.

Built the same way as the Frankfurt loop in [ROUTE-GPX.md](./ROUTE-GPX.md) —
BRouter on OpenStreetMap, every OSM way tag echoed back and audited, distances
recomputed from the saved coordinates by a script that does not trust the
builder — but with a purpose-built road-bike profile, because the stock trekking
profile gets this coast badly wrong (see [below](#the-profile-and-why-the-stock-one-fails-here)).

> **Total: `858.6 km`, `+6,800 m`, 3 stages.** Every stage joins the next to
> within **1.2 m**. **Zero** unpaved metres on day 1, 48 m on day 2, 223 m on
> day 3 (190 m of which is the Santa Monica Pier boardwalk). **391 m** of one
> deliberate, documented legal exception — [the Winchester Canyon
> gap](#the-one-deliberate-exception-391-m) — and no other bike-banned or
> not-explicitly-legal freeway metre anywhere. **945 waypoints** harvested and
> curated, of which 273 are in the readable subset.
>
> `python3 scripts/validate_pch_routes.py` → **ALL CHECKS PASS**.

---

## The three days

| # | File | From → To | Distance | Climb | Notes |
|---|------|-----------|---------:|------:|-------|
| 1 | [`gpx/pch_day1_sf_limekiln.gpx`](./gpx/pch_day1_sf_limekiln.gpx) | 426 Fell St, SF → **Limekiln SP** | **326.4 km** | +3,642 m | The whole ride is in this day. 12 climbs over 70 m. |
| 2 | [`gpx/pch_day2_limekiln_refugio.gpx`](./gpx/pch_day2_limekiln_refugio.gpx) | Limekiln SP → **Refugio SB** | **302.7 km** | +2,377 m | 19.8 km of bicycle-legal US-101 shoulder. |
| 3 | [`gpx/pch_day3_refugio_la.gpx`](./gpx/pch_day3_refugio_la.gpx) | Refugio SB → **LA Union Station** | **229.5 km** | +781 m | The easy day. Only 2 climbs over 70 m. |
| | [`gpx/pch_sf_la_master.gpx`](./gpx/pch_sf_la_master.gpx) | all three in one file | **858.6 km** | +6,800 m | For a device that wants one route. |
| | [`gpx/pch_waypoints_essential.gpx`](./gpx/pch_waypoints_essential.gpx) | — | — | — | **273 waypoints** — every curated stop plus water, campgrounds and bike shops. The one to put on the bike computer. |
| | [`gpx/pch_waypoints.gpx`](./gpx/pch_waypoints.gpx) | — | — | — | **945 waypoints** — the above plus every convenience store, supermarket, fuel stop and public toilet within range of the line. Thorough; too dense to read while moving. |
| | `gpx/pch_day*_annotated.gpx` | per day | — | — | Each day's track **with its own waypoints embedded** (411 / 208 / 326). |

Climb figures are BRouter's noise-filtered ascent. The raw point-to-point SRTM
sum is roughly double (13,022 m for the route) because it counts sampling noise
on cliff faces as climbing — that number is meaningless and is recorded in
`data/pch_route_summary.json` only for comparison.

---

## ⚠️ Four things the GPX says that the plan didn't

The plan these files were built from came out of a chat transcript. Building the
route measured it, and four numbers moved.

**1. Day 1 is 326 km, not 280–290 km.** Measured from the saved coordinates,
San Francisco to Limekiln is **326.4 km with +3,642 m**. The estimate was low by
roughly 40 km — about an extra 1½–2 hours. On a 05:00 start that is the
difference between arriving in dusk and arriving in the dark, and the last 80 km
are the Big Sur cliffs. It also collides with the next item.

**2. Limekiln is reservation-only. There are no first-come-first-served sites.**
California State Parks states it plainly on the Limekiln camping page:
*"Reservations are strongly encouraged for all campsites. **There are no
first-come, first-served campsites.**"* The hike/bike site is **$5/night**, you
must arrive on foot or by bike with no vehicle, and the stay is capped at two
consecutive nights. **Check-in is 14:00, check-out 12:00.** The plan's read —
that California hike/bike sites are normally walk-up, so it would probably be
fine — does not hold for this park. Book it on ReserveCalifornia
(**800-444-7275**) before leaving, or ride to a fallback. Camping here reopened
**1 April 2026** after the slide closures.
([source](https://www.parks.ca.gov/?page_id=31154))

**3. Highway 1 is open — and there is a signal-controlled hold you will sit in.**
Highway 1 reopened through Regent's Slide on **14 January 2026**, about 90 days
early, after an $82 million repair; Caltrans calls the slope stable and monitors
it continuously. But as of August 2026 there is **one-way, signal-controlled
traffic at Rocky Creek Bridge, 24/7 through 31 August, with delays up to 15
minutes** — that is at **km 283.8 of day 1**, and you will be stopped in it.
Check [QuickMap](https://quickmap.dot.ca.gov) the morning you leave.
([reopening](https://www.gov.ca.gov/2026/01/14/governor-newsom-announces-early-reopening-of-highway-1-through-big-sur/),
[conditions](https://www.bigsurcalifornia.org/highway-1-conditions/))

**4. Devil's Slide may be gated shut when you get there.** Bicycles are banned
from the Tom Lantos Tunnels, so the Devil's Slide Trail is the only legal way
past — and San Mateo County publishes an **08:00 opening for the parking lots**
while publishing **no trail-access hours at all**, telling you to contact the
department. A 05:00 departure reaches the trail at **km 33.8, around
06:30–07:00**. If it is locked there is no legal alternative on that line, so
this repo now ships an **inland bypass** that costs essentially nothing:

| | Distance | Climb | Devil's Slide |
|---|---:|---:|---|
| Main line (coast + Devil's Slide Trail) | 326.4 km | +3,642 m | passes through it |
| [`pch_day1_alt_inland_bypass.gpx`](./gpx/pch_day1_alt_inland_bypass.gpx) | **326.2 km** | +3,745 m | **stays 7.7 km clear** |

Skyline Boulevard (CA-35) down the peninsula ridge to CA-92 and over into Half
Moon Bay is **0.2 km shorter** than the coast and only ~100 m hillier. It cannot
be gated. Call the county; if you get no answer, take the bypass.
([trail hours](https://www.smcgov.org/parks/devils-slide-trail-hours))

---

## The alternative endpoints, as files

Day 1 has four possible finishes and day 2 has three, so each is a complete
stage file rather than a note to improvise from.

| File | Finish | Day distance | Climb |
|------|--------|-------------:|------:|
| [`pch_day1_alt_pfeiffer.gpx`](./gpx/pch_day1_alt_pfeiffer.gpx) | Pfeiffer Big Sur SP (55 km short) | 282.1 km | +2,558 m |
| [`pch_day1_alt_lucia.gpx`](./gpx/pch_day1_alt_lucia.gpx) | Lucia Lodge (indoor, 10 rooms) | 322.9 km | +3,592 m |
| **`pch_day1_sf_limekiln.gpx`** | **Limekiln SP (the plan)** | **326.4 km** | **+3,642 m** |
| [`pch_day1_alt_17mile.gpx`](./gpx/pch_day1_alt_17mile.gpx) | Limekiln, via 17-Mile Drive | 340.0 km | +3,663 m |
| [`pch_day1_alt_raggedpoint.gpx`](./gpx/pch_day1_alt_raggedpoint.gpx) | Ragged Point Inn (indoor, 39 rooms) | 363.6 km | +4,399 m |
| [`pch_day1_alt_sansimeon.gpx`](./gpx/pch_day1_alt_sansimeon.gpx) | San Simeon motels | 396.2 km | +4,498 m |
| [`pch_day2_alt_gaviota.gpx`](./gpx/pch_day2_alt_gaviota.gpx) | Gaviota SP (16 km earlier) | 284.8 km | +2,296 m |
| **`pch_day2_limekiln_refugio.gpx`** | **Refugio SB (the plan)** | **302.7 km** | **+2,377 m** |
| [`pch_day2_alt_elcapitan.gpx`](./gpx/pch_day2_alt_elcapitan.gpx) | El Capitán SB (3 km later) | 305.3 km | +2,398 m |

Two consequences worth reading off that table. **Ragged Point costs 37 km more
than Limekiln, not the 72 km the plan implied** (the plan compared it against a
280 km day 1 that does not exist). And **17-Mile Drive costs 13.6 km** — the main
line now goes direct from Monterey to Carmel (9.9 km, including 0.5 km of
CA-1 shoulder that OSM marks bicycle-legal) instead of round the peninsula
(23.5 km), because day 1 has no spare distance to give away.

---

## The profile, and why the stock one fails here

Geometry comes from BRouter using [`scripts/velo_pch_road.brf`](./scripts/velo_pch_road.brf),
a retuned copy of the stock `trekking` profile. Four changes, each of which was
forced by an actual wrong route observed while building:

**1. Highway 1 *is* the cycle route.** Trekking charges 10.0 for a trunk road and
3.0 for a primary without a bike hint. CA-1 is variously tagged trunk, primary
and secondary along its length, so those penalties push the line onto inland farm
roads. Here all three sit near 1.0, just above a cycleway so a parallel bike path
still wins in town.

**2. No elevation avoidance** (`consider_elevation = false`). With it on, BRouter
tries to flatten the route, and the cheapest way to flatten San Francisco → Los
Angeles is to abandon the coast for the Salinas Valley. Big Sur's climbing is the
point, not a cost.

**3. Freeway in three tiers.** `bicycle=no` is excluded; `bicycle=yes|designated`
costs 2.0; **untagged** freeway costs 2.6 — allowed, but only when the
alternative is absurd. That middle tier is not optional: OSM's freeway bicycle
tagging on this coast is patchy, and with untagged freeway banned outright the
router answered the 5 km hop from El Capitán to Goleta by **crossing the Santa
Ynez Mountains — 75 km, +1,504 m, over a 695 m pass, with 5.3 km of unpaved
track.**

**4. Pavement only.** Gravel, dirt, sand, grass and tracktype grade2+ are
penalised hard (grade4/5 excluded), and the cycle-route bonus no longer applies
to unpaved ways — otherwise a dirt path tagged `lcn` gets a flat cost of 1.0 and
beats the paved highway beside it.

`bicycle=no` is **excluded outright**, not discounted. Stock trekking charges
only 4 when a bike-banned way still allows pedestrians ("you may push your
bike"), which routed this trip straight through the Tom Lantos Tunnels. An
intermediate experiment — making it merely expensive rather than forbidden —
immediately put 510 m of bike-banned trail inside Point Lobos into day 1, which
is why it is a hard ban now.

> **A trap for whoever edits the profile next:** every tag *value* you write must
> exist in BRouter's `lookups.dat`, or the profile is rejected at route time with
> a bare **HTTP 500 and an empty body**. `chipseal`, `concrete:plates`,
> `concrete:lanes`, `unhewn_cobblestone` and `woodchips` are **not** in it.
> `smoothness=very_good` is.

### The one deliberate exception: 391 m

OSM begins the US-101 `bicycle=no` run about **1 km west of the Winchester Canyon
off-ramp** (verified against Overpass: 196 US-101 ways tagged `bicycle=no`
between Gaviota and Ventura, the westernmost at `34.4339,-119.9147`). Taken
literally there is **no legal bicycle path at all** from the Gaviota coast into
Goleta, and the router's answer is the 85 km mountain crossing above.

Cyclists ride that shoulder in practice — it is the Adventure Cycling Pacific
Coast alignment, and the reported hazard is the narrow *southbound* bridge near
the Baron Ranch trailhead, not the shoulder. So exactly one leg, named in
`pch_waypoints.PERMISSIVE_LEGS`, is routed with
[`scripts/velo_pch_road_bridge.brf`](./scripts/velo_pch_road_bridge.brf) — a copy
identical but for allowing `bicycle=no` at a cost of 8. It uses **391 m** of
disputed freeway and saves **77 km**. Leave 101 at the Winchester Canyon off-ramp
and take Calle Real / Hollister Ave into Goleta; **if signage on the day says
otherwise, obey the signage.**

Everywhere else the ban holds. US-101 **is** genuinely closed to bicycles from
Santa Barbara to Ventura, and day 3 obeys that — it runs on city streets, county
roads and the ocean-side paths through Carpinteria and the Rincon, with zero
bike-banned metres.

---

## Validation

Re-read independently from the saved GPX by
[`scripts/validate_pch_routes.py`](./scripts/validate_pch_routes.py), which
re-parses the XML and recomputes distance from the coordinates rather than
trusting the builder.

| Check | Result |
|-------|--------|
| XML well-formed, GPX 1.1, has trackpoints | ✅ all 11 files |
| Continuity (largest single jump) | ✅ **299 m** worst case — tracks are simplified to 2.5 m then re-densified to ≤ 300 m |
| Every corridor waypoint on its own track | ✅ worst offset **244 m** |
| Seam day 1 → day 2 / day 2 → day 3 | ✅ **1.2 m** / **0.0 m** |
| Recomputed distance vs. build summary | ✅ within 2% |
| Master file reproduces the three per-day files | ✅ 3 tracks, 858.0 km |
| **Freeway not marked bicycle-legal** | ✅ **0.000 km** |
| **`bicycle=no`** | ✅ **0.391 km**, all of it the documented Winchester Canyon gap |
| Unpaved (worst stage) | ✅ **0.22 km** — 190 m of it the Santa Monica Pier boards |
| Ferries / steps | ✅ 0.0 km |
| Tunnels | 0.23 km, both `highway=cycleway bicycle=designated` (Rincon path, Santa Monica underpass) |
| Every waypoint has a name and a description | ✅ |

Machine-readable: [`data/pch_route_summary.json`](./data/pch_route_summary.json)
(per-stage audit, every flagged way with coordinates and tags, detected climbs,
cue sheet) and [`data/pch_validation.json`](./data/pch_validation.json).

### Bugs this validation caught while building

Worth recording, because all four would have shipped silently:

- **Garrapata State Park** — the geocoded park centroid sits **1.2 km inland at
  540 m**. As a via-point it dragged the line 6.8 km up Garrapata Canyon and
  added 585 m of climbing. Removed; Highway 1 is unambiguous there anyway.
- **Piedras Blancas light station** — routing to it fails outright (`no track
  found`): the headland access road is a disconnected private way in OSM.
- **Three via-points snapped off the highway onto dirt** — Piedras Blancas
  (1,964 m), the elephant seal vista car park (349 m) and San Simeon Acres
  (2,590 m of `surface=dirt` path). All three demoted to waypoints.
- **Sunset State Beach** — a spur off San Andreas Road, costing 5.4 km
  out-and-back for nothing.

Geocoders are genuinely hostile on this corridor, which is why
[`scripts/pch_waypoints.py`](./scripts/pch_waypoints.py) carries explicit
coordinates: *"Monterey, California"* resolves 10 km from the city, *"San Luis
Obispo, California"* lands **41 km inland**, *"Harmony, California"* comes back
**434 km away** in San Diego County, and every Amtrak-station query collapses
onto Guadalupe.

---

## The climbs, measured from the route's own elevation profile

Detected by walking the smoothed profile (`detect_climbs`), not from memory —
which is how the summit of Hurricane Point fell out at `36.3583,-121.9006`
without being told it exists.

| Day | km | Climb | Length | Gain | Summit |
|-----|---:|-------|-------:|-----:|-------:|
| 1 | 30.1 → 33.3 | **Devil's Slide Trail** | 3.19 km | +137 m | 142 m |
| 1 | 209.7 → 220.8 | out of Monterey Bay to Carmel | 11.12 km | +171 m | 183 m |
| 1 | 252.4 → 255.3 | **Hurricane Point** (after Bixby Bridge) | 2.90 km | +130 m | 164 m |
| 1 | 265.2 → 279.0 | the long drag to Pfeiffer Big Sur | 13.85 km | +147 m | 155 m |
| 1 | 279.9 → 283.4 | **Grimes Point / Nepenthe** — day 1's biggest | 3.47 km | +209 m | 298 m |
| 1 | 297.6 → 299.6 | the two steep pitches south of McWay Falls | 1.9 km | +281 m | 339 m |
| 2 | 22.4 → 29.8 | south of Gorda toward Ragged Point | 7.42 km | +200 m | 243 m |
| 2 | 32.4 → 35.1 | the **Ragged Point** climb | 2.69 km | +143 m | 244 m |
| 2 | 254.8 → 275.5 | **CA-1 over the Santa Rosa Hills** (Lompoc → Las Cruces) | 20.72 km | +272 m | 328 m |
| 3 | — | nothing over 110 m all day | — | +781 m total | — |

Gains are SRTM-derived. **Treat the gradients on the Big Sur cliffs with
suspicion** — SRTM's 30–90 m posting misreads a road cut into a cliff face, which
is why two short pitches south of McWay come out at 13–16%. The *gains* are
about right; the *percentages* there are not.

---

## Water and food — where you actually run dry

`harvest_pch_pois.py` queries Overpass with an `around` clause against the routed
line itself, so everything it returns is genuinely beside the road, then measures
the longest run with **no water and no shop**, counting only POIs within 400 m of
the line (a supermarket 2 km inland is not resupply when you are chasing
daylight).

| Day | On-road resupply points | Longest dry stretch | Where it starts |
|-----|------------------------:|--------------------:|-----------------|
| 1 | 220 | **34.5 km** | km 55.3 — **south of Half Moon Bay**, not Big Sur |
| 2 | **75** | **34.3 km** | km 250.4 — **Lompoc → Las Cruces** over the Santa Rosa Hills |
| 3 | 170 | 20.3 km | km 119.5 — the Oxnard/Point Mugu coast |

Day 2 has **a third** the on-road resupply of the other two days across a longer
distance — it is the day to carry food on, not day 1.

Two of those are worth internalising. **Big Sur is not day 1's problem** — Big Sur
Village, Big Sur Station, Nepenthe, Lucia and the campgrounds keep the gaps under
30 km. The San Mateo coast between Half Moon Bay and Pigeon Point is worse,
because Pescadero and San Gregorio sit inland off the highway.

And day 2's worst stretch reproduces, from OSM data alone, exactly what touring
cyclists say about that road: *"there are very few opportunities for water or food
between Lompoc and Santa Barbara. The rest stop at Gaviota is the best place to
water up."* Fill up in Lompoc at km 257.

## Two more live hazards worth knowing

**PCH through Malibu is an active fire-rebuild corridor.** The last ~25 km of day
3 runs through the Palisades Fire reconstruction. Caltrans District 7 has a
rock-slope-protection and pavement rebuild near Ratner Beach due to finish
**Fall 2026**, and a second project covering about five miles from just south of
the California Incline to Topanga Creek due **end of 2026** — both still live in
August 2026. After the fire, PCH reopened with **one lane each way at 25 mph**.
Expect no shoulder and construction traffic exactly where you are most tired. The
route already leaves PCH at Santa Monica Pier and turns inland via Culver City,
so the exposure is Malibu → Santa Monica only; if it looks bad, quit at Oxnard or
Ventura and take the Surfliner in.
([source](https://dot.ca.gov/caltrans-near-me/district-7/district-7-projects/pch-palisades-fire-repairs))

**Vandenberg can close the road on a few hours' notice.** Day 2 passes Vandenberg
Space Force Base on CA-1. Launch operations close roads around the base — a
documented case shut **CA-246 between CA-1 and Mission Gate Road from 10:00 to
15:00 on 2 March 2026** for a launch that then scrubbed. That closure was on
CA-246, *not* on this route's CA-1 line, but CA-1 has been closed here for base
incidents and carries ongoing roadwork near Vandenberg Village and Santa Lucia
Canyon Road. Check the launch schedule against your date; there is no good detour
— the inland alternative is US-101 via Santa Maria and Los Alamos.

## Sleeping, with sources

| Place | km | What's confirmed |
|-------|---:|------------------|
| **Limekiln SP** (night 1) | d1 326.4 | Hike/bike **$5**, arrive on foot/bike only, max 2 nights. Fresh water, token hot showers ($1/5 min), toilets. Check-in 14:00. Sites 1–29. **Reservation required — no FCFS.** Reopened 1 Apr 2026. ([src](https://www.parks.ca.gov/?page_id=31154)) |
| Kirk Creek CG (USFS) | d2 3.5 | 3.5 km *south* of Limekiln, ocean bluff at Nacimiento-Fergusson Rd. recreation.gov. **Verify water** — historically none. |
| Plaskett Creek CG (USFS) | d2 12.5 | Across CA-1 from Sand Dollar Beach. recreation.gov. |
| Pfeiffer Big Sur SP | d1 311.0 | The short-day fallback, 55 km before Limekiln. Full facilities, stores nearby. |
| **Refugio SB** (night 2) | d2 302.7 | 10 Refugio Beach Rd, Goleta 93117. Hike/bike sites confirmed; drinking water, restrooms/showers, **camp store**. Open Aug 2026. **(805) 968-1033.** ([src](https://www.parks.ca.gov/refugio)) |
| Gaviota SP | d2 293.0 | Hike/bike sites, water, showers, store. Open Aug 2026, reservable. Windy. |
| El Capitán SB | d3 2.6 | Most services of the three. Reported FCFS on middle/upper loops through 28 Jun 2026 — verify for August. |

**Still unverified, and worth a phone call:** neither Refugio's nor Gaviota's
park page publishes a **per-person hike/bike rate**, so the plan's *$10/person*
is unconfirmed — ring **(805) 968-1033**. Kirk Creek's and Plaskett Creek's
hiker/biker arrangements are USFS policy, not State Parks policy, and differ.
Treebones' two-night minimum and Gorda Springs' phone number both came from the
transcript, not from the operators.

---

## Before you leave — the checks that actually matter

1. **Book Limekiln.** ReserveCalifornia, **800-444-7275**. There is no walk-up.
2. **Call San Mateo County Parks** about Devil's Slide Trail access before 08:00.
   No answer → load `pch_day1_alt_inland_bypass.gpx`; it costs you 0.2 km.
3. **[QuickMap](https://quickmap.dot.ca.gov)** the morning you go — Rocky Creek
   Bridge one-way control runs through 31 Aug, and Big Sur controls move.
4. **Ring (805) 968-1033** for the Refugio hike/bike rate and to sanity-check
   arrival after dark.
5. **Check the Vandenberg launch schedule** against your date — CA-1 past the base
   can shut at a few hours' notice, and the only detour is US-101 inland.
6. **Book the bike on the train home.** Coast Starlight roll-on space out of LA
   Union Station is limited and sells out; the bike is a separate reservation.
7. **Fill up in Lompoc (km 257 of day 2).** The next 34 km over the Santa Rosa
   Hills has nothing; the Gaviota rest area is the next reliable water.
8. **Do the day-1 arithmetic honestly.** 326 km, +3,642 m, sunrise-to-after-dark,
   with a 15-minute enforced stop at km 284 and the cliffs in the last 80 km.
   Pfeiffer Big Sur at km 311 is the graceful out; use it rather than descending
   Big Sur in the dark.

## Reproduce

```bash
python3 scripts/build_pch_route.py      # gpx/pch_*.gpx + data/pch_route_summary.json
python3 scripts/harvest_pch_pois.py     # gpx/pch_waypoints.gpx + data/pch_pois.json
python3 scripts/validate_pch_routes.py  # data/pch_validation.json, non-zero exit on failure
```

BRouter and Overpass responses are cached under `scripts/.cache/`, so re-runs are
free and reproducible. `PROFILE_CACHE_KEY` in `build_pch_route.py` must be bumped
whenever a `.brf` changes, or you will get stale geometry back — that mistake
cost an hour during this build. Overpass's main instance times out almost always;
`harvest_pch_pois.py` falls through a mirror list.

### Caveats

- Geometry is OpenStreetMap via BRouter. Tag auditing is only as good as OSM's
  tagging, which is exactly why the Winchester Canyon exception exists and is
  documented rather than hidden.
- Live conditions were checked on **4 August 2026** and are perishable. Road
  status, campground status and trail gates all move.
- The route ends at LA Union Station because that is where the train home is. If
  the finish should be somewhere else, only day 3's tail changes.
