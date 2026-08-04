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
    ("Great Highway at Sloat Blvd",        37.73500, -122.50600),
    ("Lake Merced / Skyline Blvd",         37.72050, -122.49800),
    ("Sharp Park, Pacifica",               37.63600, -122.48800),
    ("Pacifica (Rockaway Beach)",          37.59800, -122.49950),
    ("Devil's Slide Trail (N trailhead)",  37.58080, -122.51600),
    ("Montara",                            37.54942, -122.49354),
    ("Half Moon Bay",                      37.46355, -122.42859),
    ("San Gregorio State Beach",           37.32450, -122.40300),
    # No via-point between here and Pigeon Point: CA-1 is the only road, and a
    # point placed at the Pescadero Creek Rd junction snapped onto a dirt
    # service track (+0.7 km, 322 m unpaved).
    ("Pigeon Point Lighthouse",            37.18212, -122.39408),
    ("Davenport",                          37.01542, -122.19071),
    ("Santa Cruz (downtown)",              36.97436, -122.02947),
    ("Capitola (Soquel Dr)",               36.97549, -121.95362),
    ("Aptos (Soquel Dr)",                  36.97760, -121.89750),
    ("San Andreas Rd",                     36.89300, -121.81100),
    # Sunset State Beach removed: it is a spur off San Andreas Rd and cost
    # 5.4 km out-and-back for nothing.
    ("Moss Landing",                       36.80359, -121.78627),
    ("Castroville",                        36.76412, -121.75176),
    ("Marina",                             36.68440, -121.80217),
    ("Monterey Bay Coastal Trail",         36.60303, -121.86500),
    # Monterey -> Carmel goes direct (9.9 km). Round the Monterey peninsula on
    # 17-Mile Drive instead and it is 23.5 km: see the 17-Mile Drive variant.
    ("Carmel-by-the-Sea (Ocean Ave)",      36.55508, -121.92614),
    ("Carmel River State Beach",           36.53458, -121.92796),
    ("Point Lobos State Reserve",          36.51473, -121.94279),
    # No via-point at Garrapata: the geocoded park centroid sits 1.2 km inland
    # at 540 m and dragged the line 6.8 km up Garrapata Canyon (+585 m climb).
    ("Rocky Creek Bridge",                 36.38480, -121.90270),
    ("Bixby Creek Bridge",                 36.37243, -121.90288),
    ("Point Sur Lighthouse",               36.30637, -121.90172),
    ("Andrew Molera State Park",           36.27965, -121.83095),
    ("Big Sur Village (River Inn)",        36.27064, -121.80849),
    ("Pfeiffer Big Sur State Park",        36.25331, -121.78330),
    ("Big Sur Station",                    36.24798, -121.78129),
    ("Nepenthe",                           36.22181, -121.75966),
    ("Julia Pfeiffer Burns SP (McWay)",    36.16997, -121.66539),
    ("Esalen Institute",                   36.12481, -121.63774),
    ("Lucia",                              36.02079, -121.55050),
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
    ("Kirk Creek Campground",              35.98916, -121.49557),
    ("Plaskett Creek / Sand Dollar",       35.91788, -121.46665),
    ("Treebones Resort",                   35.88427, -121.45533),
    ("Gorda Springs",                      35.87641, -121.44614),
    ("Ragged Point Inn",                   35.78072, -121.33083),
    # No via-points at Piedras Blancas, the elephant seal vista or San Simeon
    # Acres: CA-1 is the only road from Ragged Point to Cambria, and every one of
    # those three snapped off the highway onto a bluff trail or a parking lot
    # (1,964 m + 349 m + 2,590 m of dirt between them). They survive as POIs in
    # pch_pois.py, snapped to the highway line.
    ("Hearst Castle entrance",             35.64540, -121.18414),
    ("Cambria",                            35.56414, -121.08111),
    ("Harmony",                            35.50858, -121.02269),
    ("Cayucos",                            35.43701, -120.88311),
    ("Morro Bay",                          35.36581, -120.84990),
    ("Morro Bay State Park",               35.34277, -120.82602),
    ("Los Osos",                           35.31072, -120.83235),
    ("Los Osos Valley Rd",                 35.27746, -120.71900),
    ("San Luis Obispo",                    35.28280, -120.65960),
    ("Avila Beach Dr",                     35.17998, -120.73184),
    ("Shell Beach",                        35.15525, -120.67239),
    ("Pismo Beach",                        35.14274, -120.64129),
    ("Oceano",                             35.10531, -120.61689),
    ("Guadalupe",                          34.97164, -120.57184),
    ("Orcutt",                             34.86518, -120.44722),
    ("Vandenberg Village",                 34.71165, -120.46068),
    ("Lompoc",                             34.63915, -120.45790),
    ("Las Cruces (CA-1 / US-101)",         34.50804, -120.22904),
    ("Gaviota State Park",                 34.47718, -120.22857),
    ("Refugio State Beach (NIGHT 2)",      34.46243, -120.04830),
]

