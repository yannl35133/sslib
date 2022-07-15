from __future__ import annotations
from dataclasses import dataclass
from functools import cache
import random
from typing import List  # Only for typing purposes

from options import Options, OPTIONS
from .backwards_filled_algorithm import BFA, RandomizationSettings, timeit
from .logic import Logic, Placement, LogicSettings
from .logic_input import Areas
from .logic_expression import DNFInventory, InventoryAtom
from .inventory import Inventory, EXTENDED_ITEM
from .constants import *
from .placements import *
from .pools import *


@dataclass
class AdditionalInfo:
    required_dungeons: List[str]
    unrequired_dungeons: List[str]
    randomized_dungeon_entrance: dict[str, str]
    randomized_trial_entrance: dict[str, str]
    initial_placement: Placement


class LogicUtils:
    def __init__(
        self,
        areas: Areas,
        logic: Logic,
        additional_info: AdditionalInfo,
        runtime_requirements,
    ):

        self._logic = logic
        self.areas = areas
        self.short_to_full = logic.short_to_full
        self.full_to_short = logic.full_to_short
        self.placement = logic.placement
        self.required_dungeons = additional_info.required_dungeons
        self.unrequired_dungeons = additional_info.unrequired_dungeons
        self.starting_inventory = Inventory(
            {EXTENDED_ITEM[item] for item in self.placement.starting_items}
        )
        self.randomized_dungeon_entrance = additional_info.randomized_dungeon_entrance
        self.randomized_trial_entrance = additional_info.randomized_trial_entrance
        self.initial_placement = additional_info.initial_placement
        self.runtime_requirements = runtime_requirements

    @cache
    def requirements(self):
        assert len(self.placement.locations) == len(self.areas.checks)
        requirements = self.areas.requirements
        for loc, req in self.runtime_requirements.items():
            requirements[EXTENDED_ITEM[loc]] |= req

        for exit, entrance in self.placement.map_transitions.items():
            self._logic._link_connection(exit, entrance, requirements=requirements)

        for k, v in self.placement.locations.items():
            self._logic._place_item(k, v, requirements)

        for k in self.starting_inventory:
            requirements[k] = DNFInventory(True)

        return requirements

    @cache
    def _fill_for_test(self, banned_intset, inventory):
        custom_requirements = self.requirements().copy()
        for index, e in enumerate(reversed(bin(banned_intset))):
            if e == "1":
                custom_requirements[index] = DNFInventory(False)

        return Logic._fill_inventory(custom_requirements, inventory)

    def fill_restricted(
        self,
        banned_indices: List[EXTENDED_ITEM] = [],
        starting_inventory: None | Inventory = None,
    ):
        if starting_inventory is None:
            starting_inventory = self.starting_inventory

        banned_intset = 0
        for i in banned_indices:
            banned_intset += 1 << i

        return self._fill_for_test(banned_intset, starting_inventory)

    def restricted_test(
        self,
        test_index,
        banned_indices: List[EXTENDED_ITEM] = [],
        starting_inventory: None | Inventory = None,
    ):
        if starting_inventory is None:
            starting_inventory = self.starting_inventory

        banned_intset = 0
        for i in banned_indices:
            banned_intset += 1 << i

        restricted_full = self._fill_for_test(banned_intset, starting_inventory)

        return restricted_full[test_index]

    def aggregate_requirements(self, item):
        if not hasattr(self, "aggregated_reqs"):
            self._isvisited_agg = set()
            self.aggregated_reqs: List[None | bool | Inventory] = [
                None for _ in self.requirements()
            ]

        if item in self._isvisited_agg:
            return False

        if self.aggregated_reqs[item] is not None:
            return self.aggregated_reqs[item]

        self._isvisited_agg.add(item)
        aggregate = False
        for (possibility, (_, conj_pre)) in self._logic.requirements[
            item
        ].disjunction.items():
            aggregate_ = Inventory(conj_pre)
            for req_item in possibility:
                ag = timeit(
                    f"Aggr reqs {req_item}",
                    lambda: self.aggregate_requirements(req_item),
                )
                if ag is False:
                    break
                aggregate_ |= ag
            else:
                if aggregate is False:
                    aggregate = aggregate_
                else:
                    aggregate &= aggregate_

        self._isvisited_agg.remove(item)
        if not self._isvisited_agg:
            self.aggregated_reqs[item] = aggregate

        return aggregate

    @cache
    def get_sots_items(self, loc=DEMISE):
        index = EXTENDED_ITEM[self.short_to_full(loc)]
        usefuls = self.get_useful_items()
        return [
            item
            for item in PROGRESS_ITEMS
            if item in usefuls
            and not self.restricted_test(index, [EXTENDED_ITEM[item]])
        ]

        # requireds: Inventory = self.aggregate_requirements(index)  # type: ignore
        # return [
        # self.full_to_short(EXTENDED_ITEM[i])
        # for i in requireds.intset
        # if EXTENDED_ITEM[i] in self.checks
        # ]

    def aggregate_useful_items(self, item):
        if hasattr(self, "aggregated_usefuls"):
            return self.aggregated_usefuls[item]

        self.aggregated_usefuls: Dict[EXTENDED_ITEM, Inventory] = {
            item: self.requirements()[item].disj_pre for item in EXTENDED_ITEM
        }

        just_added = {k: v.intset for k, v in self.aggregated_usefuls.items()}

        keep_going = True
        while keep_going:
            keep_going = False
            for i in EXTENDED_ITEM:
                new_just_added = set()
                for item in just_added[i]:
                    new_just_added |= (
                        self.aggregated_usefuls[item].intset
                        - self.aggregated_usefuls[i].intset
                    )
                    self.aggregated_usefuls[i] |= self.aggregated_usefuls[item]
                just_added[i] = new_just_added
                keep_going = keep_going or bool(new_just_added)

        return self.aggregated_usefuls[item]

    def aggregate_useful_items_one(self, item):
        if hasattr(self, "aggregated_usefuls") and item in self.aggregated_usefuls:
            return self.aggregated_usefuls[item]
        if not hasattr(self, "aggregated_usefuls"):
            self.aggregated_usefuls: Dict[EXTENDED_ITEM, Inventory] = {}

        aggregate = self.requirements()[item].disj_pre

        just_added = aggregate.intset

        keep_going = True
        while keep_going:
            keep_going = False
            new_just_added = set()
            for item2 in just_added:
                req = self.requirements()[item2].disj_pre
                new_just_added |= req.intset - aggregate.intset
                aggregate |= req
            just_added = new_just_added
            keep_going = keep_going or bool(new_just_added)
        self.aggregated_usefuls[item] = aggregate

        return self.aggregated_usefuls[item]

    def get_useful_items(self, loc=DEMISE):
        index = EXTENDED_ITEM[self.short_to_full(loc)]
        usefuls: Inventory = self.aggregate_useful_items_one(index)
        return [
            loc
            for i in usefuls.intset
            if (loc := EXTENDED_ITEM.get_item_name(i)) in PROGRESS_ITEMS
        ]

    def locations_by_hint_region(self, region):
        for n, c in self.areas.checks.items():
            if c["hint_region"] == region:
                yield n

    @cache
    def get_barren_regions(self, loc=DEMISE):
        useful_checks = [
            self.placement.items[item]
            for item in self.get_useful_items(loc)
            if item not in self.placement.starting_items
        ]
        non_banned = self.fill_restricted()

        useless_regions = ALL_HINT_REGIONS.copy()
        for c in useful_checks:
            useless_regions.pop(self.areas.checks[c]["hint_region"], None)

        inaccessible_regions = ALL_HINT_REGIONS.copy()
        for c in self.areas.checks.values():
            if non_banned[c["req_index"]]:
                inaccessible_regions.pop(c["hint_region"], None)

        return [
            reg for reg in useless_regions if reg not in inaccessible_regions
        ], list(inaccessible_regions)

    def calculate_playthrough_progression_spheres(self):
        spheres = []
        keep_going = True
        inventory = self.starting_inventory
        requirements = self.requirements()
        # usefuls = self.aggregate_useful_items(EXTENDED_ITEM[self.short_to_full(DEMISE)])
        while keep_going:
            sphere = []
            keep_going = False
            for i in EXTENDED_ITEM.items():
                if not inventory[i] and requirements[i].eval(inventory):
                    inventory |= i
                    keep_going = True
                    if (loc := EXTENDED_ITEM.get_item_name(i)) in self.areas.checks:
                        # i in usefuls:
                        sphere.append(loc)
                    elif i == EXTENDED_ITEM[self.short_to_full(DEMISE)]:
                        sphere.append("Past - Demise")
            if sphere:
                spheres.append(sphere)
        return spheres


