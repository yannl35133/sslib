from .constants import *
from .logic import PoolEntrance, PoolExit

DUNGEON_ENTRANCES_POOL = [
    PoolEntrance(make_entrance(entrance), [make_exit(entrance)])
    for entrance in DUNGEON_ENTRANCES.values()
]
DUNGEON_REVERSE_ENTRANCES_POOL = [
    PoolExit(make_exit(entrance), [make_entrance(entrance)])
    for entrance in DUNGEON_ENTRANCES.values()
]

VANILLA_DUNGEON_ACCESSES = {
    SV: "Deep Woods - Skyview Exit",
    ET: "Eldin Volcano - Earth Temple Exit",
    LMF: "Lanayru Desert - LMF Exit",
    AC: "Lake Floria - Ancient Cistern Exit",
    SSH: "Sand Sea - Sandship Exit",
    FS: "Volcano Summit - Fire Sanctuary Exit",
    SK: "Skyloft - Sky Keep Exit",
}

DUNGEON_ACCESSES_POOL = [
    PoolExit(make_exit(exit), [make_entrance(exit)])
    for exit in VANILLA_DUNGEON_ACCESSES.values()
]
DUNGEON_REVERSE_ACCESSES_POOL = [
    PoolEntrance(make_entrance(exit), [make_exit(exit)])
    for exit in VANILLA_DUNGEON_ACCESSES.values()
]

DUNGEON_ENTRANCES_COMPLETE_POOLS = [
    (DUNGEON_ENTRANCES_POOL, DUNGEON_ACCESSES_POOL),
    (DUNGEON_REVERSE_ACCESSES_POOL, DUNGEON_REVERSE_ENTRANCES_POOL),
]

# Silent Realms
SILENT_REALMS = {
    "Skyloft Silent Realm ",
    "Faron Silent Realm ",
    "Lanayru Silent Realm ",
    "Eldin Silent Realm ",
}
SILENT_REALM_ENTRANCES_POOL = [
    PoolEntrance(realm + " - Entrance", [realm + " - Exit"]) for realm in SILENT_REALMS
]
SILENT_REALM_EXITS_POOL = [
    PoolExit(realm + " - Exit", [realm + " - Entrance"]) for realm in SILENT_REALMS
]

SILENT_REALM_ACCESSES = {
    "Trial Gate on Skyloft",
    "Trial Gate in Faron Woods",
    "Trial Gate in Lanayru Desert",
    "Trial Gate in Eldin Volcano",
}
SILENT_REALM_ACCESSES_POOL = [
    PoolExit(make_exit(access), [make_entrance(access)])
    for access in SILENT_REALM_ACCESSES
]
SILENT_REALM_REVERSE_ACCESSES_POOL = [
    PoolEntrance(make_entrance(access), [make_exit(access)])
    for access in SILENT_REALM_ACCESSES
]

SILENT_REALMNS_COMPLETE_POOLS = [
    (SILENT_REALM_ENTRANCES_POOL, SILENT_REALM_ACCESSES_POOL),
    (SILENT_REALM_REVERSE_ACCESSES_POOL, SILENT_REALM_EXITS_POOL),
]
