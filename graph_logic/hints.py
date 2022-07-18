from graph_logic.constants import EIN, TRIAL_CHECKS
from graph_logic.inventory import EXTENDED_ITEM
from graph_logic.logic_input import Areas
from hints.hint_distribution import HintDistribution
from hints.hint_types import *
from .randomize import LogicUtils
from options import Options
from paths import RANDO_ROOT_PATH
import yaml
from collections import OrderedDict, defaultdict
from dataclasses import dataclass
from typing import Dict, List, Set

# from .constants import (
#     EXTENDED_ITEM_NAME,
#     POTENTIALLY_REQUIRED_DUNGEONS,
#     ALL_DUNGEON_AREAS,
#     SILENT_REALMS,
#     SILENT_REALM_CHECKS,
# )
from util import textbox_utils


class Hints:
    def __init__(self, options: Options, rng, areas: Areas, logic: LogicUtils):
        self.logic = logic
        self.areas = areas
        self.norm = areas.short_to_full
        self.placement = logic.placement
        self.options = options
        self.rng = rng

        self.hints = OrderedDict()
        with open(
            RANDO_ROOT_PATH
            / f"hints/distributions/{self.options['hint-distribution']}.json"
        ) as f:
            self.dist = HintDistribution()
            self.dist.read_from_file(f)

    def do_hints(self):
        not_banned = self.logic.fill_restricted()
        needed_always_hints: List[EIN] = [
            loc
            for loc, check in self.areas.checks.items()
            if check.get("hint") == "always" and not_banned[check["req_index"]]
        ]

        # in shopsanity, we need to hint some beetle shop items
        # add them manually, cause they need to be kinda weirdly implemented because of bug net
        if (
            self.options["shop-mode"] == "Randomized"
            and "expensive" not in self.options["banned-types"]
        ):
            needed_always_hints.append(self.norm("Beedle - 1200 Rupee Item"))
            needed_always_hints.append(self.norm("Beedle - 1600 Rupee Item"))
        if self.options["song-hints"] == "None":
            for check in TRIAL_CHECKS.values():
                needed_always_hints.append(self.norm(check))
        needed_sometimes_hints = [
            loc
            for loc, check in self.areas.checks.items()
            if check.get("hint") == "sometimes" and not_banned[check["req_index"]]
        ]
        self.dist.start(
            self.areas,
            self.options,
            self.logic,
            self.rng,
            needed_always_hints,
            needed_sometimes_hints,
        )
        hints = self.dist.get_hints(30)
        self._place_hints_for_locations(hints)

    def _place_hints_for_locations(self, hints: List[GossipStoneHint]):
        # make sure hint locations aren't locked by the item they hint

        potential: List[EXTENDED_ITEM] = [
            EXTENDED_ITEM[hint.location]
            for hint in hints
            if isinstance(hint, LocationGossipStoneHint)
            and self.placement.locations[hint.location] in self.logic.get_useful_items()
        ]

        hint_banned_stones: Dict[EIN, Set[EXTENDED_ITEM]] = {}
        for (
            gossipstone_name,
            gossipstone_def,
        ) in self.areas.gossip_stones.items():
            index = gossipstone_def["req_index"]
            hint_banned_stones[gossipstone_name] = {
                item
                for item in potential
                if not self.logic.restricted_test(index, [item])
            }

        stones_to_banned_locs_sorted = sorted(
            hint_banned_stones.items(), key=lambda x: len(x[1]), reverse=True
        )

        assert len(hints) == len(self.areas.gossip_stones) * 2
        unplaced_hints = hints.copy()

        # place locations that are restricted in locations
        for gossipstone_name, banned_locations in stones_to_banned_locs_sorted:
            if gossipstone_name in self.dist.banned_stones:
                self.hints[gossipstone_name] = EmptyGossipStoneHint(
                    self.dist.get_junk_text()
                )
                continue

            valid_locations: List[GossipStoneHint] = [
                hint
                for hint in unplaced_hints
                if not isinstance(hint, LocationGossipStoneHint)
                or EXTENDED_ITEM[hint.location] not in banned_locations
            ]

            nb_hints = 2
            if len(valid_locations) < nb_hints:
                raise ValueError(
                    f"Not enough valid locations for {gossipstone_name} in seed {self.options['seed']}"
                )
                # picked_hints = self.rng.sample(unplaced_hints, nb_hints)
            else:
                picked_hints = self.rng.sample(valid_locations, nb_hints)
            self.hints[gossipstone_name] = GossipStoneHintWrapper(*picked_hints)
            for hint in picked_hints:
                unplaced_hints.remove(hint)