class Rando:
    def __init__(self, areas: Areas, options: Options, rng: random.Random):

        self.options = options
        self.rng = rng

        self.areas = areas
        self.short_to_full = areas.short_to_full
        self.norm = self.short_to_full

        placement = self.options.get("placement")
        self.placement: Placement = placement if placement is not None else Placement()
        self.parse_options()
        self.initial_placement = self.placement.copy()

        starting_inventory_BFA = Inventory(
            {
                item
                for item in EXTENDED_ITEM.items()
                if (item_name := EXTENDED_ITEM.get_item_name(item)) in INVENTORY_ITEMS
                and (
                    item_name not in self.placement.items
                    or item_name in self.placement.starting_items
                )
            }
        )

        runtime_requirements = (
            self.logic_options_requirements
            | self.endgame_requirements
            | self.ban_options
        )

        logic_settings = LogicSettings(
            starting_inventory_BFA,
            runtime_requirements,
            self.banned,
        )
        additional_info = AdditionalInfo(
            self.required_dungeons,
            self.unrequired_dungeons,
            self.randomized_dungeon_entrance,
            self.randomized_trial_entrance,
            self.placement.copy(),
        )

        logic = Logic(areas, logic_settings, self.placement)
        self.logic = LogicUtils(areas, logic, additional_info, runtime_requirements)

        if self.options["logic-mode"] == "No Logic":
            for i in range(len(logic.requirements)):
                logic.requirements[i] = DNFInventory(True)

        self.rando_algo = BFA(logic, self.rng, self.randosettings)

    def randomize(self):
        self.rando_algo.randomize()
        logic = self.logic._logic

        # Check
        logic.inventory = Inventory(
            {EXTENDED_ITEM[item] for item in self.placement.starting_items}
        )
        logic.fill_inventory()
        DEMISE_BIT = EXTENDED_ITEM[self.short_to_full(DEMISE)]
        if not logic.full_inventory[DEMISE_BIT]:
            print("Could not reach Demise")
            print(f"It would require {logic.backup_requirements[DEMISE_BIT]}")
            exit(1)

        logic.add_item(EXTENDED_ITEM.banned_bit())
        all_checks = Inventory(
            {check["req_index"] for check in self.areas.checks.values()}
        )

        if not all_checks <= logic.full_inventory:
            print("Everything is not accessible")
            print(all_checks.intset - logic.full_inventory.intset)
            i = next(iter(all_checks.intset - logic.full_inventory.intset))
            print(f"For example, {i} would require {logic.backup_requirements[i]}")
            exit(1)

    def parse_options(self):
        # Initialize location related attributes.
        self.randomize_required_dungeons()  # self.required_dungeons, self.unrequired_dungeons
        self.randomize_starting_items()  # self.placement.starting_items
        self.ban_the_banned()  # self.banned, self.ban_options

        for item in self.placement.starting_items:
            self.placement.items[item] = EIN("Start Item")

        self.get_endgame_requirements()  # self.endgame_requirements

        self.initialize_items()  # self.randosettings

        self.set_placement_options()  # self.logic_options_requirements

        self.randomize_dungeons_trials()

        for item in self.placement.items:
            self.randosettings.must_be_placed_items.pop(item, None)

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
        starting_items = {
            number(PROGRESSIVE_SWORD, i)
            for i in range(SWORD_COUNT[self.options["starting-sword"]])
        }

        for tablet in self.rng.sample(TABLETS, k=self.options["starting-tablet-count"]):
            starting_items.add(tablet)

        # if self.options.get('start-with-sailcloth', True):
        #   starting_items.add('Sailcloth')
        if self.options["start-with-pouch"]:
            starting_items.add(number(PROGRESSIVE_POUCH, 0))

        self.placement.starting_items |= starting_items

    def ban_the_banned(self):

        banned_req = DNFInventory(EXTENDED_ITEM.banned_bit())
        nothing_req = DNFInventory(True)
        maybe_req = lambda b: banned_req if b else nothing_req
        self.ban_options = {
            BEEDLE_STALL_ACCESS: maybe_req(self.options["shop-mode"] == "Always Junk"),
            MEDIUM_PURCHASES: maybe_req("medium" in self.options["banned-types"]),
            EXPENSIVE_PURCHASES: maybe_req("expensive" in self.options["banned-types"]),
        } | {
            MAY_GET_n_CRYSTALS(c): (maybe_req(c > self.options["max-batreaux-reward"]))
            for c in CRYSTAL_THRESHOLDS
        }

        self.banned: List[EIN] = []

        if self.options["empty-unrequired-dungeons"]:
            self.banned.extend(
                self.norm(entrance_of_exit(DUNGEON_MAIN_EXITS[dungeon]))
                for dungeon in self.unrequired_dungeons
            )

            if self.options["skip-skykeep"]:
                self.banned.append(self.norm(entrance_of_exit(DUNGEON_MAIN_EXITS[SK])))

        banned_types = set(self.options["banned-types"]) - {"medium", "expensive"}
        for loc in self.areas.checks:
            check_types = set(
                s.strip() for s in self.areas.checks[loc]["type"].split(",")
            )
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

        may_be_placed_items: List[EIN] = list(CONSUMABLE_ITEMS)
        duplicable_items = DUPLICABLE_ITEMS

        rupoor_mode = self.options["rupoor-mode"]
        if rupoor_mode != "Off":
            duplicable_items = DUPLICABLE_COUNTERPROGRESS_ITEMS  # Rupoors
            if rupoor_mode == "Added":
                may_be_placed_items += [EIN(RUPOOR)] * 15
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
        for exit, v in self.areas.map_exits.items():
            if v["type"] == "entrance" or v.get("disabled", False):
                continue
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
            EIN(trick(trick_name)): DNFInventory(trick_name in enabled_tricks)
            for trick_name in OPTIONS["enabled-tricks-bitless"]["choices"]
        }

        if shop_mode == "Vanilla":
            self.placement |= VANILLA_BEEDLE_PLACEMENT(self.norm)
        elif shop_mode == "Randomized":
            pass
        elif shop_mode == "Always Junk":
            pass

        small_key_mode = self.options["small-key-mode"]
        boss_key_mode = self.options["boss-key-mode"]
        map_mode = self.options["map-mode"]
        # remove small keys from the dungeon pool if small key sanity is enabled
        if small_key_mode == "Vanilla":
            self.placement |= VANILLA_SMALL_KEYS_PLACEMENT(self.norm)
        elif small_key_mode == "Own Dungeon - Restricted":
            self.placement |= DUNGEON_SMALL_KEYS_RESTRICTION(self.norm)
            self.placement |= CAVES_KEY_RESTRICTION(self.norm)
        elif small_key_mode == "Lanayru Caves Key Only":
            self.placement |= DUNGEON_SMALL_KEYS_RESTRICTION(self.norm)
        elif small_key_mode == "Anywhere":
            pass

        # remove boss keys from the dungeon pool if boss key sanity is enabled
        if boss_key_mode == "Vanilla":
            self.placement |= VANILLA_BOSS_KEYS_PLACEMENT(self.norm)
        elif boss_key_mode == "Own Dungeon":
            self.placement |= DUNGEON_BOSS_KEYS_RESTRICTION(self.norm)
        elif boss_key_mode == "Anywhere":
            pass

        # remove maps from the dungeon pool if maps are shuffled
        if map_mode == "Removed":
            pass  # Dealt with during item initialization
        elif map_mode == "Vanilla":
            self.placement |= VANILLA_MAPS_PLACEMENT(self.norm)
        elif map_mode == "Own Dungeon - Restricted":
            self.placement |= DUNGEON_MAPS_RESTRICTED_RESTRICTION(self.norm)
        elif map_mode == "Own Dungeon - Unrestricted":
            self.placement |= DUNGEON_MAPS_RESTRICTION(self.norm)
        elif map_mode == "Anywhere":
            pass

    #
    #
    # Retro-compatibility

    def reassign_entrances(
        self, exs1: list[EIN] | list[list[EIN]], exs2: list[EIN] | list[list[EIN]]
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

        self.reassign_entrances(dungeon_entrances, dungeons)

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
        self.reassign_entrances(trial_entrances, trials)
