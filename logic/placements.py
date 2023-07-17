from typing import Any, List
from .constants import *
from .logic import Placement

# Single crystals
SINGLE_CRYSTAL_CHECKS = [
    "Upper Skyloft - Crystal in Link's Room",
    "Upper Skyloft - Crystal in Knight Academy Plant",
    "Upper Skyloft - Crystal in Zelda's Room",
    "Upper Skyloft - Crystal in Sparring Hall",
    "Central Skyloft - Crystal between Wooden Planks",
    "Central Skyloft - Crystal on West Cliff",
    "Central Skyloft - Crystal in Orielle and Parrow's House",
    "Central Skyloft - Crystal on Light Tower",
    "Skyloft Village - Crystal near Pumpkin Patch",
    "Central Skyloft - Crystal after Waterfall Cave",
    "Central Skyloft - Crystal in Loftwing Prison",
    "Central Skyloft - Crystal on Waterfall Island",
    "Sky - Crystal outside Lumpy Pumpkin",
    "Sky - Crystal inside Lumpy Pumpkin",
    "Sky - Crystal on Beedle's Ship",
]


# Tries to force an item to its vanilla location.
# Produces an error if this is not possible.
def norm_force_vanilla(list: List[str]):
    def norm_keys(norm: Callable[[str], EIN], checks: Dict[EIN, Any]) -> Placement:
        list2 = map(norm, list)
        dict = {k: EIN(checks[k]["original item"]) for k in list2}
        return Placement(locations=dict, items={v: k for k, v in dict.items()})

    return norm_keys


# Restricts an item to only be placeable in its vanilla location.
# This is always possible.
def norm_restrict_vanilla(locations: List[str]):
    def norm_keys(norm: Callable[[str], EIN], checks: Dict[EIN, Any]) -> Placement:
        locs2 = map(norm, locations)
        restriction = {EIN(checks[loc]["original item"]): loc for loc in locs2}
        return Placement(item_placement_limit=restriction)

    return norm_keys


SINGLE_CRYSTAL_PLACEMENT = norm_force_vanilla(SINGLE_CRYSTAL_CHECKS)


def norm_keys(dict: Dict[str, EIN]):
    def norm_keys(norm: Callable[[str], EIN]) -> Placement:
        dict2 = {norm(k): v for k, v in dict.items()}
        return Placement(locations=dict2, items={v: k for k, v in dict2.items()})

    return norm_keys


def norm_values(dict: Dict[EIN, str]):
    def norm_values(norm: Callable[[str], EIN]):
        dict2 = {k: norm(v) for k, v in dict.items()}
        return Placement(item_placement_limit=dict2)

    return norm_values


HARDCODED_PLACEMENT = norm_keys({})

BEEDLE_CHECKS = [
    "Beedle's Shop - First Outer Left Item",
    "Beedle's Shop - Second Outer Left Item",
    "Beedle's Shop - Third Outer Left Item",
    "Beedle's Shop - First Inner Left Item",
    "Beedle's Shop - Second Inner Left Item",
    "Beedle's Shop - First Inner Right Item",
    "Beedle's Shop - Second Inner Right Item",
    "Beedle's Shop - Third Inner Right Item",
    "Beedle's Shop - First Outer Right Item",
    "Beedle's Shop - Second Outer Right Item",
]
VANILLA_BEEDLE_PLACEMENT = norm_force_vanilla(BEEDLE_CHECKS)

RUPIN_CHECKS = [
    "Central Skyloft - Gear Shop - Top Left Item",
    "Central Skyloft - Gear Shop - Middle Left Item",
    "Central Skyloft - Gear Shop - Bottom Left Item",
    "Central Skyloft - Gear Shop - Left Front Item",
    "Central Skyloft - Gear Shop - Middle Front Item",
    "Central Skyloft - Gear Shop - Right Front Item",
    "Central Skyloft - Gear Shop - Bottom Right Item",
    "Central Skyloft - Gear Shop - Middle Right Item",
    "Central Skyloft - Gear Shop - Top Right Item",
]
VANILLA_RUPIN_PLACEMENT = norm_force_vanilla(RUPIN_CHECKS)

# The order of this list matters.
# It is used in gamepatches to provide custom text for each potion item.
LUV_CHECKS = [
    "Central Skyloft - Potion Shop - Outer Left Item",
    "Central Skyloft - Potion Shop - Inner Left Item",
    "Central Skyloft - Potion Shop - Middle Item",
    "Central Skyloft - Potion Shop - Inner Right Item",
    "Central Skyloft - Potion Shop - Outer Right Item",
]
VANILLA_LUV_PLACEMENT = norm_force_vanilla(LUV_CHECKS)

SMALL_KEY_CHECKS = [
    "Skyview - Chest behind Two Eyes",
    "Skyview - Chest behind Three Eyes",
    "Lanayru Mining Facility - First Chest in Hub Room",
    "Ancient Cistern - Chest in East Part",
    "Ancient Cistern - Bokoblin",
    "Sandship - Chest behind Combination Lock",
    "Sandship - Robot in Brig's Reward",
    "Fire Sanctuary - Chest in First Room",
    "Fire Sanctuary - Chest near First Trapped Mogma",
    "Fire Sanctuary - Chest after Bombable Wall",
    "Sky Keep - Chest after Dreadfuse",
    "Lanayru Caves - Golo's Gift",
]
VANILLA_SMALL_KEYS_PLACEMENT = norm_restrict_vanilla(SMALL_KEY_CHECKS)