# ---------------------------------------------------------------------------
# Stage 3 - Refugio State Beach to Los Angeles Union Station
# ---------------------------------------------------------------------------
# Union Station is the terminus on purpose: it is where the Coast Starlight and
# the Pacific Surfliner leave from, so the finish line is also the way home.
STAGE3 = [
    ("Refugio State Beach (START)",        34.46243, -120.04830),
    ("El Capitan State Beach",             34.46000, -120.02400),
    # The two points below bracket the US-101 tagging gap west of Winchester
    # Canyon. The leg between them is the only leg of the whole trip routed with
    # the permissive profile (see PERMISSIVE_LEGS below and
    # velo_pch_road_bridge.brf). Without them the router answers this 5 km
    # coastal hop by crossing the Santa Ynez Mountains: 85 km and +1,491 m.
    ("US-101 at Naples (Gaviota coast)",   34.44500, -119.95000),
    ("US-101 Winchester Canyon off-ramp",  34.43840, -119.90500),
    ("Goleta",                             34.43583, -119.82764),
    ("Goleta Beach County Park",           34.41656, -119.83280),
    ("Santa Barbara (Cabrillo Blvd)",      34.41259, -119.68874),
    ("Carpinteria State Beach",            34.39133, -119.52147),
    ("Rincon Point",                       34.37419, -119.47664),
    ("La Conchita",                        34.36418, -119.44786),
    ("Emma Wood State Beach",              34.28422, -119.32237),
    ("Ventura (Amtrak / Harbor Blvd)",     34.27694, -119.29987),
    ("Port Hueneme",                       34.14776, -119.19516),
    ("Point Mugu Rock",                    34.09173, -119.06879),
    ("Leo Carrillo State Park",            34.06098, -118.93281),
    ("Zuma Beach",                         34.02144, -118.83103),
    ("Malibu",                             34.03559, -118.68942),
    ("Will Rogers State Beach",            34.03331, -118.53195),
    ("Santa Monica Pier",                  34.00890, -118.49740),
    ("Culver City (Expo path)",            34.02110, -118.39650),
    ("Exposition Park / USC",              34.01800, -118.28600),
    ("Downtown Los Angeles",               34.04500, -118.25000),
    ("LA Union Station (FINISH)",          34.05606, -118.23590),
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
    ("US-101 at Naples (Gaviota coast)", "US-101 Winchester Canyon off-ramp"):
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
]

