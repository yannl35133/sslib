from __future__ import annotations
import random
from typing import List  # Only for typing purposes

from options import Options, OPTIONS
from .backwards_filled_algorithm import BFA, RandomizationSettings
from .logic import Logic, Placement, LogicSettings, AdditionalInfo
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
        self.norm = lambda s: self.areas.full_to_short(self.areas.short_to_full(s))

        placement = self.options.get("placement")
        self.placement: Placement = placement if placement is not None else Placement()
        self.parse_options()
        self.initial_placement = self.placement.copy()

        starting_inventory_BFA = Inventory(
            {
                item
                for item in EXTENDED_ITEM.items()
                if EXTENDED_ITEM.get_item_name(item) in INVENTORY_ITEMS
                and EXTENDED_ITEM.get_item_name(item) not in self.placement.items
            }
        )
        starting_area = self.short_to_full(START)
        exit_pools = []
        # DUNGEON_ENTRANCES_COMPLETE_POOLS + SILENT_REALMNS_COMPLETE_POOLS

        banned_bit_inv = DNFInventory(EXTENDED_ITEM.banned_bit())

        additional_requirements = (
            self.logic_options_requirements
            | self.endgame_requirements
            | {loc: banned_bit_inv for loc in self.banned}
        )

        logic_settings = LogicSettings(
            exit_pools, starting_inventory_BFA, starting_area, additional_requirements
        )
        additional_info = AdditionalInfo(
            self.required_dungeons,
            self.unrequired_dungeons,
            self.starting_items,
            self.randomized_dungeon_entrance,
            self.randomized_trial_entrance,
        )

        self.logic = Logic(self.areas, logic_settings, additional_info, self.placement)

        if self.options["logic-mode"] == "No Logic":
            for i in range(len(self.logic.requirements)):
                self.logic.requirements[i] = DNFInventory(True)

        self.rando_algo = BFA(self.logic, self.rng, self.randosettings)

        self.retro_compatibility()

    def randomize(self):
        self.rando_algo.randomize()

        # Check
        self.logic.inventory = self.logic.starting_items.add(
            EXTENDED_ITEM[self.short_to_full(START)]
        )
        self.logic.fill_inventory()
        all_checks = Inventory(
            {check["req_index"] for check in self.areas.checks.values()}
            | {EXTENDED_ITEM[self.short_to_full("Beat Demise")]}
        )

        if not all_checks <= self.logic.full_inventory:
            print("Everything is not accessible")
            print(all_checks.intset - self.logic.full_inventory.intset)
            i = next(iter(all_checks.intset - self.logic.full_inventory.intset))
            print(f"For example, {i} would require {self.logic.backup_requirements[i]}")
            exit(1)

    def parse_options(self):
        # Initialize location related attributes.
        self.randomize_required_dungeons()  # self.required_dungeons, self.unrequired_dungeons
        self.randomize_starting_items()  # self.starting_items
        self.ban_the_banned()  # self.banned

        self.get_endgame_requirements()  # self.endgame_requirements

        self.initialize_items()  # self.randosettings

        self.set_placement_options()  # self.logic_options_requirements

        self.randomize_dungeons_trials()

        for item in self.starting_items.intset:
            item_name = EXTENDED_ITEM.get_item_name(item)
            self.randosettings.must_be_placed_items.pop(item_name, None)
        for item_name in self.placement.items:
            self.randosettings.must_be_placed_items.pop(item_name, None)

    def randomize_required_dungeons(self):
        """
        Selects the required dungeons randomly based on options
        """
        indices = list(range(len(REGULAR_DUNGEONS)))
        self.rng.shuffle(indices)
        nb_dungeons = self.options["required-dungeon-count"]
        req_indices = indices[:nb_dungeons]
        unreq_indices = indices[nb_dungeons:]
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
        self.banned: List[str] = []

        if self.options["shop-mode"] == "Always Junk":
            self.banned.append(BEEDLE_STALL)

        if self.options["empty-unrequired-dungeons"]:
            self.banned.extend(
                entrance_of_exit(DUNGEON_MAIN_EXITS[dungeon])
                for dungeon in self.unrequired_dungeons
            )

            if self.options["skip-skykeep"]:
                self.banned.append(entrance_of_exit(DUNGEON_MAIN_EXITS[SK]))

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

        options = {
            OPEN_THUNDERHEAD_OPTION: self.options["open-thunderhead"] == "Open",
            OPEN_LMF_OPTION: self.options["open-lmf"] == "Open",
            RANDOMIZED_BEEDLE_OPTION: shop_mode != "Vanilla",
            HERO_MODE: self.options["fix-bit-crashes"],
            NO_BIT_CRASHES: self.options["hero-mode"],
        }

        self.placement |= SINGLE_CRYSTAL_PLACEMENT(self.norm)

        vanilla_map_transitions = {}
        vanilla_reverse_map_transitions = {}
        for exit, v in map_exits.items():
            if v["type"] == "entrance" or v.get("disabled", False):
                continue
            exit = self.norm(exit)
            entrance = self.norm(v["vanilla"])
            vanilla_map_transitions[exit] = entrance
            vanilla_reverse_map_transitions[entrance] = exit

        self.placement |= Placement(
            map_transitions=vanilla_map_transitions,
            reverse_map_transitions=vanilla_reverse_map_transitions,
        )

        if self.options["sword-dungeon-reward"]:
            swords_to_place = {
                sword
                for sword in PROGRESSIVE_SWORDS
                if sword not in self.placement.items
                and sword not in self.starting_items.intset
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

        self.logic_options_requirements = {
            k: DNFInventory(b) for k, b in options.items()
        } | {
            trick(trick_name): DNFInventory(trick_name in enabled_tricks)
            for trick_name in OPTIONS["enabled-tricks-bitless"]["choices"]
        }

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
        elif boss_key_mode == "Own Dungeon":
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

    def reassign_entrances(
        self, exs1: list[EIN | list[EIN]], exs2: list[EIN | list[EIN]]
    ):
        for ex1, ex2 in zip(exs1, exs2):
            if isinstance(ex1, str):
                ex1 = [ex1]
            if isinstance(ex2, str):
                ex2 = [ex2]
            assert ex1[0] in self.placement.map_transitions
            assert ex2[0] in self.placement.map_transitions
            en1 = EIN(entrance_of_exit(ex1[0]))
            en2 = EIN(entrance_of_exit(ex2[0]))
            for exx1 in ex1:
                self.placement.map_transitions[exx1] = en2
            for exx2 in ex2:
                self.placement.map_transitions[exx2] = en1
            self.placement.reverse_map_transitions[en1] = ex2[0]
            self.placement.reverse_map_transitions[en2] = ex1[0]

    def randomize_dungeons_trials(self):
        # Do this in a deliberately hacky way, this is not supposed to be how ER works
        der = self.options["randomize-entrances"]
        if der == "Dungeons":
            pool = REGULAR_DUNGEONS.copy()
            self.rng.shuffle(pool)
            pool.append(SK)
        elif der == "Dungeons + Sky Keep":
            pool = ALL_DUNGEONS.copy()
            self.rng.shuffle(pool)
        else:
            assert der == "None"
            pool = ALL_DUNGEONS

        self.randomized_dungeon_entrance = {}
        for i, e in enumerate(pool):
            self.randomized_dungeon_entrance[ALL_DUNGEONS[i]] = e

        dungeon_entrances = [
            [self.norm(e) for e in DUNGEON_OVERWORLD_EXITS[k]] for k in ALL_DUNGEONS
        ]
        dungeons = [
            self.norm(DUNGEON_MAIN_EXITS[self.randomized_dungeon_entrance[k]])
            for k in ALL_DUNGEONS
        ]

        self.reassign_entrances(dungeon_entrances, dungeons)  # type: ignore

        ter = self.options["randomize-trials"]
        pool = ALL_TRIALS.copy()
        if ter:
            self.rng.shuffle(pool)

        self.randomized_trial_entrance = {}
        for i, e in enumerate(pool):
            self.randomized_trial_entrance[ALL_TRIALS[i]] = e

        trial_entrances = [self.norm(TRIAL_EXITS[k]) for k in ALL_TRIALS]
        trials = [
            self.norm(TRIALS[self.randomized_trial_entrance[k]]) for k in ALL_TRIALS
        ]
        self.reassign_entrances(trial_entrances, trials)  # type: ignore

    def retro_compatibility(self):
        self.done_item_locations = self.logic.placement.locations
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
