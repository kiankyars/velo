"""
Curated points of interest for the San Francisco -> Los Angeles coast route.

These are the ones that need a human sentence attached: where you sleep, where
the road is dangerous or legally awkward, where you can quit and catch a train,
and where the water is in the stretch that has none. Objective POIs (drinking
water taps, bike shops, campgrounds, shops, toilets) are harvested from
OpenStreetMap instead - see harvest_pch_pois.py.

Every fact with a number in it is either sourced (marked SRC) or explicitly
flagged as unverified (marked VERIFY). Nothing here is invented to look tidy;
"VERIFY" means exactly that, go and check it before you rely on it.

Fields: name, lat, lon, cat, sym, desc
  cat  - camp | lodging | services | water | hazard | bailout | info
  sym  - GPX <sym>, chosen from names Garmin/OsmAnd/Locus recognise
"""

# ---------------------------------------------------------------------------
# Night 1 and its alternatives
# ---------------------------------------------------------------------------
CAMPING = [
    dict(name="Limekiln SP - NIGHT 1 (hike/bike $5)", lat=36.00998, lon=-121.51835,
         cat="camp", sym="Campground",
         desc="NIGHT 1 (if booking rather than camping wild). Reopened to camping 1 Apr 2026 after the Highway 1 "
              "slide closures. Hike/bike site $5/night; you must arrive on foot or by "
              "bike (no vehicle) and may stay a maximum of 2 consecutive nights. "
              "Fresh water, token hot showers ($1 / 5 min), toilets. Check-in 14:00, "
              "check-out 12:00. Sites 1-29 (Beach 1-12, Redwood 13-29). "
              "CRITICAL: California State Parks states 'Reservations are strongly "
              "encouraged for all campsites. There are no first-come, first-served "
              "campsites.' Do NOT plan to walk up. ReserveCalifornia 800-444-7275. "
              "SRC parks.ca.gov/?page_id=31154"),
    dict(name="Kirk Creek Campground (USFS) - fallback", lat=35.98916, lon=-121.49557,
         cat="camp", sym="Campground",
         desc="3.5 km SOUTH of Limekiln, on the ocean bluff where Nacimiento-Fergusson "
              "Road meets Highway 1. USFS Los Padres, recreation.gov. The obvious "
              "fallback if Limekiln has no bed. VERIFY hiker/biker availability and "
              "whether any sites are held back for walk-ups - USFS policy differs from "
              "State Parks. No potable water historically; carry what you need."),
    dict(name="Plaskett Creek Campground (USFS)", lat=35.91788, lon=-121.46665,
         cat="camp", sym="Campground",
         desc="12.5 km south of Limekiln, across Highway 1 from Sand Dollar Beach. "
              "USFS, recreation.gov. Second fallback south of Limekiln. VERIFY water."),
    dict(name="Pfeiffer Big Sur SP - short-day fallback", lat=36.25331, lon=-121.78330,
         cat="camp", sym="Campground",
         desc="In Big Sur Village, ~41 km SHORT of Limekiln (day 1 becomes 256 km - see "
              "pch_day1_alt_pfeiffer.gpx). "
              "The fallback if the light goes or the legs do. Full facilities, water, "
              "showers, and stores within walking distance. Also the sane place to stop "
              "rather than descend the Big Sur cliffs after dark."),
    dict(name="Andrew Molera SP (walk-in camping)", lat=36.27965, lon=-121.83095,
         cat="camp", sym="Campground",
         desc="Walk-in sites 0.5 km from the car park, north of Big Sur Village. Rougher than Pfeiffer, no showers. VERIFY it is open - Molera "
              "has had long closures."),
    dict(name="Refugio SB - NIGHT 2 (hike/bike)", lat=34.46243, lon=-120.04830,
         cat="camp", sym="Campground",
         desc="NIGHT 2 (if booking rather than camping wild). 10 Refugio Beach Road, Goleta CA 93117 - 20 miles "
              "west of Santa Barbara, off US-101 at Refugio Road. Hike-and-bike "
              "campsites confirmed; drinking water, restrooms, showers, outdoor "
              "showers, and a camp store on site. Open August 2026. "
              "Park/district phone (805) 968-1033. VERIFY the per-person hike/bike "
              "rate: the $10/person figure in the plan is NOT published on the park "
              "page - phone it. SRC parks.ca.gov/refugio"),
    dict(name="Gaviota SP - NIGHT 2 alt (16 km earlier)", lat=34.47180, lon=-120.22860,
         cat="camp", sym="Campground",
         desc="Where CA-1 meets US-101 at the coast, under the railway trestle. "
              "Hike-and-bike campsites confirmed; drinking water, restrooms/showers, "
              "camp store. Open August 2026, reservable via ReserveCalifornia. "
              "(805) 968-1033. Stops day 2 ~18 km earlier than Refugio, at the cost of a "
              "longer day 3. Known to be windy. SRC parks.ca.gov Gaviota page"),
    dict(name="El Capitan SB - NIGHT 2 alt (3 km later)", lat=34.46000, lon=-120.02400,
         cat="camp", sym="Campground",
         desc="Third of the three Gaviota-coast hike/bike parks, 2.6 km east of "
              "Refugio, and the one with the most services. Reported first-come, "
              "first-served on the middle/upper loops through 28 Jun 2026 - VERIFY "
              "current status and whether that extends to August."),
    dict(name="Morro Bay SP campground", lat=35.34277, lon=-120.82602,
         cat="camp", sym="Campground",
         desc="Day 2 escape hatch a third of the way in, if the day falls apart early. Has a "
              "hike/bike site. Water, showers."),
    dict(name="Pismo SB - North Beach campground", lat=35.13054, lon=-120.63489,
         cat="camp", sym="Campground",
         desc="Day 2 escape hatch around halfway. Hike/bike site. Water, showers."),
    dict(name="Carpinteria SB campground", lat=34.39133, lon=-119.52147,
         cat="camp", sym="Campground",
         desc="Day 3 escape hatch, on the beach in town. Hike/bike site, water, "
              "showers, and food a block away."),
]

