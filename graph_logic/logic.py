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
from .logic_expression import LogicExpression


AllowedTimeOfDay = Enum("AllowedTimeOfDay", "DayOnly", "NightOnly", "Both")

forgotten_entrances: List[Tuple[List[str], Dict[str, LogicExpression]]] = []


@dataclass
class Area:
    name: str
    allowed_time_of_day: AllowedTimeOfDay = AllowedTimeOfDay.DayOnly
    can_sleep: bool = False
    can_save: bool = False
    sub_areas: "Dict[str, Area]" = {}
    locations: Dict[str, LogicExpression] = {}
    logical_exits: Dict[str, LogicExpression] = {}
    map_exits: Dict[str, LogicExpression] = {}

    @classmethod
    def of_dict(cls, args):
        return cls(**args)

    @classmethod
    def of_yaml(cls, prefix: List[str], name: str, raw_dict: Dict[str, Any]):
        area = cls(name)
        if (v := raw_dict.get("allowed-time-of-day")) is not None:
            area.allowed_time_of_day = AllowedTimeOfDay[v]
        if (b := raw_dict.get("can-sleep")) is not None:
            area.can_sleep = b
        if (b := raw_dict.get("can-save")) is not None:
            area.can_save = b
        if (d := raw_dict.get("locations")) is not None:
            area.locations = {k: LogicExpression.parse(v) for k, v in d.items()}
        if (d := raw_dict.get("logical-exits")) is not None:
            area.logical_exits = {k: LogicExpression.parse(v) for k, v in d.items()}
        if (d := raw_dict.get("map-exits")) is not None:
            area.map_exits = {k: LogicExpression.parse(v) for k, v in d.items()}
        if (d := raw_dict.get("logical-entrances")) is not None:
            forgotten_entrances.append(
                (prefix + [name], {k: LogicExpression.parse(v) for k, v in d.items()})
            )

        area.sub_areas = {
            k: cls.of_yaml(prefix + [name], k, v)
            for k, v in raw_dict.items()
            if "A" <= k[0] <= "Z"
        }
        return area

    def map(self, f, prefix):
        prefix = prefix + [self.name]
        for d in [self.locations, self.logical_exits, self.map_exits]:
            for k, v in d.items():
                d[k] = f(prefix, v)
        for sub_area in self.sub_areas:
            sub_area.map(f, prefix)


class Areas:
    areas: Dict[str, Area]

    checks: Dict[str, Any]
    gossip_stones: Dict[str, Any]
    map_exits: Dict[str, Any]

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

    def get_assoc_list(self) -> List[str, List[str]]:
        def get_pairs(database, full_addresses):
            res = []
            for addr in full_addresses:
                candidates = filter(
                    lambda name: self.subname(name.split(" - "), addr), database
                )
                try:
                    res.append(next(candidates), addr)  # Takes the first one
                except StopIteration:  # No first one to take
                    res.append("/".join(addr), addr)

            return res

        def get_assoc_list(prefix: List[str], area: Area):
            prefix = prefix + [area.name]
            return (
                get_pairs(self.checks | self.gossip_stones, area.locations)
                + get_pairs(self.map_exits, area.map_exits)
                + reduce(
                    list.append,
                    (get_assoc_list(prefix, sub_area) for sub_area in area.sub_areas),
                    [],
                )
            )

        return reduce(
            list.append,
            (get_assoc_list([], area) for area in self.areas),
            [],
        )

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

    def update_area_names(self):
        def update_area_names(prefix, area):
            prefix = prefix + [area.name]
            area.logical_exits = {
                "/".join(self.search_area(prefix, k.split(" - "))): v
                for k, v in area.logical_exits.items()
            }
            for sub_area in area.sub_areas.values():
                update_area_names(prefix, sub_area)

        for area in self.areas:
            update_area_names([], area)

    def __getitem__(self, addr: List[str]):
        a = self.areas
        for step in addr[:-1]:
            a = a[step].sub_areas
        return a[addr[-1]]

    def __setitem__(self, addr: List[str], value: Area):
        a = self.areas
        for step in addr[:-1]:
            a = a[step].sub_areas
        a[addr[-1]] = value

    def add_forgotten_entrances(self):
        for base, dict in forgotten_entrances:
            for partial_dst, exp in dict.items():
                dst = self.search_area(base, partial_dst)
                self[dst].logical_exits["/".join(base)] = exp

    def __init__(
        self,
        areas: Dict[str, Any],
        checks: Dict[str, Any],
        gossip_stones: Dict[str, Any],
        map_exits: Dict[str, Any],
        macros: Dict[str, Any],
    ):
        self.areas = {k: Area.of_yaml([], k, v) for k, v in areas.items()}
        self.checks = checks
        self.gossip_stones = gossip_stones
        self.map_exits = map_exits

        def localizer(base_prefix, text):
            dest_prefix, dest = text.rsplit(" - ", 1)
            dest_prefix = dest_prefix.split(" - ")
            res = self.search_area(base_prefix, dest_prefix)
            if res is None:
                return None
            return res, dest

        for k, v in macros.items():
            macros[k] = (
                LogicExpression.parse(v)
                .localize(lambda t: localizer([], t))
                .inline(macros)
            )

        for area in self.areas:
            area.map(
                lambda prefix, v: v.localize(lambda t: localizer(prefix, t)).inline(
                    macros
                )
            )

        self.short_to_full = self.get_assoc_list()


class World:
    areas: Dict[str, Area]

    accessible_areas: Dict[str, bool]
