from graph_logic.constants import EIN, HINTS, MAX_HINTS, TRIAL_CHECKS
from graph_logic.inventory import EXTENDED_ITEM
from graph_logic.logic import DNFInventory
from graph_logic.logic_input import Areas
from hints.hint_distribution import HintDistribution
from hints.hint_types import *
from .randomize import LogicUtils, UserOutput
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


MAX_HINTS_PER_STONE = 2


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

    def do_hints(self, useroutput: UserOutput):
        self.useroutput = useroutput

        not_banned = self.logic.fill_restricted()
        needed_always_hints: List[EIN] = [
            loc
            for loc, check in self.areas.checks.items()
            if check.get("hint") == "always" and not_banned[check["req_index"]]
        ]
        needed_sometimes_hints = [
            loc
            for loc, check in self.areas.checks.items()
            if check.get("hint") == "sometimes" and not_banned[check["req_index"]]
        ]

        # ensure prerandomized locations cannot be hinted
        unhintables = list(self.logic.known_locations)

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
        else:
            for check in TRIAL_CHECKS.values():
                unhintables.append(self.norm(check))

        self.dist.start(
            self.areas,
            self.options,
            self.logic,
            self.rng,
            unhintables,
            needed_always_hints,
            needed_sometimes_hints,
        )
        hints = self.dist.get_hints(MAX_HINTS)
        self.useroutput.progress_callback("placing hints...")
        hints = {hintname: hint for hint, hintname in zip(hints, HINTS)}
        self.randomize(hints)

        return {
            stone: GossipStoneHintWrapper(*(hints[name] for name in hintnames))
            for stone, hintnames in self.logic.placement.stones.items()
        }

    def randomize(self, hints: Dict[EIN, GossipStoneHint]):
        for hintname, hint in hints.items():
            hint_bit = EXTENDED_ITEM[hintname]
            if isinstance(hint, LocationGossipStoneHint):
                itembit = EXTENDED_ITEM[hint.item]
                self.logic.backup_requirements[itembit] &= DNFInventory(hint_bit)

            self.logic.inventory |= hint_bit

        self.logic.aggregate = self.logic.aggregate_requirements(
            self.logic.requirements, None
        )
        self.logic.fill_inventory_i(monotonic=False)

        for hintname in HINTS:
            if not self.place_hint(hintname):
                raise self.useroutput.GenerationFailed(f"could not place {hintname}")

    def place_hint(self, hintname: EXTENDED_ITEM_NAME, depth=0) -> bool:
        hint_bit = EXTENDED_ITEM[hintname]
        self.logic.remove_item(hint_bit)

        accessible_stones = self.logic.accessible_stones()

        available_stones = [
            stone
            for stone in accessible_stones
            if len(self.logic.placement.stones[stone]) < MAX_HINTS_PER_STONE
        ]

        if available_stones:
            stone = self.rng.choice(available_stones)
            result = self.logic.place_item(stone, hintname, hint_mode=True)
            assert result  # Undefined if False
            return True

        # We have to replace an already placed hint
        if depth > 50:
            return False
        if not available_stones:
            raise self.useroutput.GenerationFailed(
                f"no more location accessible for {hintname}"
            )

        stone = self.rng.choice(accessible_stones)
        old_hints = self.placement.stones[stone]
        assert old_hints
        old_hint = self.rng.choice(old_hints)
        new_hint = self.logic.replace_item(stone, hintname, old_hint)
        return self.place_hint(new_hint, depth + 1)