# ---------------------------------------------------------------------------
# The indoor options from the plan, north to south
# ---------------------------------------------------------------------------
LODGING = [
    dict(name="Lucia Lodge (10 rooms/cabins)", lat=36.02061, lon=-121.54926,
         cat="lodging", sym="Lodging",
         desc="3.6 km NORTH of Limekiln on the cliff - the indoor option closest to the "
              "ideal stopping point. Ten rooms/cabins only, so it books out. Restaurant "
              "on site."),
    dict(name="Treebones Resort (yurts)", lat=35.88427, lon=-121.45533,
         cat="lodging", sym="Lodging",
         desc="South of Limekiln on day 2. Yurts with real beds. The plan notes a "
              "two-night minimum, which usually rules it out for a through-ride - "
              "VERIFY, they sometimes release single nights late."),
    dict(name="Gorda Springs Resort (cabins) + store + fuel", lat=35.87641, lon=-121.44614,
         cat="lodging", sym="Lodging",
         desc="Cabins, and one of only a handful of shops "
              "on this coast. Not bookable online in practice - the plan says call "
              "805-924-1825. VERIFY the number before relying on it."),
    dict(name="Ragged Point Inn (39 rooms) + market + fuel", lat=35.78072, lon=-121.33083,
         cat="lodging", sym="Lodging",
         desc="39 conventional rooms, restaurant, market and fuel at the south end of "
              "the Big Sur cliffs - the most reliable indoor bed on the coast, but as a "
              "day-1 finish it makes for a ~333 km day. Last real services before "
              "San Simeon."),
    dict(name="San Simeon Acres (motel strip)", lat=35.59235, lon=-121.12446,
         cat="lodging", sym="Lodging",
         desc="Ordinary motels in numbers, 10 km south of the Hearst Castle entrance. "
              "The reliable indoor fallback if everything north of here has failed, "
              "but it turns day 1 into a ~365 km ride."),
]

