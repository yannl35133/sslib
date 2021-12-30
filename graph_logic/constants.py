from collections import defaultdict
from typing import Set

sep = " - "

# Logic options

OPEN_THUNDERHEAD_OPTION = "Open Thunderhead option"
OPEN_LMF_OPTION = "Open LMF option"
ENABLED_BEEDLE_OPTION = "Enabled Beedle option"
HERO_MODE = "Hero-mode"
NO_BIT_CRASHES = "No BiT crashes"

LOGIC_OPTIONS = {
    OPEN_THUNDERHEAD_OPTION,
    OPEN_LMF_OPTION,
    ENABLED_BEEDLE_OPTION,
    HERO_MODE,
    NO_BIT_CRASHES,
}

# Locations

make_day = lambda s: s + "_DAY"
make_night = lambda s: s + "_NIGHT"
make_entrance = lambda s: s + "_ENTRANCE"
make_exit = lambda s: s + "_EXIT"


SV = "Skyview"
ET = "Earth Temple"
LMF = "Lanayru Mining Facility"
AC = "Ancient Cistern"
SSH = "Sandship"
FS = "Fire Sanctuary"
SK = "Sky Keep"

REGULAR_DUNGEONS = [SV, ET, LMF, AC, SSH, FS]
ALL_DUNGEONS = REGULAR_DUNGEONS + [SK]

# Items

ITEM_COUNTS = defaultdict(lambda: 1)


def number(name: str, index: int) -> str:
    if index >= ITEM_COUNTS[name]:
        raise ValueError("Index too high")
    if ITEM_COUNTS[name] == 1:
        return name
    return f"{name} #{index}"


def strip_item_number(item) -> str:
    if "#" not in item:
        return item
    return item[: item.index("#")]


def group(name: str, count: int) -> Set[str]:
    ITEM_COUNTS[name] = count
    if count == 1:
        return {name}
    return {f"{name} #{i}" for i in range(count)}


SLINGSHOT = "Slingshot"
BOMB_BAG = "Bomb Bag"
GUST_BELLOWS = "Gust Bellows"
WHIP = "Whip"
BOW = "Bow"
BUG_NET = "Bug Net"
CLAWSHOTS = "Clawshots"
WATER_SCALE = "Water Scale"
FIRESHIELD_EARRINGS = "Fireshield Earrings"
SEA_CHART = "Sea Chart"
EMERALD_TABLET = "Emerald Tablet"
RUBY_TABLET = "Ruby Tablet"
AMBER_TABLET = "Amber Tablet"
STONE_OF_TRIALS = "Stone of Trials"

BABY_RATTLE = "Baby Rattle"
CAWLINS_LETTER = "Cawlin's Letter"
HORNED_COLOSSUS_BEETLE = "Horned Colossus Beetle"
GODDESS_HARP = "Goddess Harp"
BALLAD_OF_THE_GODDESS = "Ballad of the Goddess"
FARORES_COURAGE = "Farore's Courage"
NAYRUS_WISDOM = "Nayru's Wisdom"
DINS_POWER = "Din's Power"
FARON_SOTH_PART = "Faron Song of the Hero Part"
ELDIN_SOTH_PART = "Eldin Song of the Hero Part"
LANAYRU_SOTH_PART = "Lanayru Song of the Hero Part"
SPIRAL_CHARGE = "Spiral Charge"

GRATITUDE_CRYSTAL_PACK = "Gratitude Crystal Pack"
GRATITUDE_CRYSTAL = "Gratitude Crystal"
PROGRESSIVE_SWORD = "Progressive Sword"
PROGRESSIVE_MITTS = "Progressive Mitts"
PROGRESSIVE_BEETLE = "Progressive Beetle"
PROGRESSIVE_POUCH = "Progressive Pouch"
KEY_PIECE = "Key Piece"
EMPTY_BOTTLE = "Empty Bottle"
PROGRESSIVE_WALLET = "Progressive Wallet"
EXTRA_WALLET = "Extra Wallet"

