# North Coast out-and-back — 12–13 August 2026

Kian rode from San Francisco to the Manchester area on 12 August and returned
on 13 August. This was a completed two-day ride, not the full planned
San Francisco↔Leggett route.

## Bottom line

- **457.656 km in 23:08:15 recorded time**, with about **5,045 m of derived
  ascent**.
- The effort was overwhelmingly low-heart-rate endurance: **97.1% of recorded
  time was below 138 bpm**. The stress came from duration, not sustained high
  intensity.
- The return-day finish was real: the final **62.9 km averaged 21.04 km/h while
  moving with only 75 seconds under 3 km/h**. The sharpest surge was km 175–200,
  at **23.25 km/h**.
- Wind explains part, not all, of that finish. The km 165–190 surge had a
  modeled mean **1.85 m/s tailwind component**. The final 38 km were mixed and
  crosswind-heavy rather than a clean tailwind conveyor belt.
- Day 1 may have been adequate in total calories, but the reported **~2,500
  kcal of almonds** was mainly fat and fiber, not rapid ride carbohydrate.
  Day 2's large meal after arriving home helps recovery and 48-hour energy
  balance; it cannot retroactively fuel the preceding ride hours.
- Polar later confirmed the post-Day-2 night was very poor: **4:20:30 asleep**,
  Nightly Recharge 1, **ANS −10.0**, sleeping HR **70** and HRV **20 ms**. An
  easy 13.677 km run later that morning added another 66.6 cardio load rather
  than supplying a recovery day.

## Recorded totals

| | Day 1: northbound | Day 2: southbound | Total |
|---|---:|---:|---:|
| Polar exercise ID | `0G4aG4Ye` | `y1DBXDj3` | — |
| Distance | 229.729 km | 227.927 km | **457.656 km** |
| Polar recorded time | 11:23:31 | 11:44:44 | **23:08:15** |
| Moving time, derived | 11:01:52 | 11:13:01 | **22:14:53** |
| Under 3 km/h, derived | 21:37 | 30:54 | **52:31** |
| Gross speed | 20.17 km/h | 19.41 km/h | **19.78 km/h** |
| Moving speed | 20.83 km/h | 20.32 km/h | **20.57 km/h** |
| Average / maximum HR | 114 / 163 bpm | 106 / 160 bpm | **~110 bpm average** |
| Polar exercise calories | 5,511 kcal | 5,011 kcal | **10,522 kcal** |
| Polar cardio load | 432.6 | 344.1 | **776.7** |
| Derived ascent | 2,492 m | 2,554 m | **5,045 m** |

Moving time uses a **3 km/h speed threshold**. It is therefore time moving by
that definition, not a field independently supplied by Polar. Ascent is
derived from Polar's barometric-altitude stream after resampling every 25 m and
applying a 225 m centered smoothing window; it is not a Polar-provided total.
The derived stream covers 51 seconds less than the two API durations combined
(2 seconds on Day 1 and 49 seconds on Day 2), principally because Day 2's GPS
route begins 48 seconds after the exercise. Therefore moving plus under-threshold
time does not sum exactly to the API total.

## How the rides broke into phases

The boundaries below are descriptive changes in pace, terrain, stops, heart
rate and wind. They are more useful than pretending that either 230 km day was
one uniform effort.

### Day 1 — San Francisco to Manchester area

| Ride km | Character | Moving speed | Moving HR | Derived climb | Under 3 km/h |
|---:|---|---:|---:|---:|---:|
| 0–40 | Settling in through Marin | 20.45 km/h | 116.5 | 443 m | 3:27 |
| 40–85 | Fastest sustained block | **25.54 km/h** | 117.7 | 297 m | **0:00** |
| 85–145 | Hardest internal-load block | 20.63 km/h | **122.3** | **799 m** | 2:14 |
| 145–190 | Slower coastal grind | 19.90 km/h | 109.9 | 533 m | 3:13 |
| 190–205 | Long interruption near km 195 | 19.05 km/h | 110.5 | 167 m | **10:40** |
| 205–230 | Final adverse-wind grind | 18.23 km/h | 105.7 | 252 m | 2:03 |

The apparent fade after km 145 was not just physiological. The modeled wind
turned materially adverse, and the final 30 km were the worst wind block of the
entire trip.

### Day 2 — Manchester area to San Francisco

| Ride km | Character | Moving speed | Moving HR | Derived climb | Under 3 km/h |
|---:|---|---:|---:|---:|---:|
| 0–20 | Clean start | 21.00 km/h | 109.3 | 236 m | 1:05 |
| 20–35 | Morning interruption | 20.17 km/h | 98.7 | 148 m | **22:03** |
| 35–70 | First fast block | **23.77 km/h** | 109.3 | 357 m | 1:59 |
| 70–85 | Short climbing slowdown | 17.32 km/h | 107.1 | 309 m | 0:00 |
| 85–165 | Longest slow/adverse block | 19.09 km/h | 105.4 | **897 m** | 4:32 |
| 165–228 | Sustained late resurgence | **21.04 km/h** | **110.8** | 607 m | **1:15** |

