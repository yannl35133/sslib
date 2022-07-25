from __future__ import annotations
from functools import cache
from typing import Any, Dict, Iterable, List, Set, Tuple
from collections import defaultdict
from dataclasses import dataclass, field

from .constants import *
from .logic_input import Area, Areas, DayOnly, NightOnly, Both
from .logic_expression import DNFInventory, AndCombination
from .inventory import Inventory, EXTENDED_ITEM


@dataclass
class PoolEntrance:
    entrance: EXTENDED_ITEM_NAME
    constraints: List[EXTENDED_ITEM_NAME] = field(default_factory=list)


@dataclass
class PoolExit:
    exit: EXTENDED_ITEM_NAME
    constraints: List[EXTENDED_ITEM_NAME] = field(default_factory=list)


@dataclass
class Placement:
    item_placement_limit: Dict[EXTENDED_ITEM_NAME, EXTENDED_ITEM_NAME] = field(
        default_factory=lambda: defaultdict(lambda: EIN(str()))
    )

    map_transitions: Dict[EIN, EIN] = field(default_factory=dict)
    reverse_map_transitions: Dict[EIN, EIN] = field(default_factory=dict)

    locations: Dict[EIN, EIN] = field(default_factory=dict)
    items: Dict[EXTENDED_ITEM_NAME, EXTENDED_ITEM_NAME] = field(default_factory=dict)
    hints: Dict[EXTENDED_ITEM_NAME, Any] = field(default_factory=dict)
    starting_items: Set[EIN] = field(default_factory=set)

    def copy(self):
        return Placement(
            self.item_placement_limit.copy(),
            self.map_transitions.copy(),
            self.reverse_map_transitions.copy(),
            self.locations.copy(),
            self.items.copy(),
            self.hints.copy(),
            self.starting_items.copy(),
        )

    def __or__(self, other: Placement) -> Placement:
        if not isinstance(other, Placement):
            raise ValueError
        for k, v in other.item_placement_limit.items():
            if k in self.item_placement_limit and v != self.item_placement_limit[k]:
                raise ValueError
        for k, v in other.map_transitions.items():
            if k in self.map_transitions and v != self.map_transitions[k]:
                raise ValueError
        for k, v in other.reverse_map_transitions.items():
            if (
                k in self.reverse_map_transitions
                and v != self.reverse_map_transitions[k]
            ):
                raise ValueError
        for k, v in other.locations.items():
            if k in self.locations and v != self.locations[k]:
                raise ValueError
        for k, v in other.items.items():
            if k in self.items and v != self.items[k]:
                raise ValueError
        for k, v in other.hints.items():
            if k in self.hints and v != self.hints[k]:
                raise ValueError
        return Placement(
            self.item_placement_limit | other.item_placement_limit,
            self.map_transitions | other.map_transitions,
            self.reverse_map_transitions | other.reverse_map_transitions,
            self.locations | other.locations,
            self.items | other.items,
            self.hints | other.hints,
            self.starting_items | other.starting_items,
        )


@dataclass
class LogicSettings:
    starting_inventory: Inventory
    runtime_requirements: Dict[EIN, DNFInventory]
    banned: List[EIN]