GRATITUDE_CRYSTAL_PACKS = group(GRATITUDE_CRYSTAL_PACK, 13)
GRATITUDE_CRYSTALS = group(GRATITUDE_CRYSTAL, 15)
PROGRESSIVE_SWORDS = group(PROGRESSIVE_SWORD, 6)
PROGRESSIVE_MITTS_ALL = group(PROGRESSIVE_MITTS, 2)
PROGRESSIVE_BEETLES = group(PROGRESSIVE_BEETLE, 2)
PROGRESSIVE_POUCHES = group(PROGRESSIVE_POUCH, 5)
KEY_PIECES = group(KEY_PIECE, 5)
EMPTY_BOTTLES = group(EMPTY_BOTTLE, 5)
PROGRESSIVE_WALLETS = group(PROGRESSIVE_WALLET, 4)
EXTRA_WALLETS = group(EXTRA_WALLET, 3)

small_key = lambda d: d + " Small Key"
SV_SMALL_KEY = small_key(SV)
ET_SMALL_KEY = small_key(ET)
LMF_SMALL_KEY = small_key(LMF)
AC_SMALL_KEY = small_key(AC)
SSH_SMALL_KEY = small_key(SSH)
FS_SMALL_KEY = small_key(FS)
SK_SMALL_KEY = small_key(SK)

boss_key = lambda d: d + " Boss Key"
SV_BOSS_KEY = boss_key(SV)
ET_BOSS_KEY = boss_key(ET)
LMF_BOSS_KEY = boss_key(LMF)
AC_BOSS_KEY = boss_key(AC)
SSH_BOSS_KEY = boss_key(SSH)
FS_BOSS_KEY = boss_key(FS)
SK_BOSS_KEY = boss_key(SK)

map = lambda d: d + " Map"
SV_MAP = map(SV)
ET_MAP = map(ET)
LMF_MAP = map(LMF)
AC_MAP = map(AC)
SSH_MAP = map(SSH)
FS_MAP = map(FS)
SK_MAP = map(SK)

CAVES_KEY = "LanayruCaves Small Key"

SV_SMALL_KEYS = group(SV_SMALL_KEY, 2)
ET_SMALL_KEYS = group(ET_SMALL_KEY, 0)
LMF_SMALL_KEYS = group(LMF_SMALL_KEY, 1)
AC_SMALL_KEYS = group(AC_SMALL_KEY, 2)
SSH_SMALL_KEYS = group(SSH_SMALL_KEY, 2)
FS_SMALL_KEYS = group(FS_SMALL_KEY, 3)
SK_SMALL_KEYS = group(SK_SMALL_KEY, 1)

SV_BOSS_KEYS = group(SV_BOSS_KEY, 1)
ET_BOSS_KEYS = group(ET_BOSS_KEY, 1)
LMF_BOSS_KEYS = group(LMF_BOSS_KEY, 1)
AC_BOSS_KEYS = group(AC_BOSS_KEY, 1)
SSH_BOSS_KEYS = group(SSH_BOSS_KEY, 1)
FS_BOSS_KEYS = group(FS_BOSS_KEY, 1)
SK_BOSS_KEYS = group(SK_BOSS_KEY, 0)

WOODEN_SHIELD = "Wooden Shield"
HYLIAN_SHIELD = "Hylian Shield"
CURSED_MEDAL = "Cursed Medal"
TREASURE_MEDAL = "Treasure Medal"
POTION_MEDAL = "Potion Medal"
SMALL_SEED_SATCHEL = "Small Seed Satchel"
SMALL_BOMB_BAG = "Small Bomb Bag"
SMALL_QUIVER = "Small Quiver"
BUG_MEDAL = "Bug Medal"

HEART_MEDAL = "Heart Medal"
RUPEE_MEDAL = "Rupee Medal"
HEART_PIECE = "Heart Piece"
HEART_CONTAINER = "Heart Container"
LIFE_MEDAL = "Life Medal"

HEART_MEDALS = group("Heart Medal", 2)
RUPEE_MEDALS = group("Rupee Medal", 2)
HEART_PIECES = group("Heart Piece", 24)
HEART_CONTAINERS = group("Heart Container", 6)
LIFE_MEDALS = group("Life Medal", 2)

