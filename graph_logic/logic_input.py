from __future__ import annotations
from typing import Dict, Generic, List, Any, Tuple, TypeVar
from enum import Enum
from dataclasses import dataclass, field

from .logic_expression import DNFInventory, LogicExpression
from .inventory import EXTENDED_ITEM
from .constants import *


AllowedTimeOfDay = Enum("AllowedTimeOfDay", ("DayOnly", "NightOnly", "Both"))
DayOnly = AllowedTimeOfDay.DayOnly
NightOnly = AllowedTimeOfDay.NightOnly
Both = AllowedTimeOfDay.Both


class defaultfactorydict(dict):
    def __missing__(self, item):
        return item


events: List[EXTENDED_ITEM_NAME] = []
areas_list: List[Area[LogicExpression]] = []

LE = TypeVar("LE")
LE_bis = TypeVar("LE_bis")


@dataclass
class Area(Generic[LE]):
    name: str
    allowed_time_of_day: AllowedTimeOfDay = AllowedTimeOfDay.DayOnly
    can_sleep: bool = False
    can_save: bool = False
    sub_areas: Dict[str, Area[LE]] = field(default_factory=dict)
    locations: Dict[str, LE] = field(default_factory=dict)
    exits: Dict[str, LE] = field(default_factory=dict)

    @classmethod
    def of_dict(cls, args):
        return cls(**args)

    @classmethod
    def of_yaml(
        cls,
        name: str,
        raw_dict: Dict[str, Any],
        parent: Area[LogicExpression] | None = None,
    ):
        area: Area[LogicExpression] = cls(name)  # type: ignore

        if (v := raw_dict.get("allowed-time-of-day")) is not None:
            area.allowed_time_of_day = AllowedTimeOfDay[v]
        elif parent is not None:
            area.allowed_time_of_day = parent.allowed_time_of_day
        if (b := raw_dict.get("can-sleep")) is not None:
            area.can_sleep = b
        if (b := raw_dict.get("can-save")) is not None:
            area.can_save = b

        if (d := raw_dict.get("locations")) is not None:
            area.locations = {k: LogicExpression.parse(v) for k, v in d.items()}
            for k in d:
                events.append(with_sep_full(name, k))

        if (d := raw_dict.get("exits")) is not None:
            area.exits = {k: LogicExpression.parse(v) for k, v in d.items()}

        if (v := raw_dict.get("entrance")) is not None:
            if parent is None:
                raise ValueError("An entrance was given but no parent to give it to")
            parent.exits[name.rsplit("/", 1)[-1]] = LogicExpression.parse(v)

        area.sub_areas = {
            k: cls.of_yaml(with_sep_full(name, k), v, area)
            for k, v in raw_dict.items()
            if "A" <= k[0] <= "Z"
        }
        areas_list.append(area)
        return area

    def map(
        self,
        floc: Callable[[str, str, LE], Tuple[str, LE_bis]],
        fexit: Callable[[str, str, LE], Tuple[str, LE_bis]],
    ):
        new_self: Area[LE_bis] = self  # type: ignore
        d: Dict[str, LE_bis] = {}
        for k, v in self.locations.items():
            k, v = floc(self.name, k, v)
            d[k] = v
        new_self.locations = d

        d = {}
        for k, v in self.exits.items():
            k, v = fexit(self.name, k, v)
            d[k] = v
        new_self.exits = d

        for sub_area in self.sub_areas.values():
            sub_area.map(floc, fexit)


