# 🧭 Extending the trip — San Diego, and what beats it

You asked whether pushing on to San Diego is a good idea, or whether something
else is better. This is the answer with the routing actually done, because
"is it a good idea" turns on numbers that are easy to guess wrong: I built every
candidate with the same profile and audit as the main route rather than reasoning
about them from a map.

## Short version

**San Diego works, and it's the only extension that needs no new bookings — but
it's the least scenic riding of the trip.** Note *scenic*, not badly built: it's
an official signed route (US Bicycle Route 95) with a quarter of the day on
separated bike path, and one 27 km hole where a Marine Corps base owns the coast. The Camp Pendleton problem has exactly one solution — the Caltrans-permitted
I-5 shoulder — and the base pass turns out to be a dead letter for a southbound
rider (see below). If what you want is *more good riding* rather than a longer
line on a map, **prepending the Sonoma/Mendocino coast beats it comfortably** —
but it needs a bus with a bike space, which is a real ask two days out.

| Extension | Distance | Climb | Verdict |
|---|---:|---:|---|
| **Day 4: LA → San Diego** | **218.2 km** | **+685 m** | ✅ Built. Easiest bolt-on, no bookings. Best *infrastructure* of the trip (USBR 95, 25% separated path); worst *scenery*. |
| Day 5: San Diego → Mexican border | +26.0 km | +31 m | ✅ Built. Only worth it if you're already in San Diego. |
| **Prepend: Leggett → SF** | **357.2 km** | **+4,301 m** | 🥇 Best riding by far, and tailwind-correct. Needs a Thruway bus with bike space. |
| Prepend: Bodega Bay → SF | 114.8 km | +1,284 m | 🥈 Half a day, most of the quality, far easier logistics. |
| Prepend: Point Reyes → SF | 67.0 km | +877 m | 👍 Nearly free prologue, genuinely good coast. |
| Loop home inland (LA → SF) | 779.4 km | +3,175 m | ❌ **No.** See below — this is a heat-injury risk, not a hard day. |

Adding day 4 makes the trip **1,000.6 km over 4 days** (297 / 279 / 206 / 218),
which is the same shape you already have — day 4 is *flatter* than day 3.

---

## The San Diego extension

**Files:** [`pch_day4_la_sandiego.gpx`](./gpx/pch_day4_la_sandiego.gpx) ·
[`pch_day5_sd_border.gpx`](./gpx/pch_day5_sd_border.gpx) ·
[`pch_sf_sd_master.gpx`](./gpx/pch_sf_sd_master.gpx) (all four days in one file —
the LA-only master is untouched, so loading the extension stays a decision)

Union Station out on the Los Angeles River path to Long Beach, the Orange County
beach cities, Camp Pendleton, then the San Diego North County coast to Santa Fe
Depot.

**What the audit says:** 0 unpaved metres, 0 bike-banned metres, 0 permit-gated
metres, 607 m of out-and-back. **54.6 km of it — 25% — is protected bike path**,
which makes it the most sheltered day of the entire trip. The only climb over
60 m all day is **Torrey Pines: 4.84 km at 2.6% to 132 m**. Total climbing for
218 km is +685 m.

It is also, by some distance, the **best-supplied** day. The POI harvest found
**463 on-route POIs including 113 drinking-water taps and 38 bike shops**, and the
longest stretch with no water and no shop is **15.6 km** — against 37.0, 43.0 and
20.3 km on days 1, 2 and 3. If something breaks, you are never far from a shop:

| Day | On-route POIs | Bike shops | Longest dry stretch |
|---|---:|---:|---:|
| 1 SF → Limekiln | 382 | — | 37.0 km |
| 2 Limekiln → Refugio | 180 | — | **43.0 km** |
| 3 Refugio → LA | 303 | — | 20.3 km |
| **4 LA → San Diego** | **463** | **38** | **15.6 km** |

### To be clear: this corridor *is* properly built for cycling

An earlier draft of this file said day 4 was the "least interesting riding," which
reads as though the corridor is badly served. It isn't — those are two different
claims and only the aesthetic one is true.

LA → San Diego is **US Bicycle Route 95**, an official signed national route. OSM
carries **195 bicycle route relations** in the corridor — 5 national, 13 regional,
158 local — including the **Los Angeles River Greenway**, **Rio Hondo**, **San
Gabriel River Greenway**, **Coyote Creek Bikeway**, **Santa Ana River bike path**,
the **OC Loop** and the **California Coastal Trail**.