# ---------------------------------------------------------------------------
# Hazards, legal oddities and traffic control
# ---------------------------------------------------------------------------
HAZARDS = [
    dict(name="HAZARD Devil's Slide - tunnels ban bikes, use the trail",
         lat=37.58080, lon=-122.51600, cat="hazard", sym="Danger Area",
         desc="Bicycles are not permitted in the Tom Lantos Tunnels. The route is "
              "pinned onto the Devil's Slide Trail, the old Highway 1 alignment "
              "(2.9 km of paved bicycle=designated cycleway). "
              "TIMING PROBLEM: San Mateo County publishes that the PARKING LOTS open "
              "at 08:00; it does NOT publish separate trail-access hours, and the "
              "county page says to contact them for trail access. On a 05:00 start you "
              "reach here about 06:30-07:00. If the trail is gated you have no legal "
              "way past - the tunnels are not an option. CALL SAN MATEO COUNTY PARKS "
              "BEFORE YOU LEAVE, or ride the inland bypass variant "
              "(pch_day1_alt_inland_bypass.gpx). SRC smcgov.org/parks/devils-slide-trail-hours"),
    dict(name="HAZARD Rocky Creek Bridge - one-way signal control",
         lat=36.38480, lon=-121.90270, cat="hazard", sym="Danger Area",
         desc="Caltrans one-way, signal-controlled traffic control at Rocky Creek "
              "Bridge, running 24/7 through 31 August 2026, with delays up to 15 "
              "minutes. You will be held here. Expect to share a single lane with "
              "released traffic - take the lane, do not let a queue pass you inside the "
              "control. Check QuickMap the morning you ride. SRC Caltrans D5 / Big Sur "
              "Chamber Highway 1 conditions, Aug 2026"),
    dict(name="INFO Regent's Slide - reopened, monitored",
         lat=35.92000, lon=-121.46500, cat="info", sym="Flag, Blue",
         desc="The slide that closed Big Sur for two years. Highway 1 reopened here on "
              "14 January 2026, about 90 days early, after an $82 million repair. "
              "Caltrans calls the slope stable and monitors it continuously "
              "(prisms, accelerometer arrays, inclinometers, drone survey, "
              "piezometers). This is why the ride is possible at all in 2026 - and why "
              "you check QuickMap before departing anyway. Position approximate. "
              "SRC gov.ca.gov 14 Jan 2026 / Caltrans D5"),
    dict(name="HAZARD US-101 Goleta - 391 m OSM says bikes banned",
         lat=34.43320, lon=-119.91280, cat="hazard", sym="Danger Area",
         desc="THE ONE DELIBERATE EXCEPTION IN THIS GPX. OSM begins the US-101 "
              "bicycle=no run about 1 km west of the Winchester Canyon off-ramp, which "
              "leaves no legal bicycle path at all from the Gaviota coast into Goleta. "
              "Obeying it literally routes you over the Santa Ynez Mountains: 85 km "
              "instead of 8, +1,491 m, 5.3 km of dirt. So this leg is routed with a "
              "permissive profile and uses 391 m of freeway that OSM tags bicycle=no. "
              "Cyclists ride this shoulder in practice - it is the Adventure Cycling "
              "Pacific Coast line. Leave 101 at the Winchester Canyon off-ramp and take "
              "Calle Real / Hollister Ave into Goleta. If signage says otherwise on the "
              "day, obey the signage."),
    dict(name="HAZARD narrow southbound 101 bridge (Baron Ranch)",
         lat=34.47000, lon=-120.13000, cat="hazard", sym="Danger Area",
         desc="The Gaviota-coast 101 shoulder is wide, but riders single out the narrow "
              "SOUTHBOUND bridge near the Baron Ranch trailhead. Short, signed, good "
              "sight lines - but the shoulder pinches. Position approximate. "
              "SRC rbw-owners-bunch cyclist thread, Lompoc-Santa Barbara"),
    dict(name="INFO Gaviota Tunnel - bicycles ARE allowed",
         lat=34.51500, lon=-120.22800, cat="info", sym="Flag, Blue",
         desc="US-101 through Gaviota Pass. Bicycles are allowed through the Gaviota "
              "Tunnel - it is the only route between the South Coast and the Santa Ynez "
              "Valley. Southbound you are descending; take the lane through the bore "
              "and run lights. Position approximate."),
    dict(name="INFO US-101 closed to bikes, Santa Barbara -> Ventura",
         lat=34.40000, lon=-119.50000, cat="info", sym="Flag, Blue",
         desc="US-101 between Santa Barbara and Ventura is closed to bicycles, which is "
              "why day 3 runs on city streets, county roads and the ocean-side bike "
              "paths through Carpinteria and the Rincon instead. The route obeys this: "
              "the audit shows zero bike-banned metres on this stretch."),
    dict(name="INFO Santa Monica Pier - 190 m of timber decking",
         lat=34.00910, lon=-118.49710, cat="info", sym="Flag, Blue",
         desc="The only 'unpaved' metres on day 3 are the pier's wooden boards. "
              "Harmless, but it is where the audit's 0.22 km of non-asphalt comes from. "
              "Slippery when wet."),
    dict(name="HAZARD PCH Malibu->Santa Monica - active fire-rebuild corridor",
         lat=34.03700, lon=-118.60000, cat="hazard", sym="Danger Area",
         desc="The last ~25 km of day 3 runs through the Palisades Fire "
              "reconstruction corridor. Caltrans D7 has a rock-slope-protection and "
              "pavement rebuild near Ratner Beach due to finish FALL 2026, and a "
              "second project covering about five miles from just south of the "
              "California Incline to Topanga Creek due END OF 2026 - both still live "
              "in August 2026. After the fire, PCH reopened with ONE LANE each way at "
              "25 mph. Expect no shoulder, construction traffic and coned lanes "
              "exactly where you are most tired. The route leaves PCH at Santa Monica "
              "Pier and goes inland via Culver City, so the exposure is Malibu to "
              "Santa Monica only. If it looks bad, quit at Oxnard or Ventura Amtrak "
              "and take the Surfliner in. Position approximate - the corridor is long. "
              "SRC Caltrans D7 PCH Palisades Fire Repairs project pages"),
    dict(name="HAZARD Vandenberg - CA-1 can close at short notice",
         lat=34.71165, lon=-120.46068, cat="hazard", sym="Danger Area",
         desc="Day 2 passes Vandenberg SFB on CA-1. Launch operations close roads "
              "around the base at a few hours' notice - a documented example closed "
              "CA-246 between CA-1 and Mission Gate Road from 10:00 to 15:00 on 2 Mar "
              "2026 for a launch that then scrubbed. That closure was on CA-246, NOT "
              "on this route's CA-1 line, but CA-1 itself has been closed here for "
              "base incidents and carries ongoing Caltrans roadwork (Vandenberg "
              "Village, Santa Lucia Canyon Rd). Check QuickMap and the Vandenberg "
              "launch schedule for your date; there is no good detour - the inland "
              "alternative is US-101 via Santa Maria and Los Alamos."),
    dict(name="INFO Wild camping - where it is actually legal here",
         lat=36.02079, lon=-121.55050, cat="info", sym="Flag, Blue",
         desc="If you are stopping where you like rather than booking: dispersed "
              "camping on LOS PADRES NATIONAL FOREST land is allowed and needs no "
              "permit. The catch is geography - the strip immediately along Highway 1 "
              "through Big Sur is mostly state park or private ranch, where it is "
              "prohibited; the National Forest land (Ventana and Silver Peak "
              "Wilderness) is largely EAST of the highway and uphill, so it means "
              "getting off CA-1 and climbing. CAMPFIRES ARE BANNED until 31 Jan 2027 "
              "under a Forest Order effective 4 Jun 2026, across Los Padres including "
              "Ventana and Silver Peak; a stove is fine with a free California "
              "Campfire Permit. August is peak fire season and restrictions tighten at "
              "short notice - check before you go. Position is nominal, it applies to "
              "the whole Big Sur stretch. "
              "SRC fs.usda.gov/r05/lospadres fire-use restrictions"),
    dict(name="HAZARD Big Sur - no cell signal, no bike shop, no exit",
         lat=36.15000, lon=-121.65000, cat="hazard", sym="Danger Area",
         desc="From Carmel to Cambria there is no bike shop, no hospital, no transit and "
              "long stretches with no cell signal. A destroyed rear wheel here is a "
              "hitch-hike, not a phone call. Carry: 2 tubes, patches, a boot, a spare "
              "quick-link, a derailleur hanger, and enough water for 60 km."),
]

