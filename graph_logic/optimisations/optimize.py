from functools import cache

from graph_logic.constants import *
from graph_logic.inventory import Inventory, EXTENDED_ITEM
from graph_logic.logic import Logic, LogicSettings, Placement
from graph_logic.logic_expression import DNFInventory
from graph_logic.logic_input import Areas
from graph_logic.placements import SINGLE_CRYSTAL_PLACEMENT
from paths import RANDO_ROOT_PATH


def init_placement(areas, loop_dungeons_trials=True):
    norm = areas.short_to_full
    dungeon_entrances = [
        norm(e)
        for k in ALL_DUNGEONS
        for e in DUNGEON_ENTRANCE_EXITS[DUNGEON_OVERWORLD_ENTRANCES[k]]
    ]
    dungeons = [norm(e) for k in ALL_DUNGEONS for e in DUNGEON_EXITS[k]]

    trial_entrances = [
        norm(TRIAL_GATE_EXITS[SILENT_REALM_GATES[k]]) for k in ALL_SILENT_REALMS
    ]
    trials = [norm(SILENT_REALM_EXITS[k]) for k in ALL_SILENT_REALMS]

    vanilla_map_transitions = {}
    vanilla_reverse_map_transitions = {}
    for exit, v in areas.map_exits.items():
        if exit in dungeon_entrances + dungeons + trial_entrances + trials:
            continue
        if v["type"] == "entrance" or v.get("disabled", False) or "vanilla" not in v:
            continue
        entrance = areas.short_to_full(v["vanilla"])
        vanilla_map_transitions[exit] = entrance
        vanilla_reverse_map_transitions[entrance] = exit

    placement = Placement(
        map_transitions=vanilla_map_transitions,
        reverse_map_transitions=vanilla_reverse_map_transitions,
    )

    if loop_dungeons_trials:
        vanilla_map_transitions = {}
        vanilla_reverse_map_transitions = {}
        for exit in dungeon_entrances + trial_entrances:
            if "Harbour" in exit:
                entrance = norm("Sand Sea - Sandship Dock Entrance")
            else:
                entrance = entrance_of_exit(exit)
            vanilla_map_transitions[exit] = entrance
            vanilla_reverse_map_transitions[entrance] = exit

        placement |= Placement(
            map_transitions=vanilla_map_transitions,
            reverse_map_transitions=vanilla_reverse_map_transitions,
        )

    placement |= SINGLE_CRYSTAL_PLACEMENT(norm, areas.checks)
    return placement


def init_logic(areas, placement):
    logic_settings = LogicSettings(Inventory(), Inventory(), {}, [])

    return Logic(areas, logic_settings, placement, optim=False)


def optimize(logic: Logic):
    item_repr = EXTENDED_ITEM.__repr__
    inv_repr = Inventory.__repr__
    dnfinv_repr = DNFInventory.__repr__
    EXTENDED_ITEM.__repr__ = lambda self: int.__repr__(self)
    Inventory.__repr__ = lambda self: f"{list(self.intset)!r}"
    DNFInventory.__repr__ = lambda self: f"{list(self.disjunction)!r}"

    with open(
        RANDO_ROOT_PATH / "graph_logic" / "optimisations" / "requirements.json",
        mode="w",
    ) as f:
        f.write(
            "[\n"
            + ",\n".join(
                f"{req!r}"
                if isinstance(req, DNFInventory) and not req.opaque
                else r"{}"
                for i, req in enumerate(logic.requirements)
            )
            + "]"
        )

    EXTENDED_ITEM.__repr__ = item_repr
    Inventory.__repr__ = inv_repr
    DNFInventory.__repr__ = dnfinv_repr


from yaml_files import graph_requirements, checks, hints, map_exits


def main():
    areas = Areas(graph_requirements, checks, hints, map_exits)
    placement = init_placement(areas)
    logic = init_logic(areas, placement)
    optimize(logic)


def print_EXTENDED_ITEM():
    _ = Areas(graph_requirements, checks, hints, map_exits)
    with open(
        RANDO_ROOT_PATH / "graph_logic" / "optimisations" / "EXTENDED_ITEM.txt",
        mode="w",
    ) as f:
        f.write("".join(str(i) + "\n" for i in EXTENDED_ITEM.items()))


def post_optimize():
    areas = Areas(graph_requirements, checks, hints, map_exits)
    with open(
        RANDO_ROOT_PATH / "graph_logic" / "optimisations" / "requirements_out.txt"
    ) as f:
        requirements = eval(f.read())

    for i, e in enumerate(requirements):
        if e is None:
            requirements[i] = areas.requirements[i]

    useful0 = Logic.aggregate_requirements(areas.requirements, None)
    useful1 = Logic.aggregate_requirements(requirements, None)
    become_useless = useful0.intset - useful1.intset
    for v in areas.checks.values():
        become_useless.discard(v["req_index"])
    become_useless.discard(
        EXTENDED_ITEM[make_day(areas.short_to_full("Skyloft - Near Temple Entrance"))]
    )
    become_useless.discard(
        EXTENDED_ITEM[make_day(areas.short_to_full("Skyloft - Central"))]
    )

    impossible = DNFInventory()
    for i in become_useless:
        print(str(i))
        requirements[i] = impossible

    Logic.deep_simplify(requirements)

    useful2 = Logic.aggregate_requirements(requirements, None)
    become_useless = useful1.intset - useful2.intset
    for v in areas.checks.values():
        become_useless.discard(v["req_index"])
    become_useless.discard(
        EXTENDED_ITEM[make_day(areas.short_to_full("Skyloft - Near Temple Entrance"))]
    )
    become_useless.discard(
        EXTENDED_ITEM[make_day(areas.short_to_full("Skyloft - Central"))]
    )
    for i in become_useless:
        print(str(i))
        requirements[i] = impossible

    with open(
        RANDO_ROOT_PATH / "graph_logic" / "optimisations" / "requirements_out2.txt",
        mode="w",
    ) as f:
        f.write("[\n" + ",\n".join(f"{req!r}" for req in requirements) + "]")


@cache
def get_requirements():
    with open(
        RANDO_ROOT_PATH / "graph_logic" / "optimisations" / "requirements_out2.txt"
    ) as f:
        return eval(f.read())


if __name__ == "__main__":
    main()
