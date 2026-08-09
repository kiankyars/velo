"""
Ordered waypoints for the SOUTHBOUND California coast run:
San Francisco -> Big Sur -> Limekiln -> Gaviota coast -> Los Angeles.

Coordinates are given explicitly rather than geocoded by name. Geocoders are
actively dangerous on this corridor: "Monterey, California" resolves to the
county interior 10 km from the city, "San Luis Obispo, California" lands 41 km
inland, "Harmony, California" comes back 434 km away in San Diego County, and
every Amtrak station query collapses onto Guadalupe. Every value below was
cross-checked between Photon and Nominatim, or hand-pinned where both failed
(see data/pch_geocode_audit.json for the raw comparison).

The corridor points exist to PIN THE LINE, not to describe the ride. They are
placed densely wherever the router has a real choice - leaving San Francisco,
crossing Monterey Bay, the Santa Cruz freeway section, the Los Osos/SLO inland
dog-leg, Lompoc to Las Cruces, and the run into Los Angeles - and sparsely
through Big Sur, where Highway 1 is the only road there is.

Direction of travel = order of the list. Each stage ends where the next begins.
"""

# ---------------------------------------------------------------------------
# Stage 1 - San Francisco to Limekiln State Park (night 1)
# ---------------------------------------------------------------------------
# Notes on the pinning choices:
#  - Devil's Slide: the Tom Lantos Tunnels ban bicycles, so the line is pinned
#    onto the Devil's Slide Trail (the old Highway 1 alignment). The routing
#    profile also excludes bicycle=no, so this is belt and braces.
#  - Santa Cruz -> Watsonville: CA-1 becomes a freeway. The line is pinned onto
#    Soquel Drive / San Andreas Road, which is the Adventure Cycling alignment.
#  - Monterey -> Carmel: pinned through Pacific Grove and 17-Mile Drive rather
#    than the CA-1 expressway. Bicycles are admitted to 17-Mile Drive free.
STAGE1 = [
    ("426 Fell St, San Francisco (START)", 37.77585, -122.42500),
    ("Golden Gate Park, MLK Jr Dr",        37.76900, -122.48300),
    ("Great Highway at Lincoln Way",       37.76300, -122.51000),
    # No Sloat point: the Great Highway ends there, and pinning the turn produced
    # a 366 m out-and-back. Lincoln Way plus Lake Merced pin the exit fine.
    ("Lake Merced / Skyline Blvd",         37.72050, -122.49800),
    ("Sharp Park, Pacifica",               37.63600, -122.48800),
    ("Devil's Slide Trail (N trailhead)",  37.58080, -122.51600),
    ("Half Moon Bay",                      37.46355, -122.42859),
    # San Mateo coast: CA-1 is the only road. No via-points between Half Moon Bay
    # and Santa Cruz - San Gregorio, Pescadero, Pigeon Point and Davenport all
    # snapped off the highway and cost 0.8-1.4 km of out-and-back each.
    ("Santa Cruz (downtown)",              36.97436, -122.02947),
    ("Capitola (Soquel Dr)",               36.97549, -121.95362),
    ("Aptos (Soquel Dr)",                  36.97760, -121.89750),
    ("San Andreas Rd",                     36.89300, -121.81100),
    ("Castroville",                        36.76412, -121.75176),
    ("Marina",                             36.68440, -121.80217),
    ("Monterey Bay Coastal Trail",         36.60303, -121.86500),
    # Pinned on CA-1 south of the village, NOT on Ocean Ave: Ocean Ave dead-ends
    # at the beach, so a via-point there made the line run down it and back up
    # (470 m of out-and-back).
    ("Carmel (CA-1 at Rio Rd)",             36.54300, -121.92100),
    # Carmel -> Limekiln is 78 km on which CA-1 is the ONLY road, so it gets almost
    # no via-points. Point Sur, Point Lobos, Carmel River SB, Andrew Molera, Julia
    # Pfeiffer Burns and Esalen all sit back from the highway behind gates, ranch
    # roads or car parks; as via-points they each produced a 2-4 km out-and-back
    # spur. They live in pch_pois.py as waypoints instead.
    ("Bixby Creek Bridge",                 36.37243, -121.90288),
    ("Big Sur Village (River Inn)",        36.27064, -121.80849),
    ("Limekiln State Park (NIGHT 1)",      36.00998, -121.51835),
]