BLUE_RUPEE = "Blue Rupee"
RED_RUPEE = "Red Rupee"
SILVER_RUPEE = "Silver Rupee"
GOLD_RUPEE = "Gold Rupee"
SEMI_RARE_TREASURE = "Semi Rare Treasure"
GOLDEN_SKULL = "Golden Skull"
RARE_TREASURE = "Rare Treasure"
EVIL_CRYSTAL = "Evil Crystal"
ELDIN_ORE = "Eldin Ore"
GODDESS_PLUME = "Goddess Plume"
DUSK_RELIC = "Dusk Relic"
TUMBLEWEED = "Tumbleweed"
FIVE_BOMBS = "5 Bombs"

BLUE_RUPEES = group(BLUE_RUPEE, 4)
RED_RUPEES = group(RED_RUPEE, 25)
SILVER_RUPEES = group(SILVER_RUPEE, 12)
GOLD_RUPEES = group(GOLD_RUPEE, 10)
SEMI_RARE_TREASURES = group(SEMI_RARE_TREASURE, 10)
RARE_TREASURES = group(RARE_TREASURE, 12)
EVIL_CRYSTALS = group(EVIL_CRYSTAL, 2)
ELDIN_ORES = group(ELDIN_ORE, 2)

RUPOOR = "Rupoor"

PROGRESS_ITEMS = (
    {
        SLINGSHOT,
        BOMB_BAG,
        GUST_BELLOWS,
        WHIP,
        BOW,
        BUG_NET,
        CLAWSHOTS,
        WATER_SCALE,
        FIRESHIELD_EARRINGS,
        SEA_CHART,
        EMERALD_TABLET,
        RUBY_TABLET,
        AMBER_TABLET,
        STONE_OF_TRIALS,
        BABY_RATTLE,
        CAWLINS_LETTER,
        HORNED_COLOSSUS_BEETLE,
        GODDESS_HARP,
        BALLAD_OF_THE_GODDESS,
        FARORES_COURAGE,
        NAYRUS_WISDOM,
        DINS_POWER,
        FARON_SOTH_PART,
        ELDIN_SOTH_PART,
        LANAYRU_SOTH_PART,
        SPIRAL_CHARGE,
    }
    | GRATITUDE_CRYSTAL_PACKS
    | GRATITUDE_CRYSTALS
    | PROGRESSIVE_SWORDS
    | PROGRESSIVE_MITTS_ALL
    | PROGRESSIVE_BEETLES
    | PROGRESSIVE_POUCHES
    | KEY_PIECES
    | EMPTY_BOTTLES
    | PROGRESSIVE_WALLETS
    | EXTRA_WALLETS
)

NONPROGRESS_ITEMS = (
    {
        WOODEN_SHIELD,
        HYLIAN_SHIELD,
        CURSED_MEDAL,
        TREASURE_MEDAL,
        POTION_MEDAL,
        SMALL_SEED_SATCHEL,
        SMALL_BOMB_BAG,
        SMALL_QUIVER,
        BUG_MEDAL,
    }
    | HEART_MEDALS
    | RUPEE_MEDALS
    | HEART_PIECES
    | HEART_CONTAINERS
    | LIFE_MEDALS
)

CONSUMABLE_ITEMS = (
    {
        GOLDEN_SKULL,
        RARE_TREASURE,
        EVIL_CRYSTAL,
        ELDIN_ORE,
    }
    | BLUE_RUPEES
    | RED_RUPEES
    | SILVER_RUPEES
    | GOLD_RUPEES
    | SEMI_RARE_TREASURES
    | RARE_TREASURES
    | EVIL_CRYSTALS
    | ELDIN_ORES
)

# Once all the items that have a fixed number per seed are used up, this list is used.
# Unlike the other lists, this one does not have items removed from it as they are placed.
# The number of each item in this list is instead its weighting relative to the other items in the list.
DUPLICABLE_ITEMS = {
    BLUE_RUPEE,
    RED_RUPEE,
    SEMI_RARE_TREASURE,
    RARE_TREASURE,
}
DUPLICABLE_COUNTERPROGRESS_ITEMS = {RUPOOR}