# ---------------------------------------------------------------------------
# Where you can quit
# ---------------------------------------------------------------------------
BAILOUTS = [
    dict(name="BAILOUT Salinas Amtrak (Coast Starlight)", lat=36.67860, lon=-121.65728,
         cat="bailout", sym="Car",
         desc="11 Station Place, Salinas. Coast Starlight. ~25 km inland from the route "
              "at Marina/Castroville - the LAST bail-out before Big Sur, and the only "
              "one for the next 250 km. Coast Starlight carries bicycles but roll-on "
              "space is limited and needs a separate bike reservation. VERIFY the 2026 "
              "bike fee and space with Amtrak before counting on it."),
    dict(name="BAILOUT San Luis Obispo Amtrak", lat=35.27632, lon=-120.65468,
         cat="bailout", sym="Car",
         desc="1011 Railroad Avenue. Coast Starlight AND Pacific Surfliner - the best "
              "bail-out on the whole route, and it sits directly on day 2 at km ~148. "
              "Surfliner has roll-on bicycle racks. VERIFY 2026 bike reservation rules."),
    dict(name="BAILOUT Santa Barbara Amtrak", lat=34.41365, lon=-119.69280,
         cat="bailout", sym="Car",
         desc="209 State Street, right on the day-3 line at km ~95. Surfliner roll-on "
              "bikes; Coast Starlight also stops."),
    dict(name="BAILOUT Ventura Amtrak", lat=34.27694, lon=-119.29987,
         cat="bailout", sym="Car",
         desc="Harbor Boulevard, on the day-3 line. Surfliner."),
    dict(name="BAILOUT Oxnard Transportation Center", lat=34.20074, lon=-119.18072,
         cat="bailout", sym="Car",
         desc="Surfliner plus Metrolink. The last easy escape before the Malibu coast."),
    dict(name="FINISH LA Union Station", lat=34.05606, lon=-118.23590,
         cat="bailout", sym="Car",
         desc="800 North Alameda Street. The finish, chosen because it is also the way "
              "home: Coast Starlight north to Oakland/Emeryville, or Surfliner + "
              "Thruway. Coast Starlight roll-on bike space is limited and sells out - "
              "book the bike the moment you know your date."),
]

