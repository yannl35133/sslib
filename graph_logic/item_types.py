PROGRESS_ITEMS = (
    [
        "Slingshot",
        "Bomb Bag",
        "Gust Bellows",
        "Whip",
        "Bow",
        "Bug Net",
        "Water Scale",
        "Fireshield Earrings",
        "Clawshots",
        "Stone of Trials",
        "Sea Chart",
        "Emerald Tablet",
        "Ruby Tablet",
        "Amber Tablet",
        "Baby Rattle",
        "Cawlin's Letter",
        "Horned Colossus Beetle",
        "Goddess Harp",
        "Ballad of the Goddess",
        "Farore's Courage",
        "Nayru's Wisdom",
        "Din's Power",
        "Faron Song of the Hero Part",
        "Eldin Song of the Hero Part",
        "Lanayru Song of the Hero Part",
        "Spiral Charge"
        # "Revitalizing Potion" # causes problems in events, as it's treated like you buy a potion
    ]
    + ["Gratitude Crystal Pack"] * 13
    + ["Gratitude Crystal"] * 15
    + ["Progressive Sword"] * 6
    + ["Progressive Mitts"] * 2
    + ["Progressive Beetle"] * 2
    + ["Progressive Pouch"] * 5
    + ["Key Piece"] * 5
    + ["Empty Bottle"] * 5
    + ["Progressive Wallet"] * 4
    + ["Extra Wallet"] * 3
)

NONPROGRESS_ITEMS = (
    [
        "Wooden Shield",
        "Hylian Shield",
        "Cursed Medal",
        "Treasure Medal",
        "Potion Medal",
        "Small Seed Satchel",
        "Small Bomb Bag",
        "Small Quiver",
        "Bug Medal",
    ]
    + ["Heart Medal"] * 2
    + ["Rupee Medal"] * 2
    + ["Heart Piece"] * 24
    + ["Heart Container"] * 6
    + ["Life Medal"] * 2
)

CONSUMABLE_ITEMS = (
    4 * ["Blue Rupee"]
    + 25 * ["Red Rupee"]
    + 12 * ["Silver Rupee"]
    + 10 * ["Gold Rupee"]
    + 10 * ["Semi Rare Treasure"]
    + 1 * ["Golden Skull"]
    + 12 * ["Rare Treasure"]
    + 2 * ["Evil Crystal"]
    + 2 * ["Eldin Ore"]
    + 1 * ["Goddess Plume"]
    + 1 * ["Dusk Relic"]
    + 1 * ["Tumbleweed"]
    + 1 * ["5 Bombs"]
)

# Once all the items that have a fixed number per seed are used up, this list is used.
# Unlike the other lists, this one does not have items removed from it as they are placed.
# The number of each item in this list is instead its weighting relative to the other items in the list.
DUPLICABLE_ITEMS = [
    "Blue Rupee",
    "Red Rupee",
    "Semi Rare Treasure",
    "Rare Treasure",
]

DUPLICABLE_COUNTERPROGRESS_ITEMS = ["Rupoor"]

# note: Lanayru Caves is technically not a dungeon, but has to be treated as such for non key sanity

SMALL_KEYS = (
    ["Lanayru Caves Key"] * 1
    + ["Skyview Small Key"] * 2
    + ["Earth Temple Small Key"] * 0
    + ["Lanayru Mining Facility Small Key"] * 1
    + ["Ancient Cistern Small Key"] * 2
    + ["Sandship Small Key"] * 2
    + ["Fire Sanctuary Small Key"] * 3
    + ["Sky Keep Small Key"] * 1
)

BOSS_KEYS = (
    ["Skyview Boss Key"] * 1
    + ["Earth Temple Boss Key"] * 1
    + ["Lanayru Mining Facility Boss Key"] * 1
    + ["Ancient Cistern Boss Key"] * 1
    + ["Sandship Boss Key"] * 1
    + ["Fire Sanctuary Boss Key"] * 1
    + ["Sky Keep Boss Key"] * 0
)

MAPS = (
    ["Skyview Map"]
    + ["Earth Temple Map"]
    + ["Lanayru Mining Facility Map"]
    + ["Ancient Cistern Map"]
    + ["Sandship Map"]
    + ["Fire Sanctuary Map"]
    + ["Sky Keep Map"]
)

INVENTORY_ITEMS = (
    PROGRESS_ITEMS
    + SMALL_KEYS
    + BOSS_KEYS
    + MAPS
    + NONPROGRESS_ITEMS
    + CONSUMABLE_ITEMS
)

ALL_ITEM_NAMES = set(
    PROGRESS_ITEMS
    + NONPROGRESS_ITEMS
    + CONSUMABLE_ITEMS
    + DUPLICABLE_ITEMS
    + DUPLICABLE_COUNTERPROGRESS_ITEMS
    + SMALL_KEYS
    + BOSS_KEYS
    + MAPS
)