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
    def __init__(self, options: Options, progress_callback=dummy_progress_callback):
        super().__init__(progress_callback)
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
        self.areas = Areas(graph_requirements, checks, hints, map_exits)
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
        if self.options["json"]:
            self.write_spoiler_log_json()
        else:
            self.write_spoiler_log()
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

    def write_spoiler_log(self):
        spoiler_log = self.get_log_header()

        if self.no_logs:
            # We still calculate progression spheres even if we're not going to write them anywhere to catch more errors in testing.
            self.logic.calculate_playthrough_progression_spheres()

            spoiler_log_output_path = self.log_file_path / (
                "SS Random %s - Anti Spoiler Log.txt" % self.seed
            )
            with spoiler_log_output_path.open("w") as f:
                f.write(spoiler_log)

            return

        if len(self.logic.placement.starting_items) > 0:
            spoiler_log += "\n\nStarting items:\n  "
            spoiler_log += "\n  ".join(self.logic.placement.starting_items)
        spoiler_log += "\n\n\n"

        # Write required dungeons
        for i, dungeon in enumerate(self.logic.required_dungeons, start=1):
            spoiler_log += f"Required Dungeon {i}: " + dungeon + "\n"

        spoiler_log += "\n\n"

        # Write way of the hero (100% required) locations
        spoiler_log += "SotS:\n"
        for item in self.logic.get_sots_items():
            location = self.logic.placement.items[item]
            spoiler_log += "  %-53s %s\n" % (location + ":", item)

        spoiler_log += "\n\n"

        # Write path locations; locations 100% required to complete a given required dungeon
        spoiler_log += "Path:\n"
        for goal in GOALS:
            spoiler_log += f"{goal}:\n"
            dungeon = GOAL_DUNGEONS[goal]
            check = DUNGEON_FINAL_CHECK[dungeon]
            for item in self.logic.get_sots_items(check):
                loc = self.logic.placement.items[item]
                spoiler_log += "  %-53s %s\n" % (loc + ":", item)

        spoiler_log += "\n\n"

        barren, nonprogress = self.logic.get_barren_regions()
        spoiler_log += "Barren Regions:\n"
        for region in barren:
            spoiler_log += "  " + region + "\n"
        spoiler_log += "\n\n"

        spoiler_log += "Nonprogress Regions:\n"
        for region in nonprogress:
            spoiler_log += "  " + region + "\n"
        spoiler_log += "\n\n"

        # Write progression spheres.
        spoiler_log += "Playthrough:\n"
        progression_spheres = self.logic.calculate_playthrough_progression_spheres()
        all_progression_sphere_locations = [
            loc for locs in progression_spheres for loc in locs
        ]
        zones, max_location_name_length = self.get_zones_and_max_location_name_len(
            all_progression_sphere_locations
        )
        format_string = "      %-" + str(max_location_name_length + 1) + "s %s\n"
        for i, progression_sphere in enumerate(progression_spheres):
            # skip single gratitude crystals
            progression_sphere = [
                loc
                for loc in progression_sphere
                if loc == "Past - Demise"
                or self.logic.placement.locations[loc] != "Gratitude Crystal"
            ]
            spoiler_log += "%d:\n" % (i + 1)

            for zone_name, locations_in_zone in zones.items():
                if not any(
                    loc for (loc, _) in locations_in_zone if loc in progression_sphere
                ):
                    # No locations in this zone are used in this sphere.
                    continue

                spoiler_log += "  %s:\n" % zone_name

                for (location_name, specific_location_name) in locations_in_zone:
                    if location_name in progression_sphere:
                        if location_name == "Past - Demise":
                            item_name = "Defeat Demise"
                        else:
                            item_name = self.logic.placement.locations[location_name]
                        spoiler_log += format_string % (
                            specific_location_name + ":",
                            item_name,
                        )

        spoiler_log += "\n\n\n"

        # Write item locations.
        spoiler_log += "All item locations:\n"
        zones, max_location_name_length = self.get_zones_and_max_location_name_len(
            self.logic.placement.locations
        )
        format_string = "    %-" + str(max_location_name_length + 1) + "s %s\n"
        for zone_name in sorted(zones):
            locations_in_zone = zones[zone_name]
            spoiler_log += zone_name + ":\n"

            for (location_name, specific_location_name) in locations_in_zone:
                item_name = self.logic.placement.locations[location_name]
                # skip single gratitude crystals, since they are forced vanilla
                if item_name == "Gratitude Crystal":
                    continue
                spoiler_log += format_string % (specific_location_name + ":", item_name)

        spoiler_log += "\n\n\n"

        # Write dungeon/secret cave entrances.
        spoiler_log += "Entrances:\n"
        for (
            entrance_name,
            dungeon_or_cave_name,
        ) in self.logic.randomized_dungeon_entrance.items():
            spoiler_log += "  %-48s %s\n" % (entrance_name + ":", dungeon_or_cave_name)

        spoiler_log += "\n\n"

        # Write randomized trials
        spoiler_log += "Trial Gates:\n"
        for trial_gate, trial in self.logic.randomized_trial_entrance.items():
            spoiler_log += "  %-48s %s\n" % (trial_gate + ":", trial)

        spoiler_log += "\n\n\n"

        # Write hints
        spoiler_log += "Hints:\n"
        for hintlocation, hint in self.hints.hints.items():
            spoiler_log += "  %-53s %s\n" % (
                hintlocation + ":",
                hint.to_spoiler_log_text(),
            )

        spoiler_log += "\n\n\n"

        spoiler_log_output_path = self.log_file_path / (
            "SS Random %s - Spoiler Log.txt" % self.seed
        )
        with spoiler_log_output_path.open("w") as f:
            f.write(spoiler_log)

    def write_spoiler_log_json(self):
        spoiler_log = self.get_log_header_json()
        if self.no_logs:
            # We still calculate progression spheres even if we're not going to write them anywhere to catch more errors in testing.
            self.logic.calculate_playthrough_progression_spheres()

            spoiler_log_output_path = self.log_file_path / (
                "SS Random %s - Anti Spoiler Log.json" % self.seed
            )
            with spoiler_log_output_path.open("w") as f:
                json.dump(spoiler_log, f, indent=2)

            return
        spoiler_log["starting-items"] = sorted(self.logic.placement.starting_items)
        spoiler_log["required-dungeons"] = self.logic.required_dungeons
        spoiler_log["sots-locations"] = [
            self.logic.placement.items[item] for item in self.logic.get_sots_items()
        ]
        spoiler_log["barren-regions"] = self.logic.get_barren_regions()[0]
        spoiler_log[
            "playthrough"
        ] = self.logic.calculate_playthrough_progression_spheres()
        spoiler_log["item-locations"] = self.logic.placement.items
        spoiler_log["hints"] = dict(
            map(
                lambda kv: (kv[0], kv[1].to_spoiler_log_json()),
                self.hints.hints.items(),
            )
        )
        spoiler_log["entrances"] = self.logic.randomized_dungeon_entrance
        spoiler_log["trial-connections"] = self.logic.randomized_trial_entrance

        spoiler_log_output_path = self.log_file_path / (
            "SS Random %s - Spoiler Log.json" % self.seed
        )
        with spoiler_log_output_path.open("w") as f:
            json.dump(spoiler_log, f, indent=2)

    def get_log_header_json(self):
        header_dict = OrderedDict()
        header_dict["version"] = VERSION
        header_dict["permalink"] = self.options.get_permalink()
        header_dict["seed"] = self.seed
        header_dict["hash"] = self.randomizer_hash
        non_disabled_options = [
            (name, val)
            for (name, val) in self.options.options.items()
            if (
                self.options[name] not in [False, [], {}, OrderedDict()]
                or OPTIONS[name]["type"] == "int"
            )
        ]
        header_dict["options"] = OrderedDict(
            filter(
                lambda tupl: OPTIONS[tupl[0]].get("permalink", True),
                non_disabled_options,
            )
        )
        header_dict["cosmetic-options"] = OrderedDict(
            filter(
                lambda tupl: OPTIONS[tupl[0]].get("cosmetic", False),
                non_disabled_options,
            )
        )
        return header_dict

    def get_log_header(self):
        header = ""

        header += "Skyward Sword Randomizer Version %s\n" % VERSION

        header += "Permalink: %s\n" % self.options.get_permalink()

        header += "Seed: %s\n" % self.seed

        header += "Hash : %s\n" % self.randomizer_hash

        header += "Options selected:\n"
        non_disabled_options = [
            (name, val)
            for (name, val) in self.options.options.items()
            if (
                self.options[name] not in [False, [], {}, OrderedDict()]
                or OPTIONS[name]["type"] == "int"
            )
        ]

        def format_opts(opts):
            option_strings = []
            for option_name, option_value in opts:
                if isinstance(option_value, bool):
                    option_strings.append("  %s" % option_name)
                else:
                    option_strings.append("  %s: %s" % (option_name, option_value))
            return "\n".join(option_strings)

        header += format_opts(
            filter(
                lambda tupl: OPTIONS[tupl[0]].get("permalink", True),
                non_disabled_options,
            )
        )
        cosmetic_options = list(
            filter(
                lambda tupl: OPTIONS[tupl[0]].get("cosmetic", False),
                non_disabled_options,
            )
        )
        if cosmetic_options:
            header += "\n\nCosmetic Options:\n"
            header += format_opts(cosmetic_options)

        return header

    def get_zones_and_max_location_name_len(self, locations):
        zones = OrderedDict()
        max_location_name_length = 0
        for location_name in locations:
            zone_name, specific_location_name = (
                location_name.split(" - ", 1)
                if " - " in location_name
                else ("", location_name)
            )

            if zone_name not in zones:
                zones[zone_name] = []
            zones[zone_name].append((location_name, specific_location_name))

            if len(specific_location_name) > max_location_name_length:
                max_location_name_length = len(specific_location_name)

        return (zones, max_location_name_length)

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
                if item in self.logic.get_useful_items():
                    useful_text = "You might need what it reveals..."
                    # print(f'{item} in {trial_check} is useful')
                else:
                    useful_text = "It's probably not too important..."
                    # print(f'{item} in {trial_check} is not useful')
            elif hint_mode == "Advanced":
                if item in self.logic.get_sots_items():
                    useful_text = "Your spirit will grow by completing this trial"
                elif item in self.logic.get_useful_items():
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

        def norm(s):
            if s in ALL_ITEM_NAMES:
                return strip_item_number(s)
            if s in self.areas.checks:
                check = self.areas.checks[s]
                if (override := check.get("text")) is not None:
                    return override
                return check["short_name"]
            if s in self.areas.gossip_stones:
                return self.areas.gossip_stones[s]["short_name"]
            raise ValueError(f"Can't find a shortname for {s}")

        plcmt_file.gossip_stone_hints = dict(
            (k, v.to_gossip_stone_text(norm)) for (k, v) in self.hints.hints.items()
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
