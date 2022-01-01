import random
from typing import List  # Only for typing purposes

from options import Options, OPTIONS
from .backwards_filled_algorithm import BFA, RandomizationSettings
from .logic import Logic, Placement, LogicSettings
from .logic_input import Areas
from .logic_expression import DNFInventory, InventoryAtom, LogicExpression
from .inventory import Inventory, EXTENDED_ITEM
from yaml_files import graph_requirements, checks, hints, map_exits
from .constants import *
from .placements import *
from .pools import *


class Rando:
    def __init__(self, options: Options, rng: random.Random):

        self.options = options
        self.rng = rng

        self.areas = Areas(graph_requirements, checks, hints, map_exits)
        self.short_to_full = self.areas.short_to_full

        self.placement: Placement = self.options.get("placement", Placement())
        self.parse_options()
        self.initial_placement = self.placement.copy()

        starting_inventory_BFA = Inventory(
            {
                item
                for item in EXTENDED_ITEM.items()
                if item in INVENTORY_ITEMS and item not in self.placement.items
            }
        )
        starting_area = LINKS_ROOM
        exit_pools = DUNGEON_ENTRANCES_COMPLETE_POOLS + SILENT_REALMNS_COMPLETE_POOLS

        additional_requirements = (
            self.logic_options_requirements
            | self.endgame_requirements
            | {loc: DNFInventory(EXTENDED_ITEM.banned_bit()) for loc in self.banned}
        )

        logic_settings = LogicSettings(
            exit_pools, starting_inventory_BFA, starting_area, additional_requirements
        )

        self.logic = Logic(self.areas, logic_settings, self.placement)

        if self.options["logic-mode"] == "No Logic":
            for i in range(len(self.logic.requirements)):
                self.logic.requirements[i] = DNFInventory(True)

        self.rando_algo = BFA(self.logic, self.rng, self.randosettings)

        self.retro_compatibility()

    def randomize(self):
        self.rando_algo.randomize()

    def parse_options(self):
        # Initialize location related attributes.
        self.randomize_required_dungeons()  # self.required_dungeons, self.unrequired_dungeons
        self.randomize_starting_items()  # self.starting_items
        self.ban_the_banned()  # self.banned

        self.get_endgame_requirements()  # self.endgame_requirements

        self.initialize_items()  # self.randosettings

        self.set_placement_options()  # self.logic_options_requirements

    def randomize_required_dungeons(self):
        """
        Selects the required dungeons randomly based on options
        """
        indices = list(range(len(REGULAR_DUNGEONS)))
        self.rng.shuffle(indices)
        req_indices = indices[: self.options["required-dungeon-count"]]
        unreq_indices = indices[self.options["required-dungeon-count"] :]
        req_indices.sort()
        unreq_indices.sort()
        self.required_dungeons = [REGULAR_DUNGEONS[i] for i in req_indices]
        self.unrequired_dungeons = [REGULAR_DUNGEONS[i] for i in unreq_indices]

    def randomize_starting_items(self):
        """
        Chooses all items the player has at the start,
        for tablet randomizer adds random tablets
        """
        starting_items = Inventory(
            (PROGRESSIVE_SWORD, SWORD_COUNT[self.options["starting-sword"]])
        )

        for tablet in self.rng.sample(TABLETS, k=self.options["starting-tablet-count"]):
            starting_items |= Inventory((tablet, 1))

        # if self.options.get('start-with-sailcloth', True):
        #   starting_items |= Inventory('Sailcloth')
        if self.options["start-with-pouch"]:
            starting_items |= Inventory((PROGRESSIVE_POUCH, 1))

        self.starting_items = starting_items

    def ban_the_banned(self):
        self.banned = []
        if self.options["empty-unrequired-dungeons"]:
            self.banned.extend(
                DUNGEON_ENTRANCES[dungeon] for dungeon in self.unrequired_dungeons
            )

            if self.options["skip-skykeep"]:
                self.banned.append(DUNGEON_ENTRANCES[SK])

        first_banned_batreaux_check = BATREAUX_FIRST_CHECK_ABOVE[
            self.options["max-batreaux-reward"]
        ]
        if first_banned_batreaux_check is not None:
            self.banned.append(first_banned_batreaux_check)

        banned_types = set(self.options["banned-types"])
        for loc in checks:
            check_types = set(checks[loc]["type"].split(","))
            if not set.isdisjoint(banned_types, check_types):
                self.banned.append(loc)

    def get_endgame_requirements(self):
        # needs to be able to open GoT and open it, requires required dungeons
        got_raising_requirement = (
            DNFInventory(self.short_to_full(SONG_IMPA_CHECK))
            if self.options["got-start"]
            else DNFInventory(True)
        )
        got_opening_requirement = InventoryAtom(
            PROGRESSIVE_SWORD, SWORD_COUNT[self.options["got-sword-requirement"]]
        )
        horde_door_requirement = (
            DNFInventory(self.short_to_full(DUNGEON_FINAL_CHECK[SK]))
            if not self.options["skip-skykeep"]
            else DNFInventory(True)
        )

        dungeons_req = Inventory()
        for dungeon in self.required_dungeons:
            dungeons_req |= Inventory(self.short_to_full(DUNGEON_FINAL_CHECK[dungeon]))

        if self.options["got-dungeon-requirement"] == "Required":
            got_opening_requirement &= DNFInventory(dungeons_req)
        elif self.options["got-dungeon-requirement"] == "Unrequired":
            horde_door_requirement &= DNFInventory(dungeons_req)

        self.endgame_requirements = {
            GOT_RAISING_REQUIREMENT: got_raising_requirement,
            GOT_OPENING_REQUIREMENT: got_opening_requirement,
            HORDE_DOOR_REQUIREMENT: horde_door_requirement,
        }

    def initialize_items(self):
        # Initialize item related attributes.
        must_be_placed_items = (
            PROGRESS_ITEMS | NONPROGRESS_ITEMS | SMALL_KEYS | BOSS_KEYS
        )
        if self.options["map-mode"] != "Removed":
            must_be_placed_items |= MAPS

        for item in self.starting_items.intset:
            item_name = EXTENDED_ITEM.get_item_name(item)
            must_be_placed_items.remove(item_name)

        may_be_placed_items: List[EIN | str] = list(CONSUMABLE_ITEMS)
        duplicable_items = DUPLICABLE_ITEMS

        rupoor_mode = self.options["rupoor-mode"]
        if rupoor_mode != "Off":
            duplicable_items = DUPLICABLE_COUNTERPROGRESS_ITEMS  # Rupoors
            if rupoor_mode == "Added":
                may_be_placed_items += [RUPOOR] * 15
            else:
                self.rng.shuffle(may_be_placed_items)
                replace_end_index = len(may_be_placed_items)
                if rupoor_mode == "Rupoor Mayhem":
                    replace_end_index //= 2
                may_be_placed_items = may_be_placed_items[replace_end_index:]

        self.randosettings = RandomizationSettings(
            must_be_placed_items, may_be_placed_items, duplicable_items
        )

    def set_placement_options(self):
        shop_mode = self.options["shop-mode"]

        self.logic_options_requirements = {
            OPEN_THUNDERHEAD_OPTION: self.options["open-thunderhead"] == "Open",
            OPEN_LMF_OPTION: self.options["open-lmf"] == "Open",
            ENABLED_BEEDLE_OPTION: shop_mode != "Always Junk",
            HERO_MODE: self.options["fix-bit-crashes"],
            NO_BIT_CRASHES: self.options["hero-mode"],
        }

        self.placement |= SINGLE_CRYSTAL_PLACEMENT

        if self.options["sword-dungeon-reward"]:
            swords_to_place = {
                item
                for item in self.randosettings.must_be_placed_items
                if strip_item_number(item) == PROGRESSIVE_SWORD
            }
            dungeons = self.required_dungeons.copy()
            self.rng.shuffle(dungeons)
            for dungeon, sword in zip(dungeons, swords_to_place):
                final_check = self.short_to_full(DUNGEON_FINAL_CHECK[dungeon])
                self.placement |= Placement(
                    items={sword: final_check},
                    locations={final_check: sword},
                )

        enabled_tricks = set(self.options["enabled-tricks-bitless"])

        for trick_name in OPTIONS["Enabled Tricks BiTless"]["choices"]:
            self.logic_options_requirements[trick(trick_name)] = DNFInventory(
                trick_name in enabled_tricks
            )

        if shop_mode == "Vanilla":
            self.placement |= VANILLA_BEEDLE_PLACEMENT
        elif shop_mode == "Randomized":
            pass
        elif shop_mode == "Always Junk":
            pass

        small_key_mode = self.options["small-key-mode"]
        boss_key_mode = self.options["boss-key-mode"]
        map_mode = self.options["map-mode"]
        # remove small keys from the dungeon pool if small key sanity is enabled
        if small_key_mode == "Vanilla":
            self.placement |= VANILLA_SMALL_KEYS_PLACEMENT
        elif small_key_mode == "Own Dungeon - Restricted":
            self.placement |= DUNGEON_SMALL_KEYS_RESTRICTION
            self.placement |= CAVES_KEY_RESTRICTION
        elif small_key_mode == "Lanayru Caves Key Only":
            self.placement |= DUNGEON_SMALL_KEYS_RESTRICTION
        elif small_key_mode == "Anywhere":
            pass

        # remove boss keys from the dungeon pool if boss key sanity is enabled
        if boss_key_mode == "Vanilla":
            self.placement |= VANILLA_BOSS_KEYS_PLACEMENT
        elif small_key_mode == "Own Dungeon":
            self.placement |= DUNGEON_BOSS_KEYS_RESTRICTION
        elif boss_key_mode == "Anywhere":
            pass

        # remove maps from the dungeon pool if maps are shuffled
        if map_mode == "Removed":
            pass  # Dealt with during item initialization
        elif map_mode == "Vanilla":
            self.placement |= VANILLA_MAPS_PLACEMENT
        elif map_mode == "Own Dungeon - Restricted":
            self.placement |= DUNGEON_MAPS_RESTRICTED_RESTRICTION
        elif map_mode == "Own Dungeon - Unrestricted":
            self.placement |= DUNGEON_MAPS_RESTRICTION
        elif map_mode == "Anywhere":
            pass

    #
    #
    # Retro-compatibility

    def retro_compatibility(self):
        self.done_item_locations = self.placement.locations
        self.prerandomization_item_locations = self.initial_placement.locations
        self.entrance_connections = {}  # Names were changed
        self.trial_connections = {}  # Names were changed
        self.macros = self.logic.requirements

    def get_sots_locations(self):
        return {}

    def get_barren_regions(self):
        return [], []

    def calculate_playthrough_progression_spheres(self):
        return []

    def split_location_name_by_zone(self, name):
        return name, name

    def all_progress_items(self):
        return self.logic.aggregate_required_items(
            self.logic.requirements, self.logic.inventory
        )

    def parse_logic_expression(self, exp):
        return LogicExpression.parse(exp)

    def filter_locations_for_progression(self, lst):
        return [loc for loc in lst if loc not in self.banned]

    def can_reach_restricted(self, banned_locations, test_location):
        return self.logic.restricted_test(
            (EXTENDED_ITEM[self.areas.short_to_full(loc)] for loc in banned_locations),
            EXTENDED_ITEM[self.areas.short_to_full(test_location)],
        )
