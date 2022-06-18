from .constants import *
from .logic import Placement

# Single crystals
SINGLE_CRYSTAL_CHECKS = [
    "Knight Academy - Link's Room - Crystal",
    "Knight Academy - Crystal in Plant",
    "Knight Academy - Zelda's Room - Crystal",
    "Sparring Hall - Crystal",
    "Skyloft - Crystal between Wooden Planks",
    "Skyloft - Crystal on West Cliff",
    "Skyloft - Orielle and Parrow's House - Crystal",
    "Skyloft - Crystal on Light Tower",
    "Skyloft - Crystal near Pumpkin Patch",
    "Skyloft - Crystal after Waterfall Cave",
    "Skyloft - Crystal in Loftwing Prison",
    "Skyloft - Waterfall Island - Crystal",
    "Sky - Pumpkin Landing - Crystal",
    "Sky - Lumpy Pumpkin - Crystal",
    "Sky - Crystal on Beedle's Ship",
]


def SINGLE_CRYSTAL_PLACEMENT(norm):
    return Placement(
        items={
            crystal: norm(loc)
            for loc, crystal in zip(SINGLE_CRYSTAL_CHECKS, GRATITUDE_CRYSTALS)
        },
        locations={
            norm(loc): crystal
            for loc, crystal in zip(SINGLE_CRYSTAL_CHECKS, GRATITUDE_CRYSTALS)
        },
    )


VANILLA_BEEDLE = {
    "Beedle - 300 Rupee Item": number(PROGRESSIVE_POUCH, 1),
    "Beedle - 600 Rupee Item": number(PROGRESSIVE_POUCH, 2),
    "Beedle - 1200 Rupee Item": number(PROGRESSIVE_POUCH, 3),
    "Beedle - 800 Rupee Item": number(LIFE_MEDAL, 0),
    "Beedle - 1600 Rupee Item": number(HEART_PIECE, 0),
    "Beedle - First 100 Rupee Item": number(EXTRA_WALLET, 0),
    "Beedle - Second 100 Rupee Item": number(EXTRA_WALLET, 1),
    "Beedle - Third 100 Rupee Item": number(EXTRA_WALLET, 2),
    "Beedle - 50 Rupee Item": BUG_NET,
    "Beedle - 1000 Rupee Item": BUG_MEDAL,
}
VANILLA_BEEDLE_PLACEMENT = Placement(
    locations=VANILLA_BEEDLE, items={v: k for k, v in VANILLA_BEEDLE.items()}
)

VANILLA_SMALL_KEYS = {
    "Skyview - Behind Two Eyes": number(SV_SMALL_KEY, 0),
    "Skyview - Behind Three Eyes": number(SV_SMALL_KEY, 1),
    "Lanayru Mining Facility - First Chest in Hub Room": number(LMF_SMALL_KEY, 0),
    "Ancient Cistern - Small Key Chest": number(AC_SMALL_KEY, 0),
    "Ancient Cistern - Bokoblin": number(AC_SMALL_KEY, 1),
    "Sandship - Behind Combination Lock": number(SSH_SMALL_KEY, 0),
    "Sandship - Robot in Brig": number(SSH_SMALL_KEY, 1),
    "Fire Sanctuary - First Room": number(FS_SMALL_KEY, 0),
    "Fire Sanctuary - Second Small Key Chest": number(FS_SMALL_KEY, 1),
    "Fire Sanctuary - Third Small Key Chest": number(FS_SMALL_KEY, 2),
    "Sky Keep - Small Key Chest": number(SK_SMALL_KEY, 0),
    "Lanayru Caves - Golo": CAVES_KEY,
}
VANILLA_SMALL_KEYS_PLACEMENT = Placement(
    locations=VANILLA_SMALL_KEYS, items={v: k for k, v in VANILLA_SMALL_KEYS.items()}
)

DUNGEON_SMALL_KEYS_RESTRICTION = Placement(
    item_placement_limit={
        number(SV_SMALL_KEY, 0): SV,
        number(SV_SMALL_KEY, 1): SV,
        number(LMF_SMALL_KEY, 0): LMF,
        number(AC_SMALL_KEY, 0): AC,
        number(AC_SMALL_KEY, 1): AC,
        number(SSH_SMALL_KEY, 0): SSH,
        number(SSH_SMALL_KEY, 1): SSH,
        number(FS_SMALL_KEY, 0): FS,
        number(FS_SMALL_KEY, 1): FS,
        number(FS_SMALL_KEY, 2): FS,
        number(SK_SMALL_KEY, 0): SK,
    }
)

CAVES_KEY_RESTRICTION = Placement(item_placement_limit={CAVES_KEY: "Lanayru - Caves"})


VANILLA_BOSS_KEYS = {
    "Skyview - Boss Key": SV_BOSS_KEY,
    "Earth Temple - Boss Key": ET_BOSS_KEY,
    "Lanayru Mining Facility - Boss Key": LMF_BOSS_KEY,
    "Ancient Cistern - Boss Key": AC_BOSS_KEY,
    "Sandship - Boss Key": SSH_BOSS_KEY,
    "Fire Sanctuary - Boss Key": FS_BOSS_KEY,
}
VANILLA_BOSS_KEYS_PLACEMENT = Placement(
    locations=VANILLA_BOSS_KEYS, items={v: k for k, v in VANILLA_BOSS_KEYS.items()}
)

DUNGEON_BOSS_KEYS_RESTRICTION = Placement(
    item_placement_limit={
        SV_BOSS_KEY: SV,
        ET_BOSS_KEY: ET,
        LMF_BOSS_KEY: LMF,
        AC_BOSS_KEY: AC,
        SSH_BOSS_KEY: SSH,
        FS_BOSS_KEY: FS,
    }
)

VANILLA_MAPS = {
    "Skyview - Map Chest": SV_MAP,
    "Earth Temple - Map Chest": ET_MAP,
    "Lanayru Mining Facility - Map Chest": LMF_MAP,
    "Ancient Cistern - Map Chest": AC_MAP,
    "Sandship - Map Chest": SSH_MAP,
    "Fire Sanctuary - Map Chest": FS_MAP,
    "Sky Keep - Map Chest": SK_MAP,
}
VANILLA_MAPS_PLACEMENT = Placement(
    locations=VANILLA_MAPS, items={v: k for k, v in VANILLA_MAPS.items()}
)

DUNGEON_MAPS_RESTRICTION = Placement(
    item_placement_limit={
        SV_MAP: SV,
        ET_MAP: ET,
        LMF_MAP: LMF,
        AC_MAP: AC,
        SSH_MAP: SSH,
        FS_MAP: FS,
    }
)
DUNGEON_MAPS_RESTRICTED_RESTRICTION = Placement(
    item_placement_limit={
        SV_MAP: SV + sep + "Main",
        ET_MAP: ET + sep + "Main",
        LMF_MAP: LMF + sep + "Main",
        AC_MAP: AC + sep + "Main",
        SSH_MAP: SSH + sep + "Main",
        FS_MAP: FS + sep + "Main",
    }
)
