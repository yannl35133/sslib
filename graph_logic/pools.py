from .constants import *
from .logic import PoolEntrance, PoolExit

DUNGEON_ENTRANCES_POOL = {
    make_entrance(entrance): PoolEntrance(
        make_entrance(entrance), [make_exit(entrance)]
    )
    for entrance in DUNGEON_ENTRANCES.values()
}
DUNGEON_REVERSE_ENTRANCES_POOL = {
    make_exit(entrance): PoolExit(make_exit(entrance), [make_entrance(entrance)])
    for entrance in DUNGEON_ENTRANCES.values()
}

VANILLA_DUNGEON_ACCESSES = {
    SV: "Faron - Deep Woods - Temple Entrance",
    ET: "Eldin - Volcano - Temple Entrance",
    LMF: "Lanayru - Desert - Temple Entrance",
    AC: "Faron - Lake Floria - Temple Entrance",
    SSH: "Lanayru - Sand Sea - Temple Entrance",
    FS: "Eldin - Volcano Summit - Temple Entrance",
    SK: "Skyloft - Temple Entrance",
}

DUNGEON_ACCESSES_POOL = {
    make_exit(exit): PoolExit(make_exit(exit), [make_entrance(exit)])
    for exit in VANILLA_DUNGEON_ACCESSES.values()
}
DUNGEON_REVERSE_ACCESSES_POOL = {
    make_entrance(exit): PoolEntrance(make_entrance(exit), [make_exit(exit)])
    for exit in VANILLA_DUNGEON_ACCESSES.values()
}

DUNGEON_ENTRANCES_COMPLETE_POOLS = [
    (DUNGEON_ENTRANCES_POOL, DUNGEON_ACCESSES_POOL),
    (DUNGEON_REVERSE_ACCESSES_POOL, DUNGEON_REVERSE_ENTRANCES_POOL),
]

# Silent Realms
SILENT_REALMS = {
    "Skyloft - Silent Realm",
    "Faron - Silent Realm",
    "Lanayru - Silent Realm",
    "Eldin - Silent Realm",
}

make_entrance2 = lambda s: EIN(s + " - Entrance_ENTRANCE")
make_exit2 = lambda s: EIN(s + " - Exit_EXIT")

SILENT_REALM_ENTRANCES_POOL = {
    make_entrance2(realm): PoolEntrance(make_entrance2(realm), [make_exit2(realm)])
    for realm in SILENT_REALMS
}
SILENT_REALM_EXITS_POOL = {
    make_exit2(realm): PoolExit(make_exit2(realm), [make_entrance2(realm)])
    for realm in SILENT_REALMS
}

SILENT_REALM_ACCESSES = {
    "Skyloft - Trial Entrance",
    "Faron - Woods - Trial Entrance",
    "Lanayru - Desert - Trial Entrance",
    "Eldin - Volcano - Trial Entrance",
}
SILENT_REALM_ACCESSES_POOL = {
    make_exit(access): PoolExit(make_exit(access), [make_entrance(access)])
    for access in SILENT_REALM_ACCESSES
}
SILENT_REALM_REVERSE_ACCESSES_POOL = {
    make_entrance(access): PoolEntrance(make_entrance(access), [make_exit(access)])
    for access in SILENT_REALM_ACCESSES
}

SILENT_REALMNS_COMPLETE_POOLS = [
    (SILENT_REALM_ENTRANCES_POOL, SILENT_REALM_ACCESSES_POOL),
    (SILENT_REALM_REVERSE_ACCESSES_POOL, SILENT_REALM_EXITS_POOL),
]
