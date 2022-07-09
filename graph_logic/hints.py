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
from typing import List

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
        hints = []
        i = 0
        while i < 30:
            hint = self.dist.next_hint()
            if hint is not None:
                hints.append(hint)
                i += 1
        self._place_hints_for_locations(hints)

    def _place_hints_for_locations(self, hints: List[GossipStoneHint]):
        # make sure hint locations aren't locked by the item they hint
        hint_banned_stones = defaultdict(set)

        potential = (
            EXTENDED_ITEM[hint.location]
            for hint in hints
            if hint.needs_logic
            and self.placement.locations[hint.location] in self.logic.get_useful_items()
        )

        for (
            gossipstone_name,
            gossipstone_def,
        ) in self.areas.gossip_stones.items():
            index = gossipstone_def["req_index"]
            hint_banned_stones[gossipstone_name] = {
                item for item in potential if self.logic.restricted_test(index, [item])
            }

        stones_to_banned_locs_sorted = sorted(
            hint_banned_stones.items(), key=lambda x: len(x[1]), reverse=True
        )

        if len(hints) < len(self.areas.gossip_stones) * 2:
            hints.extend([None] * (len(self.areas.gossip_stones) * 2 - len(hints)))
        unplace_hints = hints.copy()

        hint_to_location = {}
        # place locations that are restricted in locations
        for gossipstone_name, banned_locations in stones_to_banned_locs_sorted:
            valid_locations = [
                loc for loc in unplace_hints if not loc in banned_locations
            ]
            if len(valid_locations) == 0:
                print(
                    f"no valid location for {gossipstone_name} in seed {self.options['seed']}"
                )
                loc_to_hint = unplace_hints[0]
                second_loc_to_hint = unplace_hints[1]
                # raise Exception('no valid location to place hint!')
            else:
                loc_to_hint = self.rng.choice(valid_locations)
                # ensure we dont try to place the same hint twice
                removed_list = valid_locations.copy()
                removed_list.remove(loc_to_hint)
                second_loc_to_hint = self.rng.choice(removed_list)
            hint_to_location[gossipstone_name] = [loc_to_hint, second_loc_to_hint]
            unplace_hints.remove(loc_to_hint)
            unplace_hints.remove(second_loc_to_hint)
        # place locations that aren't restricted and also fill rest of locations
        for gossipstone_name in [
            name for name in self.areas.gossip_stones if not name in hint_to_location
        ]:
            if len(unplace_hints) == 0:
                # placeholder
                hint_to_location[gossipstone_name] = [None]
                continue
            loc_to_hint = self.rng.choice(unplace_hints)
            unplace_hints.remove(loc_to_hint)
            second_loc_to_hint = self.rng.choice(unplace_hints)
            unplace_hints.remove(second_loc_to_hint)
            hint_to_location[gossipstone_name] = [loc_to_hint, second_loc_to_hint]
        anywhere_hints = [hint for hint in hints if not hint.needs_logic]
        self.rng.shuffle(anywhere_hints)

        for gossipstone_name in self.areas.gossip_stones:
            if gossipstone_name in self.dist.banned_stones:
                self.hints[gossipstone_name] = EmptyGossipStoneHint(
                    None, None, False, self.dist.get_junk_text()
                )
            else:
                locs_to_hint = hint_to_location[gossipstone_name]
                loc_to_hint = locs_to_hint[0]
                second_loc_to_hint = locs_to_hint[1]
                if second_loc_to_hint is None and loc_to_hint is not None:
                    if len(anywhere_hints) > 0:
                        self.hints[gossipstone_name] = GossipStoneHintWrapper(
                            loc_to_hint,
                            BarrenGossipStoneHint(zone=anywhere_hints.pop()),
                        )
                    else:
                        self.hints[gossipstone_name] = loc_to_hint
                elif second_loc_to_hint is not None and loc_to_hint is None:
                    if len(anywhere_hints) > 0:
                        self.hints[gossipstone_name] = GossipStoneHintWrapper(
                            BarrenGossipStoneHint(zone=anywhere_hints.pop()),
                            second_loc_to_hint,
                        )
                    else:
                        self.hints[gossipstone_name] = second_loc_to_hint
                elif loc_to_hint is None:
                    # place barren hints at locations with no hints
                    if len(anywhere_hints) < 0:
                        hint = anywhere_hints.pop()
                    else:
                        hint = None
                    if hint is not None:
                        self.hints[gossipstone_name] = hint
                    else:
                        self.hints[gossipstone_name] = EmptyGossipStoneHint(
                            None, None, False, self.dist.get_junk_text()
                        )
                else:
                    self.hints[gossipstone_name] = GossipStoneHintWrapper(
                        loc_to_hint, second_loc_to_hint
                    )