class Logic:
    def __init__(
        self,
        areas: Areas,
        logic_settings: LogicSettings,
        placement: Placement | None = None,
    ):
        self.areas = areas
        self.short_to_full = areas.short_to_full
        self.full_to_short = areas.full_to_short

        self.requirements = areas.requirements.copy()
        self.opaque = areas.opaque.copy()
        self.entrance_allowed_time_of_day = areas.entrance_allowed_time_of_day
        self.exit_to_area = areas.exit_to_area
        self.placement = placement.copy() if placement is not None else Placement()

        self.banned = {EXTENDED_ITEM[loc] for loc in logic_settings.banned}
        banned_bit_inv = DNFInventory(EXTENDED_ITEM.banned_bit())
        pure_usefuls = self.aggregate_all_useful_items(areas.requirements)

        self.ban_if = lambda it, r: r & banned_bit_inv if it in self.banned else r

        self.inventory = logic_settings.starting_inventory

        self.backup_requirements = self.requirements.copy()

        for exit, entrance in self.placement.map_transitions.items():
            self._link_connection(exit, entrance)

        self.full_inventory = self.inventory
        for k, v in self.placement.locations.items():
            self._place_item(k, v)

        for loc, req in logic_settings.runtime_requirements.items():
            it = EXTENDED_ITEM[loc]
            assert self.opaque[it]
            self.requirements[it] |= req
            self.opaque[it] = False

        for it in self.banned:
            if self.areas.requirements[it].is_impossible() or it not in pure_usefuls:
                self.requirements[it] &= banned_bit_inv
            else:
                raise ValueError(
                    f"Cannot ban potentially inlined away requirement {it}"
                )

        self.shallow_simplify()
        self.backup_requirements = self.requirements.copy()
        self.aggregate = self.aggregate_required_items(
            self.requirements, self.full_inventory.add(EXTENDED_ITEM.banned_bit())
        )

    def add_item(self, item: EXTENDED_ITEM | str):
        self.inventory |= item
        self.full_inventory |= item
        self.fill_inventory(monotonic=True)

    def remove_item(self, item: EXTENDED_ITEM):
        self.inventory = self.inventory.remove(item)
        if Inventory(item) <= self.aggregate:
            self.fill_inventory()

    @staticmethod
    def _deep_simplify(requirements, opaques):
        simplified = [len(req.disjunction) > 5 for req in requirements]
        visited = set()
        todo_list = list((range(len(requirements))))

        def simplify(item) -> Tuple[DNFInventory, Set[EXTENDED_ITEM]]:
            hit_a_visited = set()
            if opaques[item]:
                return DNFInventory(item), set()

            if item in visited:
                return DNFInventory(item), {item}

            if simplified[item]:
                return requirements[item], set()

            print(item)

            visited.add(item)
            new_req = DNFInventory()
            for possibility in requirements[item].disjunction:
                simplified_conj = []
                for req_item in possibility.intset:
                    item_req, h_a_v = simplify(req_item)
                    hit_a_visited = hit_a_visited | h_a_v
                    simplified_conj.append(item_req.remove(item))
                new_req |= AndCombination.simplifyDNF(simplified_conj)

            visited.remove(item)
            hit_a_visited.discard(item)
            if not hit_a_visited:
                requirements[item] = new_req
                simplified[item] = True
            else:
                todo_list.append(item)
            return new_req, hit_a_visited

        while todo_list:
            item = EXTENDED_ITEM(todo_list.pop())
            print(item)
            simplify(item)

    def deep_simplify(self):
        self._deep_simplify(self.requirements, self.opaque)

    @staticmethod
    def _simplify_free(requirements):
        for i in Logic._fill_inventory(requirements, Inventory()):
            requirements[i] = DNFInventory(True)

    @staticmethod
    def _shallow_simplify(requirements, opaques):
        simplifiables = Inventory(
            {
                item
                for item in EXTENDED_ITEM.items()
                if len(requirements[item].disjunction) <= 1
            }
        )

        for item, req in enumerate(requirements):
            if opaques[item] or len(req.disjunction) >= 30:
                continue
            new_req = DNFInventory()
            for conj in req.disjunction:
                if conj & simplifiables:
                    new_conj = Inventory()
                    skip = False
                    for req_item in conj.intset:
                        if opaques[req_item] or not simplifiables[req_item]:
                            new_conj |= Inventory(req_item)
                        else:
                            req_item_req = requirements[req_item].disjunction
                            if not req_item_req:
                                skip = True
                                break
                            (req_item_conj,) = req_item_req
                            new_conj |= req_item_conj
                    if not skip and not new_conj[EXTENDED_ITEM(item)]:
                        new_req |= DNFInventory(new_conj)
                else:
                    new_req |= conj
            requirements[item] = new_req

    def shallow_simplify(self):
        self._shallow_simplify(self.requirements, self.opaque)

    @staticmethod
    def aggregate_required_items(
        requirements: List[DNFInventory], inventory: Inventory
    ):
        full_inventory = Logic._fill_inventory(requirements, inventory)
        aggregate = Inventory()

        for item in EXTENDED_ITEM.items():
            if full_inventory[item]:
                for conj in requirements[item].disjunction:
                    aggregate |= conj

        return aggregate

    @staticmethod
    def aggregate_all_useful_items(requirements: List[DNFInventory]):
        aggregate = Inventory()

        for item in EXTENDED_ITEM.items():
            for conj in requirements[item].disjunction:
                aggregate |= conj

        return aggregate

    @staticmethod
    def _fill_inventory(requirements: List[DNFInventory], inventory: Inventory):
        keep_going = True
        while keep_going:
            keep_going = False
            for i in EXTENDED_ITEM.items():
                if not inventory[i] and requirements[i].eval(inventory):
                    inventory |= i
                    keep_going = True
        return inventory

    def fill_inventory(self, monotonic=False):
        # self.shallow_simplify()
        inventory = self.full_inventory if monotonic else self.inventory
        self.full_inventory = self._fill_inventory(self.requirements, inventory)

    @staticmethod
    def explore(checks, area: Area) -> Iterable[EIN]:
        def explore(area):
            for loc in area.locations:
                loc_full = with_sep_full(area.name, loc)
                if loc_full in checks:
                    yield loc_full
            for sub_area in area.sub_areas.values():
                yield from explore(sub_area)

        return explore(area)

    @cache
    def check_list(self, placement_limit: EIN) -> List[EIN]:
        return list(self.explore(self.areas.checks, self.areas[placement_limit]))

    def accessible_checks(self, placement_limit: EIN = EIN("")) -> List[EIN]:
        if placement_limit in self.areas.checks:
            placement_limit2, loc = placement_limit.rsplit("\\", 1)
            locations = self.areas[placement_limit2].locations
            assert loc in locations
            return [EIN(placement_limit2)]
        else:
            return [
                loc
                for loc in self.check_list(placement_limit)
                if self.full_inventory[EXTENDED_ITEM[loc]]
            ]

    def accessible_exits(self, exit_pool: Iterable[PoolExit]) -> Iterable[PoolExit]:
        for exit in exit_pool:
            if exit in self.areas.map_exits:
                if self.full_inventory[EXTENDED_ITEM[exit]]:
                    yield exit

    def _link_connection(self, exit: EIN, entrance: EIN, pool=None, requirements=None):
        allowed_times = self.entrance_allowed_time_of_day[entrance]
        exit_bit = EXTENDED_ITEM[exit]
        exit_area = self.exit_to_area[exit]
        exit_as_req = DNFInventory(exit_bit)

        if exit_area.abstract:
            day_req = exit_as_req
            night_req = exit_as_req
        elif exit_area.allowed_time_of_day == Both:
            day_req = exit_as_req & DNFInventory(
                EXTENDED_ITEM[make_day(exit_area.name)]
            )
            night_req = exit_as_req & DNFInventory(
                EXTENDED_ITEM[make_night(exit_area.name)]
            )
        elif exit_area.allowed_time_of_day == DayOnly:
            day_req = exit_as_req & DNFInventory(EXTENDED_ITEM[exit_area.name])
            night_req = DNFInventory()
        else:
            day_req = DNFInventory()
            night_req = exit_as_req & DNFInventory(EXTENDED_ITEM[exit_area.name])

        if allowed_times == Both:
            bit_req = [
                (EXTENDED_ITEM[make_day(entrance)], day_req),
                (EXTENDED_ITEM[make_night(entrance)], night_req),
            ]
        elif allowed_times == DayOnly:
            bit_req = [(EXTENDED_ITEM[entrance], day_req)]
        else:
            bit_req = [(EXTENDED_ITEM[entrance], night_req)]

        if requirements is None:
            self.placement.map_transitions[exit] = entrance
            self.placement.reverse_map_transitions[entrance] = exit
            for bit, req in bit_req:
                self.opaque[bit] = False
                req = self.ban_if(bit, req)
                self.requirements[bit] |= req
                self.backup_requirements[bit] |= req
        else:
            for bit, req in bit_req:
                req = self.ban_if(bit, req)
                requirements[bit] |= req

    def _place_item(self, location: EIN, item: EIN, requirements=None):
        req = DNFInventory(location)
        if item in self.placement.item_placement_limit and not location.startswith(
            self.placement.item_placement_limit[item]
        ):
            raise ValueError(
                "This item cannot be placed in this area, "
                f"it must be placed in {self.placement.item_placement_limit[item]}"
            )
        if item in EXTENDED_ITEM:
            item_bit = EXTENDED_ITEM[item]
            if requirements is not None:
                req = self.ban_if(item_bit, req)
                requirements[item_bit] = req
            else:
                req = self.ban_if(item_bit, req)
                self.requirements[item_bit] = req
                self.backup_requirements[item_bit] = req
                self.opaque[item_bit] = False
                self.fill_inventory(monotonic=True)
            self.placement.items[item] = location

        self.placement.locations[location] = item

    def place_item(self, location: EIN, item: EIN):
        if location in self.placement.locations:
            raise ValueError(f"Location {location} is already taken")
        if item in self.placement.items:
            raise ValueError(f"Item {item} is already placed")
        self._place_item(location, item)
        return True

    def replace_item(self, location: EIN, item: EIN):
        if location not in self.placement.locations:
            raise ValueError(f"Location {location} is not taken")
        if item in self.placement.items:
            raise ValueError(f"Item {item} is already placed")
        old_item = self.placement.locations[location]
        del self.placement.locations[location]
        del self.placement.items[old_item]

        if old_item in EXTENDED_ITEM:
            # We should always be in this case
            old_item_bit = EXTENDED_ITEM[old_item]
            self.opaque[old_item_bit] = True
            self.backup_requirements[old_item_bit] = DNFInventory()
            self.requirements = self.backup_requirements.copy()
            self.fill_inventory()

        self.place_item(location, item)
        return old_item