# ---------------------------------------------------------------------------
# Stage 2 - Limekiln State Park to Refugio State Beach (night 2)
# ---------------------------------------------------------------------------
#  - Morro Bay -> San Luis Obispo runs inland via Los Osos and Los Osos Valley
#    Road; CA-1 north of SLO is freeway.
#  - SLO -> Pismo is pinned via Ontario Rd / Avila Beach Dr / Shell Beach Rd,
#    because US-101 through Shell Beach is freeway.
#  - Lompoc -> Las Cruces is CA-1 over the Santa Rosa Hills; from Las Cruces
#    the only road to the coast is US-101, which is why the routing profile
#    has to permit bicycle-legal freeway shoulders.
STAGE2 = [
    ("Limekiln State Park (START)",        36.00998, -121.51835),
    ("Gorda Springs",                      35.87641, -121.44614),
    # Gorda -> Cambria: CA-1 only. Kirk Creek, Plaskett Creek, Treebones, Ragged
    # Point, Piedras Blancas, the elephant-seal vista and San Simeon Acres are all
    # off-highway and were each costing a spur; they are waypoints now.
    ("Cambria",                            35.56414, -121.08111),
    ("Morro Bay",                          35.36581, -120.84990),
    # Morro Bay -> SLO runs inland via Los Osos; CA-1 north of SLO is freeway.
    ("Los Osos",                           35.31072, -120.83235),
    ("Los Osos Valley Rd",                 35.27746, -120.71900),
    ("San Luis Obispo",                    35.28280, -120.65960),
    # SLO -> Pismo pinned on Shell Beach Rd, because US-101 through Shell Beach is
    # freeway. The Avila Beach Dr point sat 700 m down a dead end: 4.0 km spur.
    ("Shell Beach",                        35.15525, -120.67239),
    # Oceano removed: it added a 407 m stitch spur and 0.4 km for nothing;
    # Shell Beach and Guadalupe already pin this stretch.
    ("Guadalupe",                          34.97164, -120.57184),
    ("Orcutt",                             34.86518, -120.44722),
    # Vandenberg Village removed: 1.6 km off CA-1, cost a 3.9 km spur.
    ("Lompoc",                             34.63915, -120.45790),
    ("Las Cruces (CA-1 / US-101)",         34.50804, -120.22904),
    ("Refugio State Beach (NIGHT 2)",      34.46243, -120.04830),
]

