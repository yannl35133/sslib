# taken from https://github.com/LagoLunatic/wwrando/blob/master/logic/logic.py

# import yaml
# import re
from collections import defaultdict  # OrderedDict,

# import copy
# from pathlib import Path
from typing import Any, Optional, Dict, List, Tuple
from dataclasses import dataclass
from enum import Enum
from functools import reduce

# import os

# from .item_types import (
#     PROGRESS_ITEMS,
#     NONPROGRESS_ITEMS,
#     CONSUMABLE_ITEMS,
#     DUPLICABLE_ITEMS,
#     DUNGEON_PROGRESS_ITEMS,
#     MAPS,
#     SMALL_KEYS,
#     BOSS_KEYS,
# )
# from .constants import (
#     DUNGEON_NAME_TO_SHORT_DUNGEON_NAME,
#     DUNGEON_NAMES,
#     SHOP_CHECKS,
#     MAP_CHECKS,
#     SMALL_KEY_CHECKS,
#     BOSS_KEY_CHECKS,
#     POTENTIALLY_REQUIRED_DUNGEONS,
#     ALL_TYPES,
# )
# from .logic_expression import LogicExpression, parse_logic_expression, Inventory, item_with_count_re


from .logic_expression import LogicExpression, Inventory, RevInventory
from .inventory import (
    EXTENDED_ITEM as _EXTENDED_ITEM,
    INVENTORY_ITEMS as _INVENTORY_ITEMS,
)


class keydefaultdict(defaultdict):
    default_factory: Any

    def __missing__(self, key):
        if self.default_factory is None:
            raise KeyError(key)
        else:
            ret = self[key] = self.default_factory(key)
            return ret


AllowedTimeOfDay = Enum("AllowedTimeOfDay", ("DayOnly", "NightOnly", "Both"))

events: List[str] = []


@dataclass
class Area:
    name: str
    allowed_time_of_day: AllowedTimeOfDay = AllowedTimeOfDay.DayOnly
    can_sleep: bool = False
    can_save: bool = False
    sub_areas: "Dict[str, Area]" = {}
    locations: Dict[str, LogicExpression] = {}
    exits: Dict[str, LogicExpression] = {}

    @classmethod
    def of_dict(cls, args):
        return cls(**args)

    @classmethod
    def of_yaml(
        cls,
        name: str,
        raw_dict: Dict[str, Any],
        parent: Optional[Area] = None,
    ):
        area = cls(name)

        if (v := raw_dict.get("allowed-time-of-day")) is not None:
            area.allowed_time_of_day = AllowedTimeOfDay[v]
        if (b := raw_dict.get("can-sleep")) is not None:
            area.can_sleep = b
        if (b := raw_dict.get("can-save")) is not None:
            area.can_save = b

        if (d := raw_dict.get("locations")) is not None:
            area.locations = {k: LogicExpression.parse(v) for k, v in d.items()}
            for k in d:
                if k not in _INVENTORY_ITEMS:
                    events.append(name + "/" + k)

        if (d := raw_dict.get("exits")) is not None:
            area.exits = {k: LogicExpression.parse(v) for k, v in d.items()}

        if (v := raw_dict.get("entrance")) is not None:
            if parent is None:
                raise ValueError("An entrance was given but no parent to give it to")
            parent.exits[name] = LogicExpression.parse(v)

        area.sub_areas = {
            k: cls.of_yaml(name + "/" + k, v, area)
            for k, v in raw_dict.items()
            if "A" <= k[0] <= "Z"
        }
        return area

    def map(self, f):
        for d in [self.locations, self.exits]:
            for k, v in d.items():
                d[k] = f(self.name, v)
        for sub_area in self.sub_areas:
            sub_area.map(f)


