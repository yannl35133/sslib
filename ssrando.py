from collections import OrderedDict
import sys
import os
import re
import random
from pathlib import Path
import hashlib
import json
import yaml
import subprocess
from graph_logic.constants import *
from graph_logic.inventory import EXTENDED_ITEM
from graph_logic.logic_input import Areas
from yaml_files import graph_requirements, checks, hints, map_exits
import SpoilerLog


# from logic.logic import Logic
from graph_logic.randomize import Rando

# from logic.hints import Hints
from graph_logic.hints import Hints

# import logic.constants as constants
# from logic.placement_file import PlacementFile
from graph_logic.placement_file import PlacementFile
from gamepatches import GamePatcher, GAMEPATCH_TOTAL_STEP_COUNT
from paths import RANDO_ROOT_PATH, IS_RUNNING_FROM_SOURCE
from options import OPTIONS, Options

# import logic.item_types
from sslib.utils import encodeBytes
from version import VERSION, VERSION_WITHOUT_COMMIT

from typing import List, Callable


class StartupException(Exception):
    pass


def dummy_progress_callback(current_action_name):
    pass


class BaseRandomizer:
    """Class holding all the path and callback info for the GamePatcher"""

    def __init__(self, progress_callback=dummy_progress_callback):
        self.progress_callback = progress_callback
        # TODO: maybe make paths configurable?
        # exe root path is where the executable is
        self.exe_root_path = Path(".").resolve()
        # this is where all assets/read only files are
        self.rando_root_path = RANDO_ROOT_PATH
        self.actual_extract_path = self.exe_root_path / "actual-extract"
        self.modified_extract_path = self.exe_root_path / "modified-extract"
        self.oarc_cache_path = self.exe_root_path / "oarc"
        self.log_file_path = self.exe_root_path / "logs"
        self.log_file_path.mkdir(exist_ok=True, parents=True)

        # not happy that is has to land here, it's used by both GamePatches and Logic
        with (self.rando_root_path / "checks.yaml").open("r") as f:
            self.item_locations = yaml.load(f, YamlOrderedDictLoader)

        for location_name in self.item_locations:
            if not "type" in self.item_locations[location_name]:
                print("ERROR, " + location_name + " doesn't have types!")
            types_string = self.item_locations[location_name]["type"]
            types = types_string.split(",")
            types = set((type.strip() for type in types))
            self.item_locations[location_name]["type"] = types

        with (RANDO_ROOT_PATH / "hints.yaml").open() as f:
            self.stonehint_definitions: dict = yaml.safe_load(f)

    def randomize(self):
        """patch the game, or only write the spoiler log, depends on the implementation"""
        raise NotImplementedError("abstract")


