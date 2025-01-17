from collections import OrderedDict
from typing import TextIO
from logic.logic import Placement
from logic.constants import *
from logic.logic_input import Areas
from hints.hint_types import GossipStoneHintWrapper
from options import OPTIONS, Options
import itertools

from version import VERSION


def remove_prefix(region, location):
    t = location.split(sep, 1)
    if len(t) == 1:
        return location
    prefix, loc = t
    if prefix == region:
        return loc
    if region == UPPER_SKYLOFT and prefix in ["Knight Academy", "Skyloft"]:
        return loc
    if region in [CENTRAL_SKYLOFT, SKYLOFT_VILLAGE] and prefix == "Skyloft":
        return loc
    return location


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
    randomized_entrances,
):
    write_header(file, options, hash)
    norm = areas.prettify

    if options["no-spoiler-log"]:
        return

    if len(placement.starting_items) > 0:
        file.write("\n\nStarting items:\n  ")
        file.write("\n  ".join(sorted(placement.starting_items)))
    file.write("\n\n\n")

    # Write required dungeons.
    for i, dungeon in enumerate(required_dungeons, start=1):
        file.write(f"Required Dungeon {i}: {dungeon}\n")

    file.write("\n\n")

    # Write spirit of the sword (100% required) locations.
    file.write("SotS:\n")

    sorted_regions = ["Past"] + list(ALL_HINT_REGIONS)
    sorted_checks = [START_ITEM, UNPLACED_ITEM, DEMISE] + list(areas.checks)

    sots_locations = {
        goal: sorted(
            ((norm(placement.items[item]), item) for item in items),
            key=lambda c: sorted_checks.index(placement.items[c[1]]),
        )
        for goal, items in sots_items.items()
    }

    max_location_name_length = 2 + max(
        (len(loc) for goal_locs in sots_locations.values() for loc, _ in goal_locs),
        default=0,
    )

    for loc, item in sots_locations[DEMISE]:
        file.write(f"  {loc + ':':{max_location_name_length}} {item}\n")

    file.write("\n\n")

    # Write path locations; locations 100% required to complete a given required dungeon.
    file.write("Path:\n")
    for dungeon in required_dungeons:
        goal = DUNGEON_GOALS[dungeon]
        file.write(f"{goal}:\n")
        for loc, item in sots_locations[goal]:
            file.write(f"  {loc + ':':{max_location_name_length}} {item}\n")

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
    # First pass for the lengths.
    for sphere in progression_spheres:
        pretty_sphere = []
        for loc in sphere:
            if loc == DEMISE:
                pretty_sphere.append(("Past", DEMISE, "End Credits"))
            elif norm(item := placement.locations[loc]) != GRATITUDE_CRYSTAL:
                hint_region = areas.checks[loc]["hint_region"]
                pretty_sphere.append((hint_region, loc, item))
        pretty_sphere.sort(
            key=lambda check: (
                sorted_regions.index(check[0]),
                sorted_checks.index(check[1]),
            ),
        )
        prettified_spheres.append(
            [
                (reg, remove_prefix(reg, norm(loc)), item)
                for (reg, loc, item) in pretty_sphere
            ],
        )

    max_location_name_length = 2 + max(
        (len(loc) for sphere in prettified_spheres for _, loc, _ in sphere), default=0
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
        (areas.checks[loc]["hint_region"], loc, item)
        for loc, item in placement.locations.items()
        if norm(item) != GRATITUDE_CRYSTAL
    ]

    with_regions.sort(
        key=lambda check: (
            sorted_regions.index(check[0]),
            sorted_checks.index(check[1]),
        )
    )

    with_regions = [
        (reg, remove_prefix(reg, norm(loc)), item) for (reg, loc, item) in with_regions
    ]

    max_location_name_length = 1 + max(
        (len(loc) for _, loc, _ in with_regions), default=0
    )

    for zone_name, locations_in_zone in itertools.groupby(with_regions, lambda x: x[0]):
        file.write(zone_name + ":\n")
        for _, loc, item in locations_in_zone:
            file.write(f"    {loc + ':':{max_location_name_length}} {item}\n")

    file.write("\n\n\n")

    # Write entrances.
    file.write("Entrances:\n")

    # Write down exits.
    sorted_checks = list(areas.map_exits)
    sorted_randomized_entrances = sorted(
        randomized_entrances.items(), key=lambda c: sorted_checks.index(c[0])
    )
    prettified_randomized_entrances = [
        (norm(exit_name), norm(entrance_name))
        for exit_name, entrance_name in sorted_randomized_entrances
    ]
    max_exit_name_length = 1 + max(
        len(loc) for loc, _ in prettified_randomized_entrances
    )

    # Write starting entrance.
    file.write("  Starting Entrance:\n")
    file.write(f"    {norm(randomized_entrances[areas.short_to_full(START)])}\n\n")

    # Write dungeon entrances.
    file.write("  Dungeon Entrances:\n")
    for dungeon in ALL_DUNGEONS:
        entrance_name = DUNGEON_OVERWORLD_ENTRANCES[dungeon]
        exit_to = areas.short_to_full(DUNGEON_ENTRANCE_EXITS[entrance_name][0])
        associated_entrance = norm(randomized_entrances[exit_to])
        file.write(f"    {entrance_name+':':48} {associated_entrance}\n")

    file.write("\n\n")

    # Write randomized trial gates.
    file.write("Trial Gates:\n")
    for realm in ALL_SILENT_REALMS:
        trial_gate = SILENT_REALM_GATES[realm]
        gate_exit = areas.short_to_full(TRIAL_GATE_EXITS[trial_gate])
        associated_entrance = norm(randomized_entrances[gate_exit])
        file.write(f"  {trial_gate+':':48} {associated_entrance}\n")

    file.write("\n\n")

    file.write("Exits:\n")
    for exit_name, entrance_name in prettified_randomized_entrances:
        file.write(f"  {exit_name + ':':{max_exit_name_length}} {entrance_name}\n")

    file.write("\n\n\n")

    # Write hints.
    file.write("Hints:\n")

    max_hintstone_name_length = 2 + max(
        (
            len(norm(hintloc))
            for hintloc, hint_stone in hints.items()
            if not isinstance(hint_stone, GossipStoneHintWrapper)
        ),
        default=0,
    )

    for hintloc, hint_stone in hints.items():
        if isinstance(hint_stone, GossipStoneHintWrapper):
            file.write(f"  {norm(hintloc)+':'}\n")
            for hint in hint_stone.hints:
                file.write(f"        {hint.to_spoiler_log_text(norm)}\n")
        else:
            file.write(
                f"  {norm(hintloc) + ':':{max_hintstone_name_length}} {hint_stone.to_spoiler_log_text(norm)}\n"
            )

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
    randomized_entrances,
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
    spoiler_log["entrances"] = randomized_entrances
    return spoiler_log


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