class Areas:
    areas: Dict[str, Area[DNFInventory]]

    def __getitem__(self, loc):
        return self.areas[loc]

    def search_area(
        self, base_address_str: str, partial_address_str: str, multiple=False
    ) -> EXTENDED_ITEM_NAME:
        """Computes the thing referred by [partial_address] when located at [base_address]"""
        base_address = base_address_str.split("/")
        partial_address = partial_address_str.split(" - ")

        def search_area(i, j, area: Area) -> List[str]:
            if len(partial_address) - j == 0:  # We've arrived
                return [area.name]

            hd = partial_address[j]
            if len(partial_address) - j == 1 and (
                hd in area.locations
                or (hd in area.exits and hd in self.map_exit_suffixes)
            ):
                # We've also arrived
                return [with_sep_full(area.name, hd)]

            if hd in area.sub_areas:  # Abandon the base address, we've branched off
                return search_area(len(base_address), j + 1, area.sub_areas[hd])

            if len(base_address) - i > 0:
                # Let's follow the base address some more
                return search_area(i + 1, j, area.sub_areas[base_address[i]])

            # Now we search everywhere
            matches: List[str] = []
            for sub_area in area.sub_areas.values():
                if (match := search_area(i, j, sub_area)) != []:
                    if not multiple:
                        return match
                    matches.extend(match)
            return matches

        res = search_area(0, 0, self.parent_area)
        if res == []:
            raise ValueError(
                f"Could not find '{partial_address_str}' from '{base_address_str}'"
            )
        if multiple and len(res) > 1:
            for loc in res:
                self.normalize[EIN(loc)] = EIN(res[0])
        return EIN(res[0])

    def __init__(
        self,
        raw_area: Dict[str, Any],
        checks: Dict[str, Any],
        gossip_stones: Dict[str, Any],
        map_exits: Dict[str, Any],
    ):
        self.parent_area = Area.of_yaml(name="", raw_dict=raw_area)
        areas = {area.name: area for area in areas_list}

        EXTENDED_ITEM.items_list.extend(events)
        for area in areas.values():
            if area.allowed_time_of_day == Both:
                EXTENDED_ITEM.items_list.append(make_day(area.name))
                EXTENDED_ITEM.items_list.append(make_night(area.name))
            else:
                EXTENDED_ITEM.items_list.append(EIN(area.name))

        self.map_exit_suffixes = {
            exit_name.rsplit(" - ", 1)[-1] for exit_name in map_exits
        }
        self.normalize: Dict[EIN, EIN] = defaultfactorydict()

        self.parent_area.map(
            lambda prefix, k, v: (
                k,
                v.localize(lambda text: self.search_area(prefix, text)),
            ),
            lambda prefix, k, v: (
                k if k in self.map_exit_suffixes else self.search_area(prefix, k),
                v.localize(lambda text: self.search_area(prefix, text)),
            ),
        )

        new_areas: Dict[str, Area[DNFInventory]] = areas  # type: ignore
        # It doesn't understand that the type has changed, but it has
        self.areas: Dict[str, Area[DNFInventory]] = new_areas

        self.short_full: List[Tuple[str, EXTENDED_ITEM_NAME]] = []
        self.entrance_allowed_time_of_day = {}
        self.checks = set()
        self.gossip_stones = set()
        self.map_exits = set()

        for partial_address in checks:
            full_address = self.search_area("", partial_address, multiple=True)
            self.short_full.append((partial_address, full_address))
            self.checks.add(full_address)

        for partial_address in gossip_stones:
            full_address = self.search_area("", partial_address, multiple=True)
            self.short_full.append((partial_address, full_address))
            self.gossip_stones.add(full_address)

        for partial_address in map_exits:
            full_address = self.search_area("", partial_address, multiple=True)
            exit_type = map_exits[partial_address].get("exit-type", "Both")
            self.short_full.append((partial_address, full_address))
            if exit_type in ("Entrance", "Both"):
                area_name, suffix = full_address.rsplit("/", 1)
                allowed_time_of_day_str = map_exits[partial_address].get(
                    "allowed-time-of-day", None
                )
                allowed_time_of_day = (
                    AllowedTimeOfDay[allowed_time_of_day_str]
                    if allowed_time_of_day_str is not None
                    else self.areas[area_name].allowed_time_of_day
                )
                self.entrance_allowed_time_of_day[full_address] = allowed_time_of_day
                if allowed_time_of_day == Both:
                    EXTENDED_ITEM.items_list.append(
                        make_day(make_entrance(full_address))
                    )
                    EXTENDED_ITEM.items_list.append(
                        make_night(make_entrance(full_address))
                    )
                else:
                    EXTENDED_ITEM.items_list.append(make_entrance(full_address))

                self.short_full.append(
                    (
                        make_entrance(partial_address),
                        make_entrance(full_address),
                    )
                )
                self.map_exits.add(make_entrance(full_address))
            if exit_type in ("Exit", "Both"):
                EXTENDED_ITEM.items_list.append(make_exit(full_address))
                self.short_full.append(
                    (make_exit(partial_address), make_exit(full_address))
                )
                self.map_exits.add(make_exit(full_address))

        def short_to_full(elt: str):
            for (a, b) in self.short_full:
                if a == elt:
                    return b
            raise ValueError("Error: association list")

        def full_to_short(elt: EXTENDED_ITEM_NAME):
            for (a, b) in self.short_full:
                if b == elt:
                    return a
            raise ValueError("Error: association list")

        self.short_to_full = short_to_full
        self.full_to_short = full_to_short

        self.exit_to_area = {}
        self.entrance_allowed_time_of_day = {}

        self.requirements = [DNFInventory() for _ in EXTENDED_ITEM.items()]
        self.opaque = [True for _ in EXTENDED_ITEM.items()]

        reqs = self.requirements  # Local alias
        DNFInv = DNFInventory

        for area_name, area in self.areas.items():
            if area.can_sleep:
                # If one day we allow sleeping to be randomized, change the following to regular connections
                assert area.allowed_time_of_day == Both
                darea_bit = EXTENDED_ITEM[make_day(area_name)]
                narea_bit = EXTENDED_ITEM[make_night(area_name)]
                self.opaque[darea_bit] = False
                self.opaque[narea_bit] = False
                reqs[darea_bit] |= DNFInv(narea_bit)
                reqs[narea_bit] |= DNFInv(darea_bit)

            for loc, req in area.locations.items():
                if area.allowed_time_of_day == Both:
                    timed_req = (req.day_only() & DNFInv(make_day(area_name))) | (
                        req.night_only() & DNFInv(make_night(area_name))
                    )
                elif area.allowed_time_of_day == DayOnly:
                    timed_req = req.day_only() & DNFInv(EIN(area_name))
                else:
                    timed_req = req.night_only() & DNFInv(EIN(area_name))
                loc_bit = EXTENDED_ITEM[self.normalize[area_name + "/" + loc]]
                reqs[loc_bit] |= timed_req
                self.opaque[loc_bit] = False

            for exit, req in area.exits.items():
                if exit in self.areas:  # Logical exit, the name is the area
                    area_dest = self.areas[exit]
                    if area_dest.allowed_time_of_day == Both:
                        darea_bit = EXTENDED_ITEM[make_day(area_dest.name)]
                        narea_bit = EXTENDED_ITEM[make_night(area_dest.name)]
                        self.opaque[darea_bit] = False
                        self.opaque[narea_bit] = False

                        if area.allowed_time_of_day == Both:
                            reqs[darea_bit] |= req.day_only() & DNFInv(
                                make_day(area_name)
                            )
                            reqs[narea_bit] |= req.night_only() & DNFInv(
                                make_night(area_name)
                            )
                        elif area.allowed_time_of_day == DayOnly:
                            reqs[darea_bit] |= req.day_only() & DNFInv(EIN(area_name))
                        elif area.allowed_time_of_day == NightOnly:
                            reqs[narea_bit] |= req.night_only() & DNFInv(EIN(area_name))
                    else:
                        area_bit = EXTENDED_ITEM[area_dest.name]
                        self.opaque[area_bit] = False
                        if area_dest.allowed_time_of_day == DayOnly:
                            timed_req = req.day_only()
                            timed_area = make_day(area_name)
                        else:
                            timed_req = req.night_only()
                            timed_area = make_night(area_name)
                        if area.allowed_time_of_day == Both:
                            reqs[area_bit] |= timed_req & DNFInv(timed_area)
                        elif area.allowed_time_of_day == area_dest.allowed_time_of_day:
                            reqs[area_bit] |= timed_req & DNFInv(EIN(area_name))
                        else:
                            raise ValueError("Time makes this exit impossible")

                else:  # Map exit
                    exit = self.normalize[area_name + "/" + exit]
                    short_exit = self.full_to_short(exit)
                    exit_type = map_exits[short_exit].get("exit-type", "Both")
                    if exit_type in ("Entrance", "Both"):
                        full_entrance = exit
                        entrance = make_entrance(full_entrance)
                        allowed_time_of_day = self.entrance_allowed_time_of_day[
                            full_entrance
                        ]
                        if allowed_time_of_day == Both:
                            darea_bit = EXTENDED_ITEM[make_day(area_name)]
                            narea_bit = EXTENDED_ITEM[make_night(area_name)]
                            self.opaque[darea_bit] = False
                            self.opaque[narea_bit] = False
                            reqs[darea_bit] |= DNFInv(make_day(entrance))
                            reqs[narea_bit] |= DNFInv(make_night(entrance))
                        else:
                            if area.allowed_time_of_day == Both:
                                if allowed_time_of_day == DayOnly:
                                    area_bit = EXTENDED_ITEM[make_day(area_name)]
                                else:
                                    area_bit = EXTENDED_ITEM[make_night(area_name)]
                            else:
                                area_bit = EXTENDED_ITEM[area_name]
                            self.opaque[area_bit] = False
                            reqs[area_bit] |= DNFInv(entrance)

                    if exit_type in ("Exit", "Both"):
                        exit = make_exit(exit)
                        exit_bit = EXTENDED_ITEM[exit]
                        reqs[exit_bit] = req
                        self.opaque[exit_bit] = False
                        self.exit_to_area[exit] = area
