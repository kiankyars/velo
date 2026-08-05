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
        "id": "pch_day1_alt_pfeiffer",
        "name": "Day 1 variant - stop early at Big Sur Village / Pfeiffer",
        "desc": "Day 1 cut from 326 km to 282 km by stopping in Big Sur Village "
                "instead of pressing on to Limekiln. Worth having loaded: it is "
                "the decision point for whether you descend the Big Sur cliffs "
                "in the dark, and the village is the last place with food, water "
                "and a campground in one spot.",
        "trim_to": "Big Sur Village (River Inn)",
        "extra": [("Pfeiffer Big Sur SP (NIGHT 1 alt)", 36.25331, -121.78330)],
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