# ---------------------------------------------------------------------------
# Water and food in the stretch that has almost none
# ---------------------------------------------------------------------------
SERVICES = [
    dict(name="SERVICES Big Sur Village (last real resupply)", lat=36.27064, lon=-121.80849,
         cat="services", sym="Convenience Store",
         desc="The River Inn / Ripplewood / Fernwood cluster, with a general store and "
              "delis over about 1 km of Highway 1. THE last dense resupply before a very "
              "thin 90 km. Fill everything here. Hours are seasonal and early-closing - "
              "VERIFY on the day."),
    dict(name="SERVICES Big Sur Station (ranger station, water)", lat=36.24798, lon=-121.78129,
         cat="water", sym="Drinking Water",
         desc="USFS/State Parks multi-agency station just south of Pfeiffer Big Sur. "
              "Water and toilets, and the people who actually know today's road status."),
    dict(name="SERVICES Nepenthe / Cafe Kevah", lat=36.22181, lon=-121.75966,
         cat="services", sym="Restaurant",
         desc="Cliff-top restaurant 4 km south of Big Sur Station. Expensive, but it is "
              "food and water on a stretch that offers neither."),
    dict(name="SERVICES Lucia Lodge restaurant", lat=36.02061, lon=-121.54926,
         cat="services", sym="Restaurant",
         desc="3.6 km before Limekiln - the practical place to eat before camping, "
              "because Limekiln has no store. Seasonal hours; VERIFY."),
    dict(name="SERVICES Gorda Springs - store + fuel", lat=35.87641, lon=-121.44614,
         cat="services", sym="Convenience Store",
         desc="20 km south of Limekiln. Small store and fuel; famously expensive. On "
              "day 2 this is your first resupply chance after camp."),
    dict(name="SERVICES Ragged Point - market + restaurant + fuel", lat=35.78072, lon=-121.33083,
         cat="services", sym="Convenience Store",
         desc="39 km into day 2. The first substantial services since Big Sur Village "
              "and the last before San Simeon."),
    dict(name="WATER Gaviota rest area - best water on the Gaviota coast",
         lat=34.49000, lon=-120.22000, cat="water", sym="Drinking Water",
         desc="Riders single this out: 'there are very few opportunities for water or "
              "food between Lompoc and Santa Barbara. The rest stop at Gaviota is the "
              "best place to water up.' Position approximate - it is on US-101 near the "
              "CA-1 junction. SRC rbw-owners-bunch cyclist thread"),
    dict(name="INFO Aniso Trail - paved path El Capitan <-> Refugio",
         lat=34.46100, lon=-120.03600, cat="info", sym="Bike Trail",
         desc="A 2.5 mile undulating paved bike path along the bluff between El Capitan "
              "and Refugio - the pleasant way to start day 3 instead of the 101 "
              "shoulder. A segment has been closed for storm damage; VERIFY on site, "
              "and drop back onto 101 if it is shut."),
]