class Areas:
    areas: Dict[str, Area]

    @staticmethod
    def subname(lst1, lst2, i=0, j=0):
        while True:
            if len(lst1) - i == 0 or len(lst2) - j == 0:
                return False
            if len(lst1) - i == 1 == len(lst2) - j:
                return lst1[i] == lst2[j]
            if lst1[i] == lst2[j]:
                i += 1
            j += 1

    def get_assoc_list(self, checks, gossip_stones, map_exits) -> List[str, str]:
        def get_pairs(area_name: str, element_names: Dict[str, Any], database):
            res = []
            area_list = area_name.split("/")
            for name in element_names:
                full_address = area_name + "/" + name
                full_address_list = area_list + [name]
                candidates = filter(
                    lambda name: self.subname(name.split(" - "), full_address_list),
                    database,
                )
                for winner in candidates:
                    res.append((winner, full_address))
                    break
                    # Takes the first one
                else:  # No first one to take
                    res.append((full_address, full_address))

            return res

        res = []
        locations_db = checks | gossip_stones
        for area in self.areas:
            res.extend(get_pairs(area.name, area.locations, locations_db))
            res.extend(get_pairs(area.name, area.exits, map_exits))

        return res

    def search_area(
        self, base_address: List[str], partial_address: List[str]
    ) -> Optional[List[str]]:
        def search_area(i, j, areas):
            if len(partial_address) - j == 0:  # We've arrived
                return []
            hd = partial_address[j]
            if hd in areas:  # Abandon the base address, we've branched off
                return [hd] + search_area(len(base_address), j + 1, areas[hd].sub_areas)

            if len(base_address) - i > 0:  # Let's follow the base address some more
                hd2 = base_address[i]
                return [hd2] + search_area(i + 1, j, areas[hd2].sub_areas)

            # Now we search everywhere
            for area in areas.values():
                if (res := search_area(i, j, area.sub_areas)) is not None:
                    return [area.name] + res
            else:
                return None

        return search_area(0, 0, self.areas)

    def update_exit_names(self, map_exits):
        def updated_names_generator(prefix, exits):
            for k, v in exits.items():
                if k in map_exits:
                    yield k, v
                else:
                    addr = self.search_area(prefix, k.split(" - "))
                    yield "/".join(addr), v

        for area in self.areas:
            area.exits = set(updated_names_generator(area.name.split("/"), area.exits))

    def __getitem__(self, addr):
        self.areas[addr]

    def __setitem__(self, addr, value: Area):
        self.areas[addr] = value

    def __init__(
        self,
        areas: Dict[str, Any],
        checks: Dict[str, Any],
        gossip_stones: Dict[str, Any],
        map_exits: Dict[str, Any],
    ):
        self.areas = {k: Area.of_yaml("", k, v) for k, v in areas.items()}
        _EXTENDED_ITEM.items_list.extend(events)

        def flatten(areas):
            for area in areas:
                self.areas[area.name] = area
                flatten(area.sub_areas)

        for area in self.areas:
            flatten(area.sub_areas)

        def localizer(base_prefix: List[str], text):
            dest_prefix, dest = text.rsplit(" - ", 1)
            res = self.search_area(base_prefix.split("/"), dest_prefix.split(" - "))
            if res is None:
                return None
            return res, dest

        for area in self.areas:
            area.map(lambda prefix, v: v.localize(lambda t: localizer(prefix, t)))

        self.short_full = self.get_assoc_list(checks, gossip_stones, map_exits)

        def assoc(lst, elt, reverse=False):
            if reverse:
                for (a, b) in lst:
                    if b == elt:
                        return a
            else:
                for (a, b) in lst:
                    if a == elt:
                        return b
            raise ValueError("Error: association list")

        self.short_to_full = lambda x: assoc(self.short_full, x)
        self.full_to_short = lambda x: assoc(self.short_full, x, True)


@dataclass
class Placement:
    checks: Dict[str, str]
    map_transitions: Dict[str, str]

    hints: Dict[str, "Hint"]

    item_placement_limit: Dict[str, str]  # item, area where it must be placed

    def copy(self):
        return Placement(
            self.checks.copy(),
            self.map_transitions.copy(),
            self.hints.copy(),
            self.item_placement_limit.copy(),
        )


class World:
    areas: Areas

    placement: Placement

    accessible_areas: Dict[str, (bool, bool)]  # At day / at night
    inventory: Inventory

    unfilled_checks: List[str]
    unmapped_transitions: List[str]

    def __init__(
        self,
        areas: Areas,
        placement=None,
        inv_default=False,
        acc_areas_default=False,
    ):
        self.areas = areas
        self.short_to_full = areas.short_to_full

        self.placement = placement.copy()

        # def init_accessible_areas(area_short):
        #     area_long = self.short_to_full(area_short)
        #     area = self.areas[area_long]
        #     if area.allowed_time_of_day == AllowedTimeOfDay.Both:
        #         return acc_areas_default, acc_areas_default
        #     elif area.allowed_time_of_day == AllowedTimeOfDay.DayOnly:
        #         return acc_areas_default, False
        #     else:
        #         return False, acc_areas_default

        self.accessible_areas = defaultdict(lambda: False, False)
        self.inventory = Inventory()  # if not inv_default else RevInventory()

    # def recompute_plus(self):
    #     for area, (acc0, acc1) in accessible_areas:
    #         if acc0 or acc1:
    #             for

    # def give_item(self, item):
    #     self.inventory |= item
    #     for area, (acc0, acc1) in accessible_areas:
    #         if (not acc0) or (not acc1):