# ---------------------------------------------------------------------------
# Stage 3 - Refugio State Beach to Los Angeles Union Station
# ---------------------------------------------------------------------------
# Union Station is the terminus on purpose: it is where the Coast Starlight and
# the Pacific Surfliner leave from, so the finish line is also the way home.
STAGE3 = [
    ("Refugio State Beach (START)",        34.46243, -120.04830),
    # These two bracket the US-101 tagging gap west of Winchester Canyon; the leg
    # between them is the only one routed with the permissive profile.
    # On the US-101 mainline, deliberately: the earlier point at Naples snapped
    # onto a frontage road and cost a 1.5 km out-and-back at the profile-switch
    # boundary. Moving it here removed the spur AND shortened the permissive leg
    # from 7.9 km to 3.0 km.
    ("US-101 mainline W of the gap",        34.43720, -119.92500),
    ("US-101 Winchester Canyon off-ramp",  34.43790, -119.89400),
    ("Goleta",                             34.43583, -119.82764),
    # Goleta -> Santa Barbara on the OBERN TRAIL and the MODOC ROAD MULTIUSE PATH
    # rather than Hollister Ave and the other arterials. This is what the official
    # USBR 95 does here, and it is the one place on the route where the designated
    # national route is plainly safer than what the router picked on its own:
    # +4.3 km on the day buys +9.5 km of highway=cycleway, bicycle=designated and
    # takes 5.4 km off secondary arterials, for zero extra climb.
    # Coordinates lifted from OSM way geometry, not guessed, so the router lands on
    # the cycleway instead of the arterial running parallel to it.
    # Two honest caveats: parts of the Obern boardwalk are surface=wood, which is
    # slick when damp and you reach it early on a foggy morning; and a shared-use
    # path with pedestrians and dogs is slower than an arterial. The arterial line
    # is kept as pch_day3_alt_arterials if you want it back.
    # This has NOTHING to do with the 391 m bicycle=no exception, which is at km 13.7
    # in Winchester Canyon, ~9 km WEST of where this path starts. Nothing avoids that.
    ("Obern Trail (Goleta Beach end)",     34.41798, -119.83163),
    ("Obern Trail (Atascadero Creek)",     34.43377, -119.78148),
    ("Modoc Road Multiuse Path (E end)",   34.42624, -119.73582),
    ("Santa Barbara (Cabrillo Blvd)",      34.41259, -119.68874),
    ("Carpinteria",                        34.39888, -119.51846),
    ("Rincon Point",                       34.37419, -119.47664),
    # Emma Wood State Beach removed: 2.1 km off the line, cost a 4.4 km spur.
    ("Ventura (Amtrak / Harbor Blvd)",     34.27694, -119.29987),
    ("Port Hueneme",                       34.14776, -119.19516),
    ("Point Mugu Rock",                    34.09173, -119.06879),
    # Leo Carrillo (4.1 km spur) and Zuma Beach (2.4 km) removed: PCH is the only
    # road along this coast and needs no help.
    ("Malibu",                             34.03559, -118.68942),
    ("Santa Monica Pier",                  34.00890, -118.49740),
    ("Culver City (Expo path)",            34.02110, -118.39650),
    ("Exposition Park / USC",              34.01800, -118.28600),
    ("Downtown Los Angeles",               34.04500, -118.25000),
    ("LA Union Station (FINISH)",          34.05606, -118.23590),
]

# ---------------------------------------------------------------------------
# Stage 4 (OPTIONAL EXTENSION) - Los Angeles to San Diego
# ---------------------------------------------------------------------------
# Out of Union Station on the Los Angeles River path to Long Beach, then the
# Orange County beach-city coast, then the San Diego North County coast.
#
# THE CRUX IS CAMP PENDLETON. There is no public road along the coast between
# San Onofre and Oceanside - the Marine Corps base occupies 27 km of it. Two ways
# through, and they measure almost exactly the same:
#
#   * Through the base on the old highway and base bike path. Quiet and pleasant,
#     but it requires a DBIDS Recreational Bicycle pass, obtainable IN PERSON ONLY
#     at the Visitor Center by the Main Gate - which is at the OCEANSIDE end, i.e.
#     the far side from a southbound rider. Mon/Tue/Thu/Fri 07:30-15:30,
#     Wed 07:45-15:30. A southbound tourist cannot get one on the day.
#   * The I-5 shoulder, which Caltrans explicitly permits between Basilone Road
#     and Oceanside. No pass, no gate, no business hours. 27 km of freeway
#     shoulder instead of 13 km of quiet base road.
#
# Measured: base route 36.06 km, I-5 route 36.14 km. The bypass is free.
#
# The base bicycle gate at 33.3002,-117.4634 is tagged access=permit, and
# `permit` is not a value in BRouter's lookups.dat - the router literally cannot
# see that a pass is needed, so PENDLETON_GATE_NOGO keeps the line out.
#
# There WAS a through-the-base variant here. It is deleted, because the pass turns
# out to be unusable for a southbound rider on three counts:
#   1. It needs in-person biometrics (photo, fingerprint, background check) at
#      20250 Vandegrift Blvd, Oceanside - the SOUTH end, Mon-Fri 07:30-15:30. The
#      DBIDS pre-enrollment portal submits data early but does not replace the
#      in-person visit.
#   2. The DBIDS bicycle route is defined Las Pulgas gate <-> Main gate, so the
#      pass does not even cover the northern approach from San Onofre.
#   3. The publicly-rideable part north of the gate - Old Pacific Highway
#      (access=permissive, bicycle=yes) and the Pacific Coast Bikeway
#      (highway=cycleway, bicycle=yes) - DEAD-ENDS southbound. The only link from
#      that corridor onto I-5 at Las Pulgas is 80 m of access=permit road. A nogo
#      radius sweep from 20 m to 200 m over that link produced the full 27 km of
#      I-5 every single time, i.e. OSM has no alternative connection.
# So the I-5 shoulder is not a fallback, it is the only through line without base
# credentials - which is what the default stage rides.
PENDLETON_GATE_NOGO = ((33.30020, -117.46340, 200),)

