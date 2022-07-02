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
    "Beedle's Shop - 300 Rupee Item": number(PROGRESSIVE_POUCH, 1),
    "Beedle's Shop - 600 Rupee Item": number(PROGRESSIVE_POUCH, 2),
    "Beedle's Shop - 1200 Rupee Item": number(PROGRESSIVE_POUCH, 3),
    "Beedle's Shop - 800 Rupee Item": number(LIFE_MEDAL, 0),
    "Beedle's Shop - 1600 Rupee Item": number(HEART_PIECE, 0),
    "Beedle's Shop - First 100 Rupee Item": number(EXTRA_WALLET, 0),
    "Beedle's Shop - Second 100 Rupee Item": number(EXTRA_WALLET, 1),
    "Beedle's Shop - Third 100 Rupee Item": number(EXTRA_WALLET, 2),
    "Beedle's Shop - 50 Rupee Item": BUG_NET,
    "Beedle's Shop - 1000 Rupee Item": BUG_MEDAL,
}
VANILLA_BEEDLE_PLACEMENT = Placement(
    locations=VANILLA_BEEDLE, items={v: k for k, v in VANILLA_BEEDLE.items()}
)

VANILLA_SMALL_KEYS = {
    "Skyview - Chest behind Two Eyes": number(SV_SMALL_KEY, 0),
    "Skyview - Chest behind Three Eyes": number(SV_SMALL_KEY, 1),
    "Lanayru Mining Facility - Big Hub - Chest": number(LMF_SMALL_KEY, 0),
    "Ancient Cistern - East Part - Chest": number(AC_SMALL_KEY, 0),
    "Ancient Cistern - Basement Gutters - Bokoblin": number(AC_SMALL_KEY, 1),
    "Sandship - Chest behind Combination Lock": number(SSH_SMALL_KEY, 0),
    "Sandship - Brig Prison - Robot's Reward": number(SSH_SMALL_KEY, 1),
    "Fire Sanctuary - First Room - Chest": number(FS_SMALL_KEY, 0),
    "Fire Sanctuary - First Trapped Mogma Room - Chest": number(FS_SMALL_KEY, 1),
    "Fire Sanctuary - Second Trapped Mogma Room - Chest": number(FS_SMALL_KEY, 2),
    "Sky Keep - Chest after Dreadfuse": number(SK_SMALL_KEY, 0),
    "Lanayru Caves - Golo's Gift": CAVES_KEY,
}
VANILLA_SMALL_KEYS_PLACEMENT = Placement(
    locations=VANILLA_SMALL_KEYS, items={v: k for k, v in VANILLA_SMALL_KEYS.items()}
)

DUNGEON_SMALL_KEYS_RESTRICTION = Placement(
    item_placement_limit={
        number(SV_SMALL_KEY, 0): SV + sep + "Main",
        number(SV_SMALL_KEY, 1): SV + sep + "Main",
        number(LMF_SMALL_KEY, 0): LMF + sep + "Main",
        number(AC_SMALL_KEY, 0): AC + sep + "Main",
        number(AC_SMALL_KEY, 1): AC + sep + "Main",
        number(SSH_SMALL_KEY, 0): SSH + sep + "Main",
        number(SSH_SMALL_KEY, 1): SSH + sep + "Main",
        number(FS_SMALL_KEY, 0): FS + sep + "Main",
        number(FS_SMALL_KEY, 1): FS + sep + "Main",
        number(FS_SMALL_KEY, 2): FS + sep + "Main",
        number(SK_SMALL_KEY, 0): SK,
    }
)

CAVES_KEY_RESTRICTION = Placement(item_placement_limit={CAVES_KEY: "Lanayru - Caves"})


VANILLA_BOSS_KEYS = {
    "Skyview - Boss Key Chest": SV_BOSS_KEY,
    "Earth Temple - Boss Key Chest": ET_BOSS_KEY,
    "Lanayru Mining Facility - Boss Key Chest": LMF_BOSS_KEY,
    "Ancient Cistern - Boss Key Chest": AC_BOSS_KEY,
    "Sandship - Boss Key Chest": SSH_BOSS_KEY,
    "Fire Sanctuary - Boss Key Chest": FS_BOSS_KEY,
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
    "Skyview - Chest on Tree Branch": SV_MAP,
    "Earth Temple - West Room - Chest": ET_MAP,
    "Lanayru Mining Facility - Armos Fight Room - Chest": LMF_MAP,
    "Ancient Cistern - After Whip Hooks - Chest": AC_MAP,
    "Sandship - Chest before 4-Door Corridor": SSH_MAP,
    "Fire Sanctuary - Second Trapped Mogma Room - Reward": FS_MAP,
    "Sky Keep - First Chest": SK_MAP,
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
        SK_MAP: SK,
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
        SK_MAP: SK + sep + "Main",
    }
)