| | Day 4 |
|---|---:|
| On a signed cycle network (icn/ncn/rcn/lcn) | **73.5%** (160.2 km) |
| …excluding the Camp Pendleton freeway hop | **77.8%** of 190.9 km |
| Separated bike path (`highway=cycleway`) | **54.6 km — 25% of the day** |
| Car-free altogether (cycleway + path + pedestrian) | ~59 km |
| Bike shops within 1.2 km of the line | **38** |
| Longest stretch with no water and no shop | **15.6 km** — best of the four days |

That 25% on separated path is **more dedicated infrastructure than any other day
of this trip**, and the resupply density is the best of the four. The 73.5%
network figure is the lowest of the four days only because the 27 km Pendleton
freeway bypass is 12.5% of the day by itself; take that out and it sits at 77.8%,
in line with days 1–3 (91.5 / 86.6 / 83.1%).

**So the corridor has exactly one hole in it, and it is not a planning failure —
it is a Marine Corps base.** 27 km where the coast is Camp Pendleton and there is
no public road at all. No route design fixes that. Everything either side of it is
about as purpose-built for a bicycle as American road cycling gets.

What is genuinely true is the *aesthetic* judgement: Orange County beach cities
are not Big Sur. That's a statement about scenery, not about whether anyone
bothered to build a path.

### Camp Pendleton: the crux, and why the pass is a dead letter

27 km of the coast between San Onofre and Oceanside is Marine Corps base with no
public road. **This is the only genuine hole in the corridor, and there is exactly
one way through it for you: the I-5 shoulder.** The base pass looked like an
option; it isn't, on three separate counts.