STAGE4 = [
    ("LA Union Station (START)",            34.05606, -118.23590),
    ("LA River path (Vernon)",              33.98500, -118.20500),
    ("Long Beach (Shoreline)",              33.76076, -118.19019),
    ("Seal Beach",                          33.74240, -118.10559),
    ("Huntington Beach Pier",               33.65460, -118.00465),
    ("Newport Beach Pier",                  33.60307, -117.88405),
    ("Laguna Beach",                        33.54270, -117.78537),
    ("Dana Point",                          33.46336, -117.70536),
    ("San Clemente Pier",                   33.41961, -117.61974),
    # No via-points across Camp Pendleton - the nogo does the work.
    ("Oceanside Pier",                      33.19427, -117.38444),
    ("Carlsbad Village",                    33.16245, -117.35217),
    ("Encinitas",                           33.03699, -117.29198),
    ("Del Mar",                             32.95949, -117.26531),
    ("Torrey Pines State Beach",            32.93140, -117.26041),
    ("La Jolla Cove",                       32.85050, -117.27304),
    ("Mission Beach",                       32.78259, -117.25249),
    ("San Diego Santa Fe Depot (FINISH)",   32.71685, -117.16956),
]

# ---------------------------------------------------------------------------
# The one permissive leg
# ---------------------------------------------------------------------------
# Legs listed here are routed with velo_pch_road_bridge.brf instead of
# velo_pch_road.brf, because OSM's bicycle=no tagging leaves them with no legal
# path at all. Keep this list as short as it can possibly be, and keep the
# reason next to it - every entry is a deliberate departure from "the audit
# proves the line is legal".
PERMISSIVE_LEGS = {
    ("US-101 mainline W of the gap", "US-101 Winchester Canyon off-ramp"):
        "OSM starts the US-101 bicycle=no run ~1 km west of the Winchester "
        "Canyon off-ramp, leaving no legal bicycle path from the Gaviota coast "
        "into Goleta. Cyclists ride this shoulder in practice (Adventure "
        "Cycling Pacific Coast alignment). Hazard: narrow southbound bridge "
        "near the Baron Ranch trailhead.",
}