# ---------------------------------------------------------------------------
# The optional San Diego extension (day 4)
# ---------------------------------------------------------------------------
EXTENSION = [
    dict(name="CRUX Camp Pendleton - the only real problem on day 4",
         lat=33.30020, lon=-117.46340, cat="hazard", sym="Danger Area",
         desc="27 km of coast between San Onofre and Oceanside is Marine Corps base "
              "with no public road. Two ways through, and they MEASURE THE SAME "
              "(36.1 km either way): "
              "(1) THROUGH THE BASE on the old highway and base bike path - quiet and "
              "pleasant, but needs a DBIDS Recreational Bicycle pass, obtainable IN "
              "PERSON ONLY at the Visitor Center by the Main Gate (Bldg 20255T), which "
              "is at the OCEANSIDE end - the far side from a southbound rider. "
              "Mon/Tue/Thu/Fri 07:30-15:30, Wed 07:45-15:30, valid one year. You "
              "cannot get one en route. The path also closes for military exercises. "
              "(2) THE I-5 SHOULDER, which Caltrans permits between Basilone Road and "
              "Oceanside (exits 62-54) - no pass, no gate, no business hours, but "
              "27 km of freeway shoulder instead of 13 km of quiet road. "
              "THE PASS IS NOT USABLE SOUTHBOUND, on three counts: it needs in-person "
              "biometrics (photo, fingerprint, background check) at the south end; the "
              "DBIDS bicycle route is defined Las Pulgas gate <-> Main gate so it does "
              "not cover the northern approach at all; and the publicly-rideable part "
              "north of the gate (Old Pacific Highway, access=permissive, and the "
              "Pacific Coast Bikeway, bicycle=yes) DEAD-ENDS southbound - the only link "
              "onto I-5 at Las Pulgas is 80 m of access=permit road. So option 2 is not "
              "a fallback, it is the only through line, and it is what the GPX rides. "
              "This waypoint is that 80 m gate."),
    dict(name="INFO Aliso Creek rest area - water on the I-5 stretch",
         lat=33.31500, lon=-117.48200, cat="water", sym="Drinking Water",
         desc="On the I-5 bypass stretch through Camp Pendleton: water, restrooms and "
              "vending machines. The only stop in 27 km of freeway shoulder. Position "
              "approximate."),
    dict(name="Torrey Pines - the only climb on day 4",
         lat=32.89495, lon=-117.24139, cat="info", sym="Summit",
         desc="4.84 km at 2.6% to 132 m, the single climb over 60 m on the whole "
              "218 km day (which totals just +685 m). Detected from the route's own "
              "elevation profile. Torrey Pines Rd out of Del Mar; the coast road "
              "through the reserve is the scenic line."),
    dict(name="San Elijo SB - the ONLY hike/bike site left on the extension",
         lat=33.02000, lon=-117.28300, cat="camp", sym="Campground",
         desc="One single hike/bike site (#94), FIRST COME FIRST SERVED after 16:00, "
              "vacate by 09:00, ONE NIGHT ONLY, $10 per person. "
              "IMPORTANT: hiker/biker sites at San Onofre, San Clemente and South "
              "Carlsbad State Beaches have reportedly been ELIMINATED, so this is the "
              "only cheap legal bed on the LA-San Diego coast. VERIFY with San Diego "
              "Coast District before relying on it - the elimination report is a "
              "cyclist forum, not a parks.ca.gov page. Practical upshot: ride "
              "LA-San Diego in ONE day (218 km, +685 m, easily inside your range) "
              "rather than planning to camp partway. Position approximate."),
    dict(name="BAILOUT/FINISH San Diego Santa Fe Depot", lat=32.71685, lon=-117.16956,
         cat="bailout", sym="Car",
         desc="1050 Kettner Blvd, downtown. Pacific Surfliner: FREE bike reservations, "
              "7 bike spaces per train, roll-on. Getting home = Surfliner to LA, then "
              "Coast Starlight north (6 bikes in the baggage car, books out). Note "
              "this is one MORE transfer than finishing at LA Union Station, not "
              "fewer - but San Diego airport is 5 km from here, which LAX is not. "
              "Surfliner also runs SD all the way to San Luis Obispo."),
    dict(name="INFO Coronado - bridge banned to bikes, take the ferry",
         lat=32.69152, lon=-117.17669, cat="info", sym="Flag, Blue",
         desc="If you ride the border extension: bicycles cannot use the San "
              "Diego-Coronado Bridge. Options are the ferry from Broadway Pier "
              "(bikes carried, small fare) and then the Silver Strand bike path - "
              "24.8 km to the border and much the nicer ride - or round the bay "
              "through National City and Chula Vista, 26.0 km, no boat needed. The "
              "GPX takes the round-the-bay line because it has no dependency; ride "
              "to the ferry terminal instead if you prefer the Strand."),
    dict(name="Border Field SP - the end of the Pacific Coast Bike Route",
         lat=32.55638, lon=-117.09673, cat="info", sym="Flag, Blue",
         desc="Where the route meets the Mexican border at the ocean. 26 km past "
              "Santa Fe Depot. The access road floods and closes regularly - check "
              "before committing to the last 3 km, and be ready to turn round at "
              "Imperial Beach."),
    dict(name="INFO LA River path - how you get out of Union Station",
         lat=33.98500, lon=-118.20500, cat="info", sym="Bike Trail",
         desc="Day 4 leaves downtown on the Los Angeles River path south to Long "
              "Beach, which is why the first 38 km are almost all Class I. Day 4 is "
              "25% bike path overall (54.6 km of 218 km) - by far the most protected "
              "day of the whole trip."),
]

POIS = CAMPING + LODGING + HAZARDS + BAILOUTS + SERVICES + EXTENSION