**1. Getting the pass means being at the wrong end of the base.** The DBIDS
Recreational Bicycle pass is issued **in person only**, with a photograph,
fingerprint and criminal background check, at the Visitor Center — **20250
Vandegrift Blvd, Oceanside**, **Mon–Fri 07:30–15:30**, valid one year. That is the
**south** end. A southbound rider reaches the base at the north end. There is a
[DBIDS pre-enrollment portal](https://dbids-global-enroll.dmdc.mil/), but it
submits your details early; it does not replace the in-person biometric capture.
([base access](https://www.pendleton.marines.mil/Staff/Principal-Staff/Security-and-Emergency-Services/Base-Access/))

**2. Even with the pass, it doesn't cover the direction you're coming from.** The
bicycle route it grants is defined **Las Pulgas gate ↔ Main gate** — the *southern*
half of the base. It does not include the San Onofre approach at all.

**3. The corridor north of the gate is rideable, but you cannot get past the gate
without credentials.** *(Corrected — an earlier version of this file called it a
dead end, which is wrong.)* The old highway through San Onofre Bluffs is genuinely
open: Overpass shows **Old Pacific Highway** as `access=permissive, bicycle=yes` and
the **Pacific Coast Bikeway** as `highway=cycleway, bicycle=yes, foot=yes`. And it
does **not** dead-end — **US Bicycle Route 95 is designated straight along it**,
continuing into Oceanside on North Pacific Street and Harbor Drive. It is a
through route, and a national one.

What stops you is the gate, not the geography. Its only southern link onto I-5 at
Las Pulgas is **80 m of `access=permit` road**, and base access has required a
DBIDS pass since 1 October 2018. A nogo-radius sweep over that link — 20, 35, 50,
80, 120, 200 m — produced **the full 27 km of I-5 every single time**, because
BRouter has no legal way past it.

| Nogo radius over the 80 m gate | Route | Freeway | Bike path |
|---:|---:|---:|---:|
| none (gate open) | 30.05 km | 12.25 km | 5.08 km |
| 20 m … 200 m (all identical) | 29.64 km | **27.16 km** | 0 km |

**So: the I-5 shoulder is not a fallback, it is the route.** Caltrans permits
bicycles between Basilone Road and Oceanside (exits 62–54); there is water,
restrooms and vending at the Aliso Creek rest area partway. 27 km of freeway
shoulder is the least pleasant riding on the whole trip, and it is also the only
legal way a bicycle gets from Los Angeles to San Diego along the coast.
([route notes](https://visitoceanside.org/blog/bike-to-san-onofre-state-park/))

There *was* a `pch_day4_alt_pendleton.gpx` here. **It is deleted** — it depended on
a gate you cannot get through, and keeping it invited riding 150 km into a day and
finding out.

#### An audit limitation worth knowing about

BRouter's routing data **does not carry `permit` at all** — `permit` is not a value
in its `lookups.dat`, so neither the profile nor the audit can see it. Overpass
shows Camp Pendleton's **Stuart Mesa Road** and **Vandegrift Boulevard** tagged
`bicycle=permit` across every one of their 17 and 19 ways; BRouter would route a
bicycle onto them without complaint. The 80 m this audit *did* catch showed up only
because that particular way spells it `access=permit`, which survives as raw text
in the echoed tags. The audit now checks both spellings, but the honest position is
that **permit restrictions on this route cannot be verified from BRouter output** —
they were established from Overpass, by hand, and this is the note that says so.

### The border, if you're going to be there anyway

[`pch_day5_sd_border.gpx`](./gpx/pch_day5_sd_border.gpx) adds **26.0 km** from
Santa Fe Depot to **Border Field State Park**, where the Pacific Coast Bike Route
ends at the Mexican border. Flat, and the only way to say you rode the whole
thing.

One trap: **bicycles cannot use the San Diego–Coronado Bridge.** The nicer line is
the ferry from Broadway Pier and then the Silver Strand bike path — 24.8 km
including a 2.4 km boat — but the GPX goes round the bay through National City and
Chula Vista instead (26.0 km) because that has no dependency on a timetable. Ride
to the ferry terminal if you want the Strand. A Coronado via-point with ferries
disabled, incidentally, produced a 54 km route with **49 km of out-and-back** —
caught by the spur check that went in last round.

Border Field's access road floods and closes regularly; be ready to turn around
at Imperial Beach.

---

## What beats it: prepend the Sonoma/Mendocino coast

**Leggett → San Francisco: 357.2 km, +4,301 m** — measured with the same
profile: 0 unpaved, 0 bike-banned metres.

This is the stretch that people who have ridden the whole Pacific Coast route
remember: the Lost Coast approaches, Leggett Hill, the Mendocino headlands, the
Sonoma coast cliffs through Jenner and Bodega. It is Big Sur–grade riding, and
unlike San Diego it is **more** of what you're already going for rather than less.
It's also **tailwind-correct** — you ride it southbound, into your existing trip,
rather than fighting the prevailing north-westerly.

**The logistics are the whole question.** You have to get north with the bike
first. The **Amtrak San Joaquins Thruway Bus Route 7** serves Humboldt County to
Martinez and **stops at Leggett**, plus Willits, Ukiah and Laytonville. Bikes are
carried in the luggage bay **subject to space, first-come-first-served** — not a
reservation. Two days before departure, that is a real risk: turning up at a bus
with no bike space strands you.
([MTA connections](https://mendocinotransit.org/connections/) ·
[Amtrak Thruway](https://www.amtrak.com/california-thruway-buses-reach-hot-vacation-spots))

**Cheaper versions of the same idea**, both of which you can ride to from home
with no bus at all:

- **Bodega Bay → SF: 114.8 km, +1,284 m.** Half a day, and it keeps the best of
  the Sonoma coast.
- **Point Reyes → SF: 67.0 km, +877 m.** A prologue rather than a stage, over the
  Golden Gate and through Marin. Nearly free, still excellent.

---

## What not to do: loop home inland

Measured, so it can be dismissed with a number rather than a shrug:
**LA → Santa Clarita → Bakersfield → Fresno → Modesto → Livermore → SF is
779.4 km and +3,175 m** — as long as the entire southbound trip, to avoid one
train.

And it goes up the Central Valley in August. For **early August 2026** the
forecast for Fresno was **an 11-day run of triple digits, 103–108°F (39–42°C)**,
with NWS Hanford warning of moderate-to-major heat risk across the Highway 99
corridor. That is not a hard day on the bike; it is a heat-injury exposure with
no shade and no bail-out for 200 km stretches.
([GV Wire / NWS Hanford](https://gvwire.com/2026/07/30/triple-digits-here-to-stay-in-fresno-with-highs-up-to-108/))

---

## My call

**Given that you leave in a day or two: take San Diego.** It's the only option
that needs no new booking, it's a genuine 1-day add at a distance you're already
riding, the Pendleton problem is solved for free, and it gives you an airport 5 km
from the finish line. Ride it in one day; don't plan on camping between LA and
San Diego, because the hiker/biker sites there are largely gone.

**If you had another week of lead time, I'd tell you to skip it and prepend
Leggett → SF instead.** 357 km of the best coast on the west side of the
continent beats 218 km of Orange County, and it points the same direction as the
rest of your trip. The only thing standing in the way is a bus with an
unreserved bike space.

**Cheap middle path:** ride **Point Reyes → SF** (67 km) as a shakedown prologue
the day before you leave, then do the core three days, then decide about San
Diego when you actually get to Los Angeles and know how your legs are. Nothing
about the extension has to be committed in advance — that is its real advantage.

---

*All distances measured from the built GPX by
[`scripts/validate_pch_routes.py`](./scripts/validate_pch_routes.py), not
estimated. Alternatives were routed with the same profile to make the comparison
like-for-like; the ones that are not built as files
(Leggett/Bodega/Point Reyes/inland) were routed and measured but not saved,
because they are a decision, not a plan. Live conditions checked 4 August 2026.*
