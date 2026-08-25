# Europe bicycle trip distance audit

Audit date: 2026-07-17

## Result

The preferred estimate is **3,049.4 km / 1,894.8 mi** of cycling from June 24 through July 10, 2026.

This estimate uses four confirmed trip facts:

- the unrecorded June 24 Mainz-to-Karlsruhe leg remained broadly on the Rheinradweg/EV15 corridor, consistent with the trip plan, repair receipt, and photo breadcrumbs;
- Brig-to-Sion on June 29 was by train;
- June 28 was a rest day near Danis;
- the July 7 Drocourt-to-Vimy outing was by car.

With the Rheinradweg route confirmed, the track- and route-reconstruction range is approximately **3,040–3,061 km / 1,889–1,902 mi**.

The Brig-to-Sion train, June 28 rest day, and July 7 car outing are all excluded from bicycle mileage.

## Source integrity

- Original archive: `/Users/kian/Downloads/export_106370063.zip`
- Size: 273,816,825 bytes
- SHA-256: `4fba22585a0e5f4852ee049bda8c817ab00b8592843240b9dbe121e9b9a44450`
- ZIP integrity test: passed with no errors
- Trip inventory: 15 activity files on 13 Strava dates; June 24 and July 8 each contain two distinct rides
- The archive, Strava account, Photos originals, and Obsidian repository were not modified

Original FIT/GPX tracks were treated as primary evidence. Timestamped Apple Photos breadcrumbs were used independently to verify routes and reconstruct missing segments. Planned GPXs were not assumed correct; they were used only where actual photo points and other evidence aligned with them.

Photo evidence was located locally and read-only by querying `/Users/kian/Pictures/Photos Library.photoslibrary/database/Photos.sqlite` for the trip dates, then matching asset UUIDs to local Photos thumbnail/video-poster derivatives. Some evidence remained indexed in Recently Deleted. Nothing was restored, uploaded, deleted, or edited.

For each suspect interval:

`corrected distance = Strava distance - distance falsely credited + reconstructed bicycle distance`

## Daily ledger

| Date | Activity ID(s) | Strava km | Preferred corrected km | Corrected mi | Confidence | Finding |
|---|---|---:|---:|---:|---|---|
| Jun 24 | `19046169262`, `19317642280` | 65.971 | **224.37** | 139.42 | B | Add about 158.4 km from the Mainz repair shop to the final recorded ride; exclude the Kelsterbach-to-Mainz S-Bahn. The broadly followed Rheinradweg gives a day range of 222.77–226.47 km. |
| Jun 25 | `19065417135` | 151.322 | **157.57** | 97.91 | B | Strava credited essentially zero for the heat/phone-off gap; add a 6.18–6.32 km routed replacement. |
| Jun 26 | `19146675003` | 202.552 | **202.55** | 125.86 | A | Complete track. The activity was left paused overnight, affecting elapsed time but not distance. |
| Jun 27 | `19146675383` | 257.799 | **278.06** | 172.78 | B | Track ends at Carrera/Valendas, about 20.26 km before Danis. |
| Jun 28 | none | 0 | **0** | 0 | A | Confirmed rest day near Danis. |
| Jun 29 | `19119394299` | 135.595 | **135.60** | 84.26 | A | Clean Danis-to-Brig track; confirmed train from Brig to Sion is excluded. |
| Jun 30 | `19133470268` | 189.772 | **163.87** | 101.82 | A/B | Remove 24.561 km train chord into Valserhône and 1.342 km stationary GPS drift. |
| Jul 1 | none | 0 | **140.66** | 87.40 | B/C | Entire Valserhône-to-Lagnieu/Ambérieu ride missing. Fifteen endpoint/photo constraints give 135.499–146.938 km. |
| Jul 2 | `19155965787` | 172.483 | **172.48** | 107.18 | A | Complete track; only stationary pauses. |
| Jul 3 | `19167739530` | 274.983 | **274.98** | 170.87 | A | Complete track. |
| Jul 4 | `19185489004` | 284.622 | **287.47** | 178.62 | B | Logger retained a stale point before the final ride into Paris; add about 2.85 km. Plausible 287.15–287.74 km. |
| Jul 5 | none | 0 | **0** | 0 | A | Paris rest day. |
| Jul 6 | `19205929214` | 206.392 | **206.39** | 128.25 | A | Complete Paris-to-Drocourt FIT track. |
| Jul 7 | none | 0 | **0** | 0 | A | Confirmed car outing from Drocourt to Vimy Memorial. |
| Jul 8 | `19231669612`, `19233596890` | 197.170 | **197.17** | 122.52 | A | Two distinct rides: Drocourt-to-Bruges plus a valid 16.06 km Bruges city loop. |
| Jul 9 | `19248631298` | 337.807 | **337.84** | 209.92 | A/B | Replace a 604 m GPS-loss chord at Antwerp's Sint-Anna Tunnel with a 636–638 m bicycle path. |
| Jul 10 | `19263689886` | 270.394 | **270.42** | 168.03 | A/B | Add about 18–37 m for one short Hanau recording gap. |