The fastest 25 km late in the ride was km **175–200: 23.25 km/h moving at
110.2 bpm**. The literal last 5 km were not the fastest; they averaged 18.8
km/h moving. The right description is a strong final **~63 km**, especially
km 175–200, rather than a finishing sprint.

The final 50 km averaged **21.06 km/h moving and 20.95 km/h gross**, with only
45 seconds under 3 km/h. Its gross pace ranked around the **79th percentile**
of all rolling 50 km windows on Day 2, while moving pace ranked around the 58th
percentile. The standout trait was relentless forward progress, not the ride's
highest raw speed.

## Wind reconstruction

Weather was reconstructed against the exact GPS time and position using NOAA
HRRR through the Open-Meteo Historical Forecast API. Wind vectors were
interpolated in time and space, projected onto a centered ~200 m riding
heading, and stopped minutes were excluded. Positive longitudinal wind is a
tailwind; negative is a headwind.

| | Day 1 | Day 2 |
|---|---:|---:|
| Mean wind speed | 2.84 m/s | **3.61 m/s** |
| Mean longitudinal component | **-0.79 m/s** | **-0.34 m/s** |
| Headwind / neutral / tailwind time | 40.0% / 38.3% / 21.7% | 41.8% / 31.3% / 26.9% |
| Strong-headwind time | 17.1% | 14.3% |
| Crosswind-dominant time | 60.9% | **63.6%** |
| Mean absolute crosswind | 1.86 m/s | **2.64 m/s** |
| Maximum modeled gust | 9.43 m/s | **10.00 m/s** |
| Relative-air drag proxy vs calm | **1.29×** | **1.25×** |

The drag ratio is a CdA-independent comparison at the observed speeds. It is
not watts and cannot be converted into energy saved or lost without reliable
power, position and rolling-resistance inputs.

### Where the wind mattered

- **Day 1, km 0–100:** mostly favorable or crosswind. The modeled drag proxy was
  below the calm-air counterfactual.
- **Day 1, km 100–145:** the wind turned adverse: about 55% of distance was
  headwind and mean longitudinal wind was about -1.0 m/s.
- **Day 1, km 145–230:** the late slowdown coincided with the worst sustained
  adverse wind. Across the final 30 km, about **95% of distance was headwind**,
  **83% strong headwind**, with a mean component near **-3.94 m/s** and a
  2.92× relative-air drag proxy. The final pace therefore understates the
  mechanical work implied by speed alone.
- **Day 2, km 0–35:** broadly favorable, mean tail component about +1.13 m/s.
- **Day 2, km 75–165:** the main adverse block: 61% of distance headwind, mean
  component about -1.35 m/s, plus substantial crosswind.
- **Day 2, km 165–190:** the fastest late block was clearly assisted: 66% of
  distance tailwind, mean tail component about **+1.85 m/s**, and a 0.78× drag
  proxy.
- **Day 2, km 190–228:** mixed, windy and crosswind-heavy. The mean longitudinal
  component was near neutral, so the entire finish cannot be dismissed as a
  simple tailwind.

The return-day note, “Can't beat the wind on this return trip,” is compatible
with the reconstruction: Day 2 had stronger wind, stronger crosswind and
larger gusts. It was not, however, a continuous direct headwind from Manchester
to San Francisco.

HRRR is a 3 km / 15-minute atmospheric model. It cannot resolve shelter from
trees, bluff cuts, vehicles or individual gust direction at handlebar height.
Four NWS stations were used as a sanity check; station speed mean-absolute
errors were roughly 1.0–1.5 m/s and vector RMSE roughly 2.0–2.9 m/s. The phase
pattern is informative; the decimals are not instrument-grade local wind.

## Temperature and precipitation

| | Day 1 | Day 2 |
|---|---:|---:|
| Modeled temperature range | 13.0–20.7 °C | 12.5–19.9 °C |
| Mean temperature | 17.1 °C | 15.9 °C |
| Apparent-temperature range | 11.4–22.5 °C | 11.9–20.2 °C |
| Mean relative humidity | 79% | 87% |
| Route precipitation estimate | 0 mm | 0 mm |

Polar's type-9 temperature stream is wrist/device temperature, not ambient
air, so it was not substituted for the weather model.

## Internal load and durability

Using Polar's configured bands descriptively:

| HR band | Combined time | Share |
|---|---:|---:|
| Below 99 bpm | 4:01:16 | 17.4% |
| [99, 118) | 12:31:39 | 54.1% |
| [118, 138) | 5:55:30 | 25.6% |
| [138, 158) | 38:52 | 2.8% |
| [158, 177) | 0:58 | <0.1% |
| 177+ | 0:00 | 0% |

The configured max HR 197, aerobic threshold 138 and anaerobic threshold 177
are unverified, so these are watch bands rather than lab-validated physiology.
Still, the central conclusion is robust: almost all of the trip was low-HR
work and the extraordinary load came from **23 hours of duration**.

Day 2's Polar cardio load was 20.5% lower than Day 1 despite slightly longer
duration. That could reflect lower internal effort, pacing, wind/terrain mix,
fatigue-related HR suppression, or some combination. With no power or cadence,
it is not evidence of improved efficiency or full recovery.

