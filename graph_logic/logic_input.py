from typing import Any, Optional, Dict, List, Tuple
from enum import Enum
from dataclasses import dataclass, field

from .logic_expression import LogicExpression
from .inventory import EXTENDED_ITEM
from .constants import *


AllowedTimeOfDay = Enum("AllowedTimeOfDay", ("DayOnly", "NightOnly", "Both"))
DayOnly = AllowedTimeOfDay.DayOnly
NightOnly = AllowedTimeOfDay.NightOnly
Both = AllowedTimeOfDay.Both

events: List[str] = []
areas_list: "List[Area]" = []


@dataclass
class Area:
    name: str
    allowed_time_of_day: AllowedTimeOfDay = AllowedTimeOfDay.DayOnly
    can_sleep: bool = False
    can_save: bool = False
    sub_areas: "Dict[str, Area]" = field(default_factory=dict)
    locations: Dict[str, LogicExpression] = field(default_factory=dict)
    exits: Dict[str, LogicExpression] = field(default_factory=dict)

    @classmethod
    def of_dict(cls, args):
        return cls(**args)

    @classmethod
    def of_yaml(
        cls,
        name: str,
        raw_dict: Dict[str, Any],
        parent: "Optional[Area]" = None,
    ):
        area = cls(name)

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
        areas_list.append(area)
        return area

    def map(self, floc, fexit):
        d = {}
        for k, v in self.locations.items():
            k, v = floc(self.name, k, v)
            d[k] = v
        self.locations = d

        d = {}
        for k, v in self.exits.items():
            k, v = fexit(self.name, k, v)
            d[k] = v
        self.exits = d

        for sub_area in self.sub_areas.values():
            sub_area.map(floc, fexit)


class Areas:
    areas: Dict[str, Area]

    def search_area(
        self, base_address_str: str, partial_address_str: str
    ) -> Optional[str]:
        """Computes the thing referred by [partial_address] when located at [base_address]"""
        base_address = base_address_str.split("/")
        partial_address = partial_address_str.split(" - ")

        def search_area(i, j, area):
            if len(partial_address) - j == 0:  # We've arrived
                return ""

            hd = partial_address[j]
            if len(partial_address) - j == 1 and (
                hd in area.locations
                or (hd in area.exits and hd in self.map_exit_suffixes)
            ):
                # We've also arrived
                return hd

            if hd in area.sub_areas:  # Abandon the base address, we've branched off
                if (
                    res := search_area(len(base_address), j + 1, area.sub_areas[hd])
                ) is not None:
                    return f"{hd}/{res}"
                return None

            if (
                len(base_address) - i > 0 and len(partial_address) - j > 1
            ):  # Let's follow the base address some more
                hd2 = base_address[i]
                if (res := search_area(i + 1, j, area.sub_areas[hd2])) is not None:
                    return f"{hd2}/{res}"
                return None

            # Now we search everywhere
            for sub_area in area.sub_areas.values():
                if (res := search_area(i, j, sub_area)) is not None:
                    return f"{sub_area.name}/{res}"
            else:
                return None

        res = search_area(0, 0, self.parent_area)
        if res is None:
            raise ValueError(
                f"Could not find '{partial_address_str}' from '{base_address_str}'"
            )
        return res

    def __init__(
        self,
        areas: Dict[str, Any],
        checks: Dict[str, Any],
        gossip_stones: Dict[str, Any],
        map_exits: Dict[str, Any],
    ):
        self.parent_area = Area(
            name="",
            allowed_time_of_day=Both,
            sub_areas={k: Area.of_yaml(k, v) for k, v in areas.items()},
        )
        self.areas = {area.name: area for area in areas_list}
        self.areas[""] = self.parent_area

        EXTENDED_ITEM.items_list.extend(events)
        for area in self.areas.values():
            if area.allowed_time_of_day == Both:
                EXTENDED_ITEM.items_list.append(make_day(area.name))
                EXTENDED_ITEM.items_list.append(make_night(area.name))
            else:
                EXTENDED_ITEM.items_list.append(area.name)

        self.map_exit_suffixes = {
            exit_name.rsplit(" - ", 1)[-1] for exit_name in map_exits
        }

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

        self.short_full = []
        self.checks = set()
        self.gossip_stones = set()
        self.map_exits = set()

        for partial_address in checks:
            full_address = self.search_area("", partial_address)
            self.short_full.append((partial_address, full_address))
            self.checks.add(full_address)

        for partial_address in gossip_stones:
            full_address = self.search_area("", partial_address)
            self.short_full.append((partial_address, full_address))
            self.gossip_stones.add(full_address)

        for partial_address in map_exits:
            full_address = self.search_area("", partial_address)
            exit_type = map_exits[partial_address].get("exit_type", "Both")
            self.short_full.append((partial_address, full_address))
            if exit_type in ("Entrance", "Both"):
                area_name, suffix = full_address.rsplit("/", 1)
                if self.areas[area_name].allowed_time_of_day == Both:
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

        self.exit_to_area = {}
        self.entrance_to_area = {}
        self.entrance_allowed_time_of_day = {}

        self.requirements = [DNFInventory() for i in EXTENDED_ITEM.items()]
        self.opaque = [True for i in EXTENDED_ITEM.items()]

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
                    timed_req = req.day_only() & DNFInv(area_name)
                else:
                    timed_req = req.night_only() & DNFInv(area_name)
                loc_bit = EXTENDED_ITEM[area_name + "/" + loc]
                reqs[loc_bit] = timed_req
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
                            reqs[darea_bit] |= req.day_only() & DNFInv(area_name)
                        elif area.allowed_time_of_day == NightOnly:
                            reqs[narea_bit] |= req.night_only() & DNFInv(area_name)
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
                            reqs[area_bit] |= timed_req & DNFInv(area_name)
                        else:
                            raise ValueError("Time makes this exit impossible")

                else:  # Map exit
                    exit = area_name + "/" + exit
                    exit_type = map_exits[self.full_to_short(exit)].get(
                        "exit_type", "Both"
                    )
                    if exit_type in ("Entrance", "Both"):
                        entrance = make_entrance(exit)
                        self.entrance_allowed_time_of_day[
                            entrance
                        ] = area.allowed_time_of_day
                        if area.allowed_time_of_day == Both:
                            darea_bit = EXTENDED_ITEM[make_day(area_name)]
                            narea_bit = EXTENDED_ITEM[make_night(area_name)]
                            self.opaque[darea_bit] = False
                            self.opaque[narea_bit] = False
                            reqs[darea_bit] |= DNFInv(make_day(entrance))
                            reqs[narea_bit] |= DNFInv(make_night(entrance))
                            self.entrance_to_area[make_day(entrance)] = darea_bit
                            self.entrance_to_area[make_night(entrance)] = narea_bit
                        elif area.allowed_time_of_day == NightOnly:
                            area_bit = EXTENDED_ITEM[area_name]
                            self.opaque[area_bit] = False
                            reqs[area_bit] |= DNFInv(entrance)
                            self.entrance_to_area[entrance] = area_bit

                    if exit_type in ("Exit", "Both"):
                        exit = make_exit(exit)
                        exit_bit = EXTENDED_ITEM[exit]
                        reqs[exit_bit] = req
                        self.opaque[exit_bit] = False
                        self.exit_to_area[exit] = area