STAGES = [
    {
        "id": "pch_day1_sf_limekiln",
        "name": "Day 1 - San Francisco to Limekiln State Park",
        "desc": "Out of San Francisco on the Great Highway, the Devil's Slide Trail "
                "around the bike-banned tunnels, the San Mateo coast to Santa Cruz, "
                "around Monterey Bay, 17-Mile Drive to Carmel, then the whole of Big "
                "Sur to the Limekiln hike/bike site two miles south of Lucia.",
        "pts": STAGE1,
    },
    {
        "id": "pch_day2_limekiln_refugio",
        "name": "Day 2 - Limekiln State Park to Refugio State Beach",
        "desc": "The southern Big Sur coast (Kirk Creek, Gorda, Ragged Point), the "
                "elephant seals at Piedras Blancas, Cambria and Morro Bay, inland to "
                "San Luis Obispo, down the dunes through Guadalupe to Lompoc, over the "
                "Santa Rosa Hills to Las Cruces and out to the Gaviota coast.",
        "pts": STAGE2,
    },
    {
        "id": "pch_day3_refugio_la",
        "name": "Day 3 - Refugio State Beach to Los Angeles Union Station",
        "desc": "The Santa Barbara channel coast, the Rincon, Ventura and Oxnard, "
                "Point Mugu and the Malibu shoreline on PCH, Santa Monica, then east "
                "across Los Angeles to Union Station and the train home.",
        "pts": STAGE3,
    },
    {
        "id": "pch_day4_la_sandiego",
        "name": "Day 4 (OPTIONAL) - Los Angeles to San Diego",
        "desc": "The optional extension. Out of Union Station on the Los Angeles "
                "River path to Long Beach, the Orange County beach cities, then the "
                "San Diego North County coast to Santa Fe Depot. Camp Pendleton is "
                "bypassed on the Caltrans-permitted I-5 shoulder, so no base pass is "
                "needed; see pch_day4_alt_pendleton.gpx for the through-the-base line.",
        "pts": STAGE4,
        "optional": True,
        "nogos": PENDLETON_GATE_NOGO,
    },
]