Current Strava total across the 15 exported trip rides: **2,746.863 km / 1,706.82 mi**.

Preferred audited total: **3,049.438 km / 1,894.83 mi**.

## Material corrections

### June 24: broken crank, S-Bahn, and missing Rheinradweg leg

- Morning FIT ends at 10:13 CEST in Kelsterbach after 51.285 km.
- The Kelsterbach-to-Mainz S-Bahn is outside both activity files and is correctly excluded.
- A receipt places the repair at Radkultur Mainz, An der Goldgrube 4, at 12:18 CEST.
- Photos at Worms and Leimersheim are approximately 240 m and 15 m from the pre-trip EV15 line.
- The missing shop-to-Maximiliansau leg is about 158.4 km on the supported EV15 reconstruction.
- The final Karlsruhe FIT contributes another 14.686 km.

The shortest bicycle route constrained only through the sparse photo points is about 25 km shorter than EV15, but the rider confirmed remaining broadly on the Rheinradweg. That rules out the shorter inland branch.

### June 25: heat shutdown

- Gap: 16:14:04–16:31:35 CEST.
- Endpoints: `(48.828457, 8.036718)` to `(48.789667, 7.983886)`.
- Straight chord visible in GPX: 5.794 km.
- GPX distance excluding that chord matches Strava within 19 m, proving Strava did not credit the chord.
- Routed replacement: 6.181–6.319 km, added directly without subtracting the chord again.

### June 27: missing Danis suffix

- Last valid point: 21:03 CEST at `(46.786792, 9.292241)`, Carrera/Valendas.
- A 21:28 screenshot shows Strava paused at 257.79 km with 5% battery.
- Route to Danis village: approximately 20.26 km; plausible 20.02–20.38 km.

### June 30: false distance and Geneva train

- Stationary GPS drift: 11:53:57–12:07:40 UTC near `(46.336823, 6.891183)`. Strava credited 1,360 m although the endpoints are only 19 m apart; net removal 1,342 m.
- Last clear bicycle point: 17:24:18 UTC / 19:24 CEST at `(46.187865, 6.128663)` near Geneva.
- Next point: 06:53:09 UTC the next morning at `(46.112070, 5.829559)` in Valserhône.
- Strava credited a 24,561 m straight chord for the train movement; replacement bicycle distance is zero.

### July 1: entirely absent activity

The June 30 endpoint, thirteen photo breadcrumbs, and the July 2 start constrain a continuous Valserhône-to-Lagnieu/Ambérieu bicycle route. Three bicycle-routing alternatives through every anchor are 135.499, 140.662, and 146.938 km. The middle route is the preferred estimate.

### July 4: missing arrival into Paris

- Recorded motion stops at 21:05:22 UTC at `(48.888650, 2.409032)`.
- A geotagged video 16m44s later at `(48.873400, 2.390100)` shows the rider still helmeted/on the bicycle.
- Routed tail: 2.530–3.122 km; preferred 2.847 km.
- The activity's Wandrer text independently reports 287.53 km, within this reconstruction range, but was not treated as authoritative.

### July 9–10: minor gaps

- July 9: the recording gap crosses Antwerp's Sint-Anna pedestrian tunnel. Credited chord 604 m; endpoint-to-endpoint bicycle path 636–638 m. The official heritage inventory records the tunnel itself as 572.28 m: <https://inventaris.onroerenderfgoed.be/teksten/169024>.
- July 10: a Hanau gap was credited as 564 m; plausible bicycle paths are 582–601 m.

## Clean-track findings

- No duplicate activities were found.
- The two July 8 files are sequential, spatially continuous, and non-overlapping.
- No other sustained train-like movement was found. The maximum rolling three-minute speeds on the late trip are consistent with cycling.
- FIT cumulative distances match the raw GPS geometry to within metres when calculated with the same Earth-radius convention.
- June 26, July 2, July 3, July 6, and both July 8 activities require no material distance correction.
- Dense photo breadcrumbs independently match the July 6, 8, 9, and 10 tracks.

## Clarification status

All material route and transport ambiguities have been resolved: Rheinradweg on June 24, rest on June 28, train from Brig to Sion, and car for the July 7 Vimy outing.

No Strava activity has been cropped, edited, deleted, or replaced as part of this audit.
