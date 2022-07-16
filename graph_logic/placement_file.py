from .constants import *
from options import Options
from version import VERSION
from util.file_accessor import read_yaml_file_cached

import json


class InvalidPlacementFile(Exception):
    pass


class PlacementFile:
    def __init__(self):
        self.version = ""
        self.options = Options()
        self.hash_str = ""
        self.starting_items = []
        self.required_dungeons = []
        self.item_locations = {}
        self.gossip_stone_hints = {}
        self.trial_hints = {}
        self.dungeon_connections = {}
        self.trial_connections = {}

    def read_from_file(self, f):
        self._read_from_json(json.load(f))

    def read_from_str(self, s):
        self._read_from_json(json.loads(s))

    def to_json_str(self):
        retval = {
            "version": self.version,
            "permalink": self.options.get_permalink(exclude_seed=True),
            "hash": self.hash_str,
            "starting-items": self.starting_items,
            "required-dungeons": self.required_dungeons,
            "item-locations": self.item_locations,
            "gossip-stone-hints": self.gossip_stone_hints,
            "trial-hints": self.trial_hints,
            "entrance-connections": self.dungeon_connections,
            "trial-connections": self.trial_connections,
        }
        return json.dumps(retval, indent=2)

    def _read_from_json(self, jsn):
        self.version = jsn["version"]
        self.options.update_from_permalink(jsn["permalink"])
        self.options.set_option("seed", -1)
        self.hash_str = jsn["hash"]
        self.starting_items = jsn["starting-items"]
        self.required_dungeons = jsn["required-dungeons"]
        self.item_locations = jsn["item-locations"]
        self.gossip_stone_hints = jsn["gossip-stone-hints"]
        self.trial_hints = jsn["trial-hints"]
        self.dungeon_connections = jsn["entrance-connections"]
        self.trial_connections = jsn["trial-connections"]

    def check_valid(self):
        """checks, if the current state is valid, throws an exception otherwise
        This does not check consistency with all the settings"""
        if VERSION != self.version:
            raise InvalidPlacementFile(
                f"Version did not match, requires {self.version} but found {VERSION}"
            )

        ALLOWED_STARTING_ITEMS = (
            dict.fromkeys((EMERALD_TABLET, AMBER_TABLET, RUBY_TABLET))
            | group(PROGRESSIVE_SWORD, 6)
            | group(PROGRESSIVE_POUCH, 1)
        )
        for item in self.starting_items:
            if item not in ALLOWED_STARTING_ITEMS:
                raise InvalidPlacementFile(f"Invalid starting item {item} !")

        for req_dungeon in self.required_dungeons:
            if req_dungeon not in REGULAR_DUNGEONS:
                raise InvalidPlacementFile(
                    f"{req_dungeon} is not a valid required dungeon!"
                )

        if sorted(self.dungeon_connections.keys()) != sorted(ALL_DUNGEONS):
            raise InvalidPlacementFile("dungeon dungeon_connections are wrong!")

        if sorted(self.dungeon_connections.values()) != sorted(ALL_DUNGEONS):
            raise InvalidPlacementFile("dungeon entries are wrong!")

        for item in self.item_locations.values():
            if item not in ALL_ITEM_NAMES:
                raise InvalidPlacementFile(f'invalid item "{item}"')

        checks_file = read_yaml_file_cached("checks.yaml")
        check_sets_equal(
            set(
                k
                for (k, v) in checks_file.items()
                if v["original item"] != "Gratitude Crystal"
            ),
            set(self.item_locations.keys()),
            "Checks",
        )
        # WRONG: Now long names here

        hint_file = read_yaml_file_cached("hints.yaml")
        check_sets_equal(
            set(hint_file.keys()),
            set(self.gossip_stone_hints.keys()),
            "Gossip Stone Hints",
        )
        # WRONG: Now long names here

        for hintlist in self.gossip_stone_hints.values():
            if not isinstance(hintlist, list):
                raise InvalidPlacementFile(
                    "gossip stone hints need to be LISTS of strings!"
                )
            for hint in hintlist:
                if not isinstance(hint, str):
                    raise InvalidPlacementFile(
                        "gossip stone hints need to be lists of STRINGS!"
                    )

        trial_check_names = set(
            (
                "Song of the Hero - Trial Hint",
                "Farore's Courage - Trial Hint",
                "Nayru's Wisdom - Trial Hint",
                "Din's Power - Trial Hint",
            )
        )

        check_sets_equal(trial_check_names, set(self.trial_hints.keys()), "Trial Hints")
        # WRONG: Not done


def check_sets_equal(orig: set, actual: set, name: str):
    if orig != actual:
        additional = actual - orig
        missing = orig - actual
        error_msg = ""
        if additional:
            error_msg += f"Additional {name}:\n"
            error_msg += ", ".join(additional) + "\n"
        if missing:
            error_msg += f"Missing {name}:\n"
            error_msg += ", ".join(missing) + "\n"
        raise InvalidPlacementFile(error_msg)