# ---------------------------------------------------------------------------
# Variant stages
# ---------------------------------------------------------------------------
# Deliberately just one. Earlier drafts shipped eight alternative overnight
# endpoints (Lucia, Ragged Point, San Simeon, Gaviota, El Capitan, 17-Mile Drive,
# an inland Devil's Slide bypass). With the destination fixed at Los Angeles and
# the rider planning to stop where they feel like it rather than at a booked
# campground, alternative *endpoints* are noise - the line is the same road either
# way, and you can stop anywhere along it.
#
# What survives is the one variant that changes the shape of the day rather than
# just its last kilometre: the short day 1, for when the light or the legs go.
VARIANTS = [
    {
        "id": "pch_day5_sd_border",
        "name": "Day 5 (optional) - San Diego to the Mexican border",
        "desc": "The last 40 km of the Pacific Coast Bike Route: Santa Fe Depot "
                "through Coronado and the Silver Strand to Imperial Beach and "
                "Border Field State Park, where the route ends at the Mexican "
                "border. Short, flat, and the only way to say you rode the whole "
                "thing. Border Field's access road floods and closes - check "
                "before committing to the last 3 km.",
        "trim_to": "San Diego Santa Fe Depot (FINISH)",
        "extra": [
            # NO Coronado via-point. Bicycles cannot use the San Diego-Coronado
            # Bridge, and with ferries disabled the router answered a Coronado
            # waypoint by going round the bay, back up to Coronado and south again:
            # 54 km with 49 km of out-and-back. Round the bay directly is 26.0 km
            # and clean. The nicer line is the Coronado ferry from Broadway Pier
            # then the Silver Strand bike path - 24.8 km including a 2.4 km ferry
            # hop - but that adds a dependency on a boat, so it is a note, not the
            # default. Ride to the ferry terminal if you want it.
            ("Imperial Beach",               32.58389, -117.11305),
            ("Border Field SP (MEXICO)",     32.55638, -117.09673),
        ],
        "base": "STAGE4",
        "nogos": PENDLETON_GATE_NOGO,
    },
    {
        "id": "pch_day1_alt_pfeiffer",
        "name": "Day 1 variant - stop early at Big Sur Village / Pfeiffer",
        "desc": "Day 1 cut from 297 km to 256 km by stopping in Big Sur Village "
                "instead of pressing on to Limekiln. Worth having loaded: it is "
                "the decision point for whether you descend the Big Sur cliffs "
                "in the dark, and the village is the last place with food, water "
                "and a campground in one spot. Pfeiffer is also the only night on "
                "the itinerary where the air is not at saturation (dewpoint spread "
                "11-21 F against 0-2 F at Limekiln) - see check_camp_dewpoint.py. "
                "BUT THE 41.8 KM IS NOT SAVED, IT IS DEFERRED: Pfeiffer sits at km "
                "255.2 of the day-1 track, 41.8 km SHORT of Limekiln, on the same "
                "line. Pair this with pch_day2_pfeiffer_refugio (321.2 km) - do "
                "not pair it with the standard day 2, which starts at Limekiln.",
        "trim_to": "Big Sur Village (River Inn)",
        "extra": [("Pfeiffer Big Sur SP (NIGHT 1 alt)", 36.25331, -121.78330)],
    },
    {
        "id": "pch_day3_alt_arterials",
        "name": "Day 3 variant - Goleta on the arterials instead of the Obern Trail",
        "desc": "The old default, kept for the case where you want the faster line. "
                "Hollister Ave and the other Goleta arterials instead of the Obern "
                "Trail: 205.7 km against 209.9 km, so it saves 4.3 km, but it gives up "
                "9.5 km of separated bike path and puts 5.4 km back onto secondary "
                "arterials. The official USBR 95 uses the path, which is why the path "
                "is now the default. Take this one if the boardwalk is wet (parts are "
                "surface=wood) or if you are chasing a train and the shared-use path "
                "traffic would cost you more than the arterial risk.",
        "base": "STAGE3",
        "replace_upto": "Carpinteria",
        "head": [
            ("Refugio State Beach (START)",       34.46243, -120.04830),
            ("US-101 mainline W of the gap",      34.43720, -119.92500),
            ("US-101 Winchester Canyon off-ramp", 34.43790, -119.89400),
            ("Goleta",                            34.43583, -119.82764),
            ("Santa Barbara (Cabrillo Blvd)",     34.41259, -119.68874),
        ],
    },
    {
        "id": "pch_day2_pfeiffer_refugio",
        "name": "Day 2 variant - Pfeiffer Big Sur to Refugio (pairs with the alt day 1)",
        "desc": "The other half of the Pfeiffer variant, and the reason that "
                "variant is a trade rather than a saving. Stopping at Pfeiffer "
                "leaves 41.8 km of the day-1 track unridden, and it lands here: "
                "this stage is 321.2 km against the standard day 2's 279.4 km, and "
                "the deferred kilometres carry roughly 738 m of the Big Sur south "
                "coast's climbing. It also front-loads the 73 km cell dead zone "
                "(Nepenthe to Ragged Point) into the first hour of the day instead "
                "of the last hour of the previous one. Built so the Pfeiffer option "
                "can be costed honestly instead of assumed free.",
        "base": "STAGE2",
        "replace_upto": "Gorda Springs",
        "head": [
            ("Pfeiffer Big Sur SP (START)",     36.25331, -121.78330),
            # Pass-through, not a stop: this is the same CA-1 line the standard
            # day 1 covers, so it re-uses the cached legs either way.
            ("Limekiln State Park",             36.00998, -121.51835),
        ],
    },
]

BASES = {"STAGE1": STAGE1, "STAGE2": STAGE2, "STAGE3": STAGE3,
         "STAGE4": STAGE4}


def variant_points(v):
    """Resolve a variant to an ordered point list.

    Two shapes:
      trim_to/extra - share the base stage's prefix up to `trim_to`, then diverge
                      (used for the alternative overnight endpoints)
      replace_upto  - substitute the base stage's opening points with `head`, then
                      rejoin the base stage from `replace_upto` onward (used for
                      the inland bypass, which changes the START not the finish)
    """
    base = BASES[v.get("base", "STAGE1")]
    labels = [p[0] for p in base]
    if "replace_upto" in v:
        if v["replace_upto"] not in labels:
            raise KeyError(f"{v['id']}: replace_upto {v['replace_upto']!r} not in base")
        join = labels.index(v["replace_upto"])
        return v["head"] + base[join:]
    if v["trim_to"] not in labels:
        raise KeyError(f"{v['id']}: trim_to {v['trim_to']!r} not in base stage")
    cut = labels.index(v["trim_to"]) + 1
    return base[:cut] + v["extra"]