## Fueling interpretation, updated 14 August

Self-report:

- Day 1 included roughly **2,500 kcal of almonds**, many bananas and substantial
  other food.
- Day 2 intake during the ride was worse, followed by a very large meal after
  arriving home.
- Exact quantities and timing were not logged.

Polar estimated 5,511 and 5,011 exercise kcal. Depending on whether those
estimates include resting energy and allowing for the rest of each day, a
defensible total-expenditure range is roughly **6,400–7,700 kcal on Day 1** and
**5,900–7,200 kcal on Day 2**. These are broad ranges, not measured energy
balance.

About 2,500 kcal of almonds is approximately 410–430 g: around 90 g protein,
205–215 g fat, 90 g total carbohydrate and 50–55 g fiber. That is a substantial
energy contribution, but only roughly 35–45 g is non-fiber carbohydrate. A
medium banana is about 27 g carbohydrate; the uncounted “many” cannot be turned
into a defensible hourly rate.

Therefore:

- **Total energy on Day 1 may have been adequate or close**, if the unspecified
  other food really added thousands of calories.
- **In-ride carbohydrate delivery was probably below the intended 80–90 g/h**
  unless those other foods were carbohydrate-heavy and eaten continuously.
- The huge post-Day-2 meal can materially help glycogen restoration, protein
  repair and whole-trip energy balance. It cannot improve the hours already
  ridden with less fuel.
- The ride data do **not** prove a bonk. The return finished strongly. Without
  power, glucose, RPE and a food timeline, lower Day-2 HR cannot be assigned to
  glycogen depletion.

For a future audit, log food and drink in 1–2-hour bins: grams of carbohydrate,
fluid, sodium, protein, GI symptoms and any cognitive or power-feeling dip.
Calories alone hide the most actionable variable.

## Recovery context

This trip did not begin fresh. Polar shows eight consecutive running days from
4–11 August totaling 146.593 km. The final 16.912 km run ended only **14:17
before Day 1 began**.

Day 1 ended at about 19:25. Day 2 began at 07:01, an **11:36 turnaround**. The
available post-Day-1 night contained 7:40:30 staged sleep, score 68, charge 3,
Polar overnight HR 54, HRV 68 ms and ANS charge +6.2. Quantity and autonomic markers held
up, but REM was only 59:30 and Polar's regeneration score was 61.8, both well
below the immediate pre-trip night.

The night after Day 2 later synced. The window was **23:16–03:49**: 4:20:30 of
staged sleep, 12:30 of interruptions, score 65, charge 2, continuity 4.4, deep
sleep 54:30 and REM 51:00. Nightly Recharge was 1 and ANS charge hit Polar's
floor at **−10.0**, with first-four-hour sleeping HR 70, HRV 20 ms and breathing
14.7/min. Against the prior 25-night medians, staged sleep was 3:10 shorter,
sleeping HR was 13 bpm higher and HRV was 29 ms lower. The moderate-looking
sleep score came from consolidated sleep; it does not make four hours adequate.

The planned 14 August rest day instead became a 13.677 km run in 1:22:43 at
6:03/km, HR 124 / 150, with Polar cardio load 66.6 (`HIGH`) and muscle load
1,285 (`MEDIUM`). Its easy pace/HR shows no obvious performance collapse, but
it is additional load, not evidence of completed recovery. Polar's updated
14 August model reads load 66.6, strain about 183, tolerance about 101, ratio
1.82 and status `OVERREACHING`. The ratio remains baseline-contaminated by the
missing Europe cycling block, while the new session load itself is real.

Practical implication: no more exercise on 14 August and a true zero on 15
August. A short easy run on 16 August is conditional on two mornings clearly
returning toward normal, normal symptoms and no focal bone/tendon pain; the 20
August running time trial remains conditional rather than automatic. The
detailed gates live in the Obsidian running plan.

## Data limits and provenance

- Polar AccessLink supplied the exercise summaries and 1 Hz heart rate, speed,
  barometric altitude, distance and device-temperature streams plus the GPS
  route. **No power or cadence stream exists.** No watts, normalized power,
  TSS, torque or pedaling-efficiency claim is possible.
- GPS reconstruction contained a few impossible one-second jumps over 100
  km/h; all performance-speed claims use Polar's speed stream instead. Polar
  speed maxima were 63.8 and 67.9 km/h.
- Polar calorie and substrate values are model estimates, not food intake,
  indirect calorimetry or energy balance.
- Weather source: [Open-Meteo Historical Forecast API](https://open-meteo.com/en/docs/historical-forecast-api),
  NOAA HRRR; station validation used [NWS observations](https://www.weather.gov/documentation/services-web-api).
- Polar endpoint semantics: [Polar AccessLink API](https://www.polar.com/accesslink-api/).
- Raw Polar exports, credentials and large weather grids are intentionally not
  committed. This report preserves aggregate findings and reproducible method
  choices without turning the repository into a health-data dump.

*Analysis refreshed 2026-08-14 after the post-Day-2 Polar sync.*