class Randomizer(BaseRandomizer):
    def __init__(
        self, areas: Areas, options: Options, progress_callback=dummy_progress_callback
    ):
        super().__init__(progress_callback)
        self.areas = areas
        self.options = options

        self.no_logs = self.options["no-spoiler-log"]

        self.seed = self.options["seed"]
        if self.seed == -1:
            self.seed = random.randint(0, 1000000)
        self.options.set_option("seed", self.seed)

        self.rng = random.Random()
        print(f"Seed: {self.seed}")
        self.rng.seed(self.seed)
        if self.no_logs:
            for _ in range(100):
                self.rng.random()
        self.rando = Rando(self.areas, self.options, self.rng)
        self.logic = self.rando.logic
        self.hints = Hints(self.options, self.rng, self.areas, self.logic)

        self.dry_run = bool(self.options["dry-run"])
        self.banned_types = self.options["banned-types"]
        self.randomizer_hash = self._get_rando_hash()

    def _get_rando_hash(self):
        # hash of seed, options, version
        current_hash = hashlib.md5()
        current_hash.update(str(self.seed).encode("ASCII"))
        current_hash.update(self.options.get_permalink().encode("ASCII"))
        current_hash.update(VERSION.encode("ASCII"))
        with open(RANDO_ROOT_PATH / "names.txt") as f:
            names = [s.strip() for s in f.readlines()]
        hash_random = random.Random()
        hash_random.seed(current_hash.digest())
        return " ".join(hash_random.choice(names) for _ in range(3))

    def check_valid_directory_setup(self):
        # catch common errors with directory setup
        if not self.actual_extract_path.is_dir():
            raise StartupException(
                "ERROR: directory actual-extract doesn't exist! Make sure you have the ISO extracted into that directory"
            )
        if not self.modified_extract_path.is_dir():
            raise StartupException(
                "ERROR: directory modified-extract doesn't exist! Make sure you have the contents of actual-extract copied over to modified-extract"
            )
        if not (self.actual_extract_path / "DATA").is_dir():
            raise StartupException(
                "ERROR: directory actual-extract doesn't contain a DATA directory! Make sure you have the ISO properly extracted into actual-extract"
            )
        if not (self.modified_extract_path / "DATA").is_dir():
            raise StartupException(
                "ERROR: directory 'DATA' in modified-extract doesn't exist! Make sure you have the contents of actual-extract copied over to modified-extract"
            )
        if not (
            self.modified_extract_path
            / "DATA"
            / "files"
            / "COPYDATE_CODE_2011-09-28_153155"
        ).exists():
            raise StartupException("ERROR: the randomizer only supports NTSC-U 1.00")

    def get_total_progress_steps(self):
        if self.dry_run:
            return 2
        else:
            return 2 + GAMEPATCH_TOTAL_STEP_COUNT

    def set_progress_callback(self, progress_callback: Callable[[str], None]):
        self.progress_callback = progress_callback

    def randomize(self):
        self.progress_callback("randomizing items...")
        self.rando.randomize()
        del self.rando
        self.hints.do_hints()
        if self.no_logs:
            self.progress_callback("writing anti spoiler log...")
        else:
            self.progress_callback("writing spoiler log...")
        plcmt_file = self.get_placement_file()
        if self.options["out-placement-file"] and not self.no_logs:
            (self.log_file_path / f"placement_file_{self.seed}.json").write_text(
                plcmt_file.to_json_str()
            )

        anti = "Anti " if self.no_logs else ""
        ext = "json" if self.options["json"] else "txt"
        log_address = self.log_file_path / (
            f"SS Random {self.seed} - {anti}Spoiler Log.{ext}"
        )

        if self.options["json"]:
            dump = SpoilerLog.dump_json(
                self.logic.placement,
                self.options,
                hash=self.randomizer_hash,
                progression_spheres=self.logic.calculate_playthrough_progression_spheres(),
                hints=self.hints.hints,
                required_dungeons=self.logic.required_dungeons,
                sots_items={
                    goal: self.logic.get_sots_items(GOAL_CHECKS[goal])
                    for goal in ALL_GOALS
                },
                barren_nonprogress=self.logic.get_barren_regions(weak=True),
                randomized_dungeon_entrance=self.logic.randomized_dungeon_entrance,
                randomized_trial_entrance=self.logic.randomized_trial_entrance,
            )
            with log_address.open("w") as f:
                json.dump(dump, f, indent=2)
        else:
            with log_address.open("w") as f:
                SpoilerLog.write(
                    f,
                    self.logic.placement,
                    self.options,
                    self.areas,
                    hash=self.randomizer_hash,
                    progression_spheres=self.logic.calculate_playthrough_progression_spheres(),
                    hints=self.hints.hints,
                    required_dungeons=self.logic.required_dungeons,
                    sots_items={
                        goal: self.logic.get_sots_items(GOAL_CHECKS[goal])
                        for goal in ALL_GOALS
                    },
                    barren_nonprogress=self.logic.get_barren_regions(weak=True),
                    randomized_dungeon_entrance=self.logic.randomized_dungeon_entrance,
                    randomized_trial_entrance=self.logic.randomized_trial_entrance,
                )
        if not self.dry_run:
            GamePatcher(
                self.areas,
                self.options,
                self.progress_callback,
                self.actual_extract_path,
                self.rando_root_path,
                self.exe_root_path,
                self.modified_extract_path,
                self.oarc_cache_path,
                plcmt_file,
            ).do_all_gamepatches()
        self.progress_callback("patching done")

    def get_placement_file(self):
        # temporary placement file stuff
        trial_checks = {
            # (getting it text patch, inventory text line)
            SKYLOFT_TRIAL: "Song of the Hero - Trial Hint",
            FARON_TRIAL: "Farore's Courage - Trial Hint",
            LANAYRU_TRIAL: "Nayru's Wisdom - Trial Hint",
            ELDIN_TRIAL: "Din's Power - Trial Hint",
        }
        trial_hints = {}
        for (trial, hintname) in trial_checks.items():
            randomized_trial = self.logic.randomized_trial_entrance[trial]
            randomized_check = TRIAL_CHECKS[randomized_trial]
            item = self.logic.placement.locations[
                self.areas.short_to_full(randomized_check)
            ]
            hint_mode = self.options["song-hints"]
            if hint_mode == "Basic":
                if item in self.logic.get_useful_items(weak=True):
                    useful_text = "You might need what it reveals..."
                    # print(f'{item} in {trial_check} is useful')
                else:
                    useful_text = "It's probably not too important..."
                    # print(f'{item} in {trial_check} is not useful')
            elif hint_mode == "Advanced":
                if item in self.logic.get_sots_items():
                    useful_text = "Your spirit will grow by completing this trial"
                elif item in self.logic.get_useful_items(weak=True):
                    useful_text = "You might need what it reveals..."
                else:
                    # barren
                    useful_text = "It's probably not too important..."
            elif hint_mode == "Direct":
                useful_text = f"This trial holds {item}"
            else:
                useful_text = ""
            trial_hints[hintname] = useful_text

        plcmt_file = PlacementFile()
        plcmt_file.dungeon_connections = self.logic.randomized_dungeon_entrance
        plcmt_file.trial_connections = self.logic.randomized_trial_entrance
        plcmt_file.hash_str = self.randomizer_hash
        plcmt_file.gossip_stone_hints = dict(
            (k, v.to_gossip_stone_text(lambda s: self.areas.prettify(s, custom=True)))
            for (k, v) in self.hints.hints.items()
        )
        plcmt_file.trial_hints = trial_hints
        plcmt_file.item_locations = self.logic.placement.locations
        plcmt_file.options = self.options
        plcmt_file.required_dungeons = self.logic.required_dungeons
        plcmt_file.starting_items = sorted(self.logic.placement.starting_items)
        plcmt_file.version = VERSION

        # plcmt_file.check_valid()

        return plcmt_file


class PlandoRandomizer(BaseRandomizer):
    def __init__(
        self, placement_file: PlacementFile, progress_callback=dummy_progress_callback
    ):
        super().__init__(progress_callback)
        self.placement_file = placement_file

    def get_total_progress_steps(self):
        return GAMEPATCH_TOTAL_STEP_COUNT

    def randomize(self):
        GamePatcher(
            self.areas,
            self.options,
            self.progress_callback,
            self.actual_extract_path,
            self.rando_root_path,
            self.exe_root_path,
            self.modified_extract_path,
            self.oarc_cache_path,
            self.placement_file,
        ).do_all_gamepatches()


class YamlOrderedDictLoader(yaml.SafeLoader):
    pass


YamlOrderedDictLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
    lambda loader, node: OrderedDict(loader.construct_pairs(node)),
)
