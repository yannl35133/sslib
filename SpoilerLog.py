from collections import OrderedDict
from typing import TextIO
from graph_logic.logic import Placement
from graph_logic.constants import *
from graph_logic.logic_input import Areas
from options import OPTIONS, Options
import itertools

from version import VERSION


def write(
    file: TextIO,
    placement: Placement,
    options: Options,
    areas: Areas,
    *,
    hash,
    progression_spheres,
    hints,
    required_dungeons,
    sots_items,
    barren_nonprogress,
    randomized_dungeon_entrance,
    randomized_trial_entrance,
):
    write_header(file, options, hash)
    norm = areas.prettify

    if options["no-spoiler-log"]:
        return

    if len(placement.starting_items) > 0:
        file.write("\n\nStarting items:\n  ")
        file.write("\n  ".join(placement.starting_items))
    file.write("\n\n\n")

    # Write required dungeons
    for i, dungeon in enumerate(required_dungeons, start=1):
        file.write(f"Required Dungeon {i}: {dungeon}\n")

    file.write("\n\n")

    # Write way of the hero (100% required) locations
    file.write("SotS:\n")
    for item in sots_items[DEMISE]:
        location = placement.items[item]
        location = norm(location) + ":"
        file.write(f"  {location:53} {item}\n")

    file.write("\n\n")

    # Write path locations; locations 100% required to complete a given required dungeon
    file.write("Path:\n")
    for dungeon in required_dungeons:
        goal = DUNGEON_GOALS[dungeon]
        file.write(f"{goal}:\n")
        for item in sots_items[goal]:
            location = placement.items[item]
            location = norm(location) + ":"
            file.write(f"  {location:53} {item}\n")

    file.write("\n\n")

    barren, nonprogress = barren_nonprogress
    file.write("Barren Regions:\n")
    for region in barren:
        file.write("  " + region + "\n")
    file.write("\n\n")

    file.write("Nonprogress Regions:\n")
    for region in nonprogress:
        file.write("  " + region + "\n")
    file.write("\n\n")

    # Write progression spheres.
    file.write("Playthrough:\n")
    prettified_spheres = []
    # First pass for the lengths
    for sphere in progression_spheres:
        pretty_sphere = []
        for loc in sphere:
            if loc == DEMISE:
                pretty_sphere.append(("Past", "Demise", DEMISE))
            elif (item := norm(placement.locations[loc])) != GRATITUDE_CRYSTAL:
                pretty_sphere.append(
                    (areas.checks[loc]["hint_region"], norm(loc), item)
                )
        prettified_spheres.append(sorted(pretty_sphere))

    max_location_name_length = 1 + max(
        len(loc[1]) for sphere in prettified_spheres for loc in sphere
    )

    for i, progression_sphere in enumerate(prettified_spheres, start=1):
        file.write(f"{i}\n")

        for zone_name, locations_in_zone in itertools.groupby(
            progression_sphere, lambda x: x[0]
        ):
            file.write(f"  {zone_name}:\n")

            for _, loc, item in locations_in_zone:
                file.write(f"      {loc + ':':{max_location_name_length}} {item}\n")

    file.write("\n\n\n")

    # Write item locations.
    file.write("All item locations:\n")

    with_regions = [
        (areas.checks[loc]["hint_region"], norm(loc), item)
        for loc, item in placement.locations.items()
        if norm(item) != GRATITUDE_CRYSTAL
    ]
    with_regions.sort()

    max_location_name_length = 1 + max(
        len(loc[1]) for sphere in prettified_spheres for loc in sphere
    )

    for zone_name, locations_in_zone in itertools.groupby(with_regions, lambda x: x[0]):
        file.write(zone_name + ":\n")
        for _, loc, item in locations_in_zone:
            file.write(f"    {loc + ':':{max_location_name_length}} {item}\n")

    file.write("\n\n\n")

    # Write dungeon/secret cave entrances.
    file.write("Entrances:\n")
    for (
        entrance_name,
        dungeon,
    ) in randomized_dungeon_entrance.items():
        file.write(f"  {entrance_name+':':48} {dungeon}\n")

    file.write("\n\n")

    # Write randomized trials
    file.write("Trial Gates:\n")
    for trial_gate, trial in randomized_trial_entrance.items():
        file.write(f"  {trial_gate+':':48} {trial}\n")

    file.write("\n\n\n")

    # Write hints
    file.write("Hints:\n")
    for hintloc, hint in hints.items():
        file.write(f"  {norm(hintloc)+':':53} {hint.to_spoiler_log_text()}\n")

    file.write("\n\n\n")


def dump_json(
    placement: Placement,
    options: Options,
    *,
    hash,
    progression_spheres,
    hints,
    required_dungeons,
    sots_items,
    barren_nonprogress,
    randomized_dungeon_entrance,
    randomized_trial_entrance,
):
    spoiler_log = dump_header_json(options, hash)
    if options["no-spoiler-log"]:
        return spoiler_log
    spoiler_log["starting-items"] = sorted(placement.starting_items)
    spoiler_log["required-dungeons"] = required_dungeons
    spoiler_log["sots-locations"] = [
        placement.items[item] for item in sots_items[DEMISE]
    ]
    spoiler_log["barren-regions"] = barren_nonprogress[0]
    spoiler_log["playthrough"] = progression_spheres
    spoiler_log["item-locations"] = placement.items
    spoiler_log["hints"] = {k: v.to_spoiler_log_json() for k, v in hints.items()}
    spoiler_log["entrances"] = randomized_dungeon_entrance
    spoiler_log["trial-connections"] = randomized_trial_entrance


def dump_header_json(options: Options, hash):
    header_dict = OrderedDict()
    header_dict["version"] = VERSION
    header_dict["permalink"] = options.get_permalink()
    header_dict["seed"] = options["seed"]
    header_dict["hash"] = hash
    non_disabled_options = [
        (name, val)
        for (name, val) in options.options.items()
        if (
            options[name] not in [False, [], {}, OrderedDict()]
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


def write_header(file: TextIO, options: Options, hash):

    file.write("Skyward Sword Randomizer Version %s\n" % VERSION)

    file.write("Permalink: %s\n" % options.get_permalink())

    file.write("Seed: %s\n" % options["seed"])

    file.write("Hash : %s\n" % hash)

    file.write("Options selected:\n")
    non_disabled_options = [
        (name, val)
        for (name, val) in options.options.items()
        if (
            options[name] not in [False, [], {}, OrderedDict()]
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

    file.write(
        format_opts(
            filter(
                lambda tupl: OPTIONS[tupl[0]].get("permalink", True),
                non_disabled_options,
            )
        )
    )
    cosmetic_options = list(
        filter(
            lambda tupl: OPTIONS[tupl[0]].get("cosmetic", False),
            non_disabled_options,
        )
    )
    if cosmetic_options:
        file.write("\n\nCosmetic Options:\n")
        file.write(format_opts(cosmetic_options))