DUNGEON_SMALL_KEYS_RESTRICTION = norm_values(
    {
        number(SMALL_KEY[SV], 0): SV + sep + "Main",
        number(SMALL_KEY[SV], 1): SV + sep + "Main",
        number(SMALL_KEY[LMF], 0): LMF + sep + "Main",
        number(SMALL_KEY[AC], 0): AC + sep + "Main",
        number(SMALL_KEY[AC], 1): AC + sep + "Main",
        number(SMALL_KEY[SSH], 0): SSH + sep + "Main",
        number(SMALL_KEY[SSH], 1): SSH + sep + "Main",
        number(SMALL_KEY[FS], 0): FS + sep + "Main",
        number(SMALL_KEY[FS], 1): FS + sep + "Main",
        number(SMALL_KEY[FS], 2): FS + sep + "Main",
        number(SMALL_KEY[SK], 0): SK,
    }
)

CAVES_KEY_RESTRICTION = norm_values({CAVES_KEY: "Lanayru - Caves"})


BOSS_KEY_CHECKS = [
    "Skyview - Boss Key Chest",
    "Earth Temple - Boss Key Chest",
    "Lanayru Mining Facility - Boss Key Chest",
    "Ancient Cistern - Boss Key Chest",
    "Sandship - Boss Key Chest",
    "Fire Sanctuary - Boss Key Chest",
]
VANILLA_BOSS_KEYS_PLACEMENT = norm_restrict_vanilla(BOSS_KEY_CHECKS)

DUNGEON_BOSS_KEYS_RESTRICTION = norm_values(
    {
        BOSS_KEY[SV]: SV,
        BOSS_KEY[ET]: ET,
        BOSS_KEY[LMF]: LMF,
        BOSS_KEY[AC]: AC,
        BOSS_KEY[SSH]: SSH,
        BOSS_KEY[FS]: FS,
    }
)

MAP_CHECKS = [
    "Skyview - Chest on Tree Branch",
    "Earth Temple - Chest in West Room",
    "Lanayru Mining Facility - Chest after Armos Fight",
    "Ancient Cistern - Chest after Whip Hooks",
    "Sandship - Chest before 4-Door Corridor",
    "Fire Sanctuary - Chest after Second Trapped Mogma",
    "Sky Keep - First Chest",
]
VANILLA_MAPS_PLACEMENT = norm_restrict_vanilla(MAP_CHECKS)

DUNGEON_MAPS_RESTRICTION = norm_values(
    {
        MAP[SV]: SV,
        MAP[ET]: ET,
        MAP[LMF]: LMF,
        MAP[AC]: AC,
        MAP[SSH]: SSH,
        MAP[FS]: FS,
        MAP[SK]: SK,
    }
)
DUNGEON_MAPS_RESTRICTED_RESTRICTION = norm_values(
    {
        MAP[SV]: SV + sep + "Main",
        MAP[ET]: ET + sep + "Main",
        MAP[LMF]: LMF + sep + "Main",
        MAP[AC]: AC + sep + "Main",
        MAP[SSH]: SSH + sep + "Main",
        MAP[FS]: FS + sep + "Main",
        MAP[SK]: SK + sep + "Main",
    }
)

VANILLA_TRIFORCES_PLACEMENT = norm_values(
    {
        TRIFORCE_OF_COURAGE: "Sky Keep - Triforce of Courage",
        TRIFORCE_OF_WISDOM: "Sky Keep - Triforce of Wisdom",
        TRIFORCE_OF_POWER: "Sky Keep - Triforce of Power",
    }
)

TRIFORCES_RESTRICTION = norm_values(
    {TRIFORCE_OF_COURAGE: SK, TRIFORCE_OF_WISDOM: SK, TRIFORCE_OF_POWER: SK}
)


VANILLA_RUPEES = norm_force_vanilla(RUPEE_CHECKS)
VANILLA_QUICK_BEETLE_RUPEES = norm_force_vanilla(QUICK_BEETLE_CHECKS)

TADTONE_CHECKS = [
    "Flooded Faron Woods - Yellow Tadtone under Lilypad",
    "Flooded Faron Woods - 8 Light Blue Tadtones near Viewing Platform",
    "Flooded Faron Woods - 4 Purple Tadtones under Viewing Platform",
    "Flooded Faron Woods - Red Moving Tadtone near Viewing Platform",
    "Flooded Faron Woods - Light Blue Tadtone under Great Tree Root",
    "Flooded Faron Woods - 8 Yellow Tadtones near Kikwi Elder",
    "Flooded Faron Woods - 4 Light Blue Moving Tadtones under Kikwi Elder",
    "Flooded Faron Woods - 4 Red Moving Tadtones North West of Great Tree",
    "Flooded Faron Woods - Green Tadtone behind Upper Bombable Rock",
    "Flooded Faron Woods - 2 Dark Blue Tadtones in Grass West of Great Tree",
    "Flooded Faron Woods - 8 Green Tadtones in West Tunnel",
    "Flooded Faron Woods - 2 Red Tadtones in Grass near Lower Bombable Rock",
    "Flooded Faron Woods - 16 Dark Blue Tadtones in the South West",
    "Flooded Faron Woods - 4 Purple Moving Tadtones near Floria Gate",
    "Flooded Faron Woods - Dark Blue Moving Tadtone inside Small Hollow Tree",
    "Flooded Faron Woods - 4 Yellow Tadtones under Small Hollow Tree",
    "Flooded Faron Woods - 8 Purple Tadtones in Clearing after Small Hollow Tree",
]

VANILLA_TADTONE_PLACEMENT = norm_restrict_vanilla(TADTONE_CHECKS)