# note: Lanayru Caves is technically not a dungeon, but has to be treated as such for non key sanity
SMALL_KEYS = (
    SV_SMALL_KEYS
    | ET_SMALL_KEYS
    | LMF_SMALL_KEYS
    | AC_SMALL_KEYS
    | SSH_SMALL_KEYS
    | FS_SMALL_KEYS
    | SK_SMALL_KEYS
    | {CAVES_KEY}
)
BOSS_KEYS = (
    SV_BOSS_KEYS
    | ET_BOSS_KEYS
    | LMF_BOSS_KEYS
    | AC_BOSS_KEYS
    | SSH_BOSS_KEYS
    | FS_BOSS_KEYS
    | SK_BOSS_KEYS
)
MAPS = {SV_MAP, ET_MAP, LMF_MAP, AC_MAP, SSH_MAP, FS_MAP, SK_MAP}

INVENTORY_ITEMS = (
    PROGRESS_ITEMS
    | NONPROGRESS_ITEMS
    | CONSUMABLE_ITEMS
    | SMALL_KEYS
    | BOSS_KEYS
    | MAPS
)

TABLETS = [EMERALD_TABLET, RUBY_TABLET, AMBER_TABLET]

SWORD_COUNT = {
    "Swordless": 0,
    "Practice Sword": 1,
    "Goddess Sword": 2,
    "Goddess Longsword": 3,
    "Goddess White Sword": 4,
    "Master Sword": 5,
    "True Master Sword": 6,
}


str_entrance = "Entrance"
DUNGEON_ENTRANCES = {
    SV: SV + sep + str_entrance,
    ET: ET + sep + str_entrance,
    LMF: LMF + sep + str_entrance,
    AC: AC + sep + str_entrance,
    SSH: SSH + sep + str_entrance,
    FS: FS + sep + str_entrance,
    SK: SK + sep + str_entrance,
}

DUNGEON_FINAL_CHECK = {
    SV: SV + sep + RUBY_TABLET,
    ET: ET + sep + AMBER_TABLET,
    LMF: LMF + sep + GODDESS_HARP,
    AC: AC + sep + "Farore's Flame",
    SSH: SSH + sep + "Nayru's Flame",
    FS: FS + sep + "Din's Flame",
    SK: SK + sep + "Complete Triforce",
}

BATn = lambda n: f"Batreaux - {n} Crystals"
BATREAUX_FIRST_CHECK_ABOVE = {
    0: BATn(5),
    5: BATn(10),
    10: BATn(30),
    30: BATn(40),
    40: BATn(50),
    50: BATn(70),
    70: BATn(80),
    80: None,
}

GOT_OPENING_REQUIREMENT = "GoT Opening Requirement"
GOT_RAISING_REQUIREMENT = "GoT Raising Requirement"
HORDE_DOOR_REQUIREMENT = "Horde Door Requirement"

LINKS_ROOM = "Knight Academy - Link's Room"
SONG_IMPA_CHECK = "Sealed Grounds - Song from Impa"

trick = lambda s: s + " Trick"


# Retro-compatibility
from collections import OrderedDict

SILENT_REALMS = OrderedDict(
    [
        ("Skyloft Silent Realm", "Skyloft Trial Gate"),
        ("Faron Silent Realm", "Faron Trial Gate"),
        ("Lanayru Silent Realm", "Lanayru Trial Gate"),
        ("Eldin Silent Realm", "Eldin Trial Gate"),
    ]
)

SILENT_REALM_CHECKS = OrderedDict(
    [
        ("Skyloft Silent Realm - Stone of Trials", "Trial Gate on Skyloft"),
        ("Faron Silent Realm - Water Scale", "Trial Gate in Faron Woods"),
        ("Lanayru Silent Realm - Clawshots", "Trial Gate in Lanayru Desert"),
        ("Eldin Silent Realm - Fireshield Earrings", "Trial Gate in Eldin Volcano"),
    ]
)