# ---------------------------------------------------------------------------
# Variant stages - the alternatives the plan actually leaves open
# ---------------------------------------------------------------------------
# Day 1 can finish at four different places depending on what is bookable and
# how the legs feel. Each is a full stage file so it can be loaded on its own.
# `trim_to` = the label in STAGE1 to cut the shared prefix at; `extra` = the
# points appended after it.
VARIANTS = [
    {
        "id": "pch_day1_alt_inland_bypass",
        "name": "Day 1 variant - inland bypass, no Devil's Slide Trail",
        "desc": "Insurance against a locked gate. San Mateo County publishes an 08:00 "
                "opening for the Devil's Slide Trail PARKING LOTS and does not publish "
                "trail-access hours; a 05:00 departure reaches the trail around "
                "06:30-07:00, and the Tom Lantos Tunnels are not a legal alternative. "
                "This variant leaves the coast at Lake Merced and takes Skyline "
                "Boulevard (CA-35) down the peninsula ridge to CA-92, then drops west "
                "into Half Moon Bay, rejoining the main line there. More climbing and "
                "no ocean for the first 60 km, but it cannot be gated shut.",
        "replace_upto": "Half Moon Bay",
        "head": [
            ("426 Fell St, San Francisco (START)", 37.77585, -122.42500),
            ("Golden Gate Park, MLK Jr Dr",        37.76900, -122.48300),
            ("Lake Merced / Skyline Blvd",         37.72050, -122.49800),
            ("Skyline Blvd (CA-35), San Bruno",    37.63000, -122.44000),
            ("Skyline Blvd, Crystal Springs",      37.54000, -122.37000),
            ("CA-35 / CA-92 junction",             37.51300, -122.34800),
            ("CA-92 westbound summit",             37.49000, -122.39000),
        ],
    },
    {
        "id": "pch_day1_alt_17mile",
        "name": "Day 1 variant - round the Monterey peninsula on 17-Mile Drive",
        "desc": "Instead of cutting straight from Monterey to Carmel (9.9 km, with "
                "0.5 km of bicycle-legal CA-1 freeway shoulder), swing around the "
                "peninsula tip through Pacific Grove, Asilomar and 17-Mile Drive "
                "(23.5 km). Bicycles are admitted to 17-Mile Drive free of charge. "
                "Costs 13.6 km and ~170 m of climbing, and keeps you off the "
                "expressway entirely. Worth it only if day 1 is going well.",
        "trim_to": "Monterey Bay Coastal Trail",
        "extra": [
            ("Pacific Grove",                   36.62111, -121.91779),
            ("Asilomar State Beach",            36.62409, -121.94009),
            ("17-Mile Drive (Cypress Point)",   36.57900, -121.96600),
            ("Carmel-by-the-Sea (Ocean Ave)",   36.55508, -121.92614),
            ("Carmel River State Beach",        36.53458, -121.92796),
            ("Point Lobos State Reserve",       36.51473, -121.94279),
            ("Rocky Creek Bridge",              36.38480, -121.90270),
            ("Bixby Creek Bridge",              36.37243, -121.90288),
            ("Point Sur Lighthouse",            36.30637, -121.90172),
            ("Andrew Molera State Park",        36.27965, -121.83095),
            ("Big Sur Village (River Inn)",     36.27064, -121.80849),
            ("Pfeiffer Big Sur State Park",     36.25331, -121.78330),
            ("Big Sur Station",                 36.24798, -121.78129),
            ("Nepenthe",                        36.22181, -121.75966),
            ("Julia Pfeiffer Burns SP (McWay)", 36.16997, -121.66539),
            ("Esalen Institute",                36.12481, -121.63774),
            ("Lucia",                           36.02079, -121.55050),
            ("Limekiln State Park (NIGHT 1)",   36.00998, -121.51835),
        ],
    },
    {
        "id": "pch_day1_alt_pfeiffer",
        "name": "Day 1 variant - finish early at Pfeiffer Big Sur (fallback)",
        "desc": "The short fallback if Limekiln cannot be confirmed or the light "
                "runs out: stop at Pfeiffer Big Sur State Park in Big Sur Village, "
                "~55 km short of Limekiln. Leaves a longer day 2.",
        "trim_to": "Big Sur Station",
        "extra": [("Pfeiffer Big Sur SP (NIGHT 1 alt)", 36.25331, -121.78330)],
    },
    {
        "id": "pch_day1_alt_lucia",
        "name": "Day 1 variant - finish at Lucia Lodge (indoor)",
        "desc": "The indoor option nearest the ideal stopping point: Lucia Lodge, "
                "10 rooms/cabins on the cliff, ~3 km north of Limekiln.",
        "trim_to": "Esalen Institute",
        "extra": [("Lucia Lodge (NIGHT 1 alt)", 36.02061, -121.54926)],
    },
    {
        "id": "pch_day1_alt_raggedpoint",
        "name": "Day 1 variant - finish at Ragged Point Inn (indoor)",
        "desc": "The longer indoor option: 39 conventional rooms plus market and "
                "fuel at the south end of the Big Sur cliffs. Pushes day 1 out by "
                "~72 km beyond Limekiln and shortens day 2 to match.",
        "trim_to": "Limekiln State Park (NIGHT 1)",
        "extra": [
            ("Kirk Creek Campground",            35.98916, -121.49557),
            ("Plaskett Creek / Sand Dollar",     35.91788, -121.46665),
            ("Gorda Springs",                    35.87641, -121.44614),
            ("Ragged Point Inn (NIGHT 1 alt)",   35.78072, -121.33083),
        ],
    },
    {
        "id": "pch_day1_alt_sansimeon",
        "name": "Day 1 variant - finish at San Simeon (indoor fallback)",
        "desc": "The reliable-motels fallback, ~32 km south of Ragged Point. Only "
                "worth it if Limekiln, Lucia and Ragged Point are all unavailable.",
        "trim_to": "Limekiln State Park (NIGHT 1)",
        "extra": [
            ("Kirk Creek Campground",            35.98916, -121.49557),
            ("Plaskett Creek / Sand Dollar",     35.91788, -121.46665),
            ("Gorda Springs",                    35.87641, -121.44614),
            ("Ragged Point Inn",                 35.78072, -121.33083),
            ("Hearst Castle entrance",           35.64540, -121.18414),
            # snapped to CA-1: the town-centre point lands on a dirt bluff trail
            ("San Simeon Acres (NIGHT 1 alt)",   35.59235, -121.12446),
        ],
    },
    {
        "id": "pch_day2_alt_gaviota",
        "name": "Day 2 variant - finish at Gaviota State Park instead of Refugio",
        "desc": "Stop 16 km earlier at Gaviota State Park, right where CA-1 meets "
                "US-101 at the coast. Shortest day 2; longest day 3.",
        "trim_to": "Gaviota State Park",
        "extra": [("Gaviota State Park (NIGHT 2 alt)", 34.47180, -120.22860)],
        "base": "STAGE2",
    },
    {
        "id": "pch_day2_alt_elcapitan",
        "name": "Day 2 variant - finish at El Capitan State Beach",
        "desc": "Push 3 km past Refugio to El Capitan State Beach - the third of "
                "the three Santa Barbara-coast hike/bike parks, and the one with "
                "the most services.",
        "trim_to": "Refugio State Beach (NIGHT 2)",
        "extra": [("El Capitan State Beach (NIGHT 2 alt)", 34.46000, -120.02400)],
        "base": "STAGE2",
    },
]

BASES = {"STAGE1": STAGE1, "STAGE2": STAGE2, "STAGE3": STAGE3}


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
