from .logic_expression import parse_logic_expression, BaseLogicExpression
from ssrando import RANDO_ROOT_PATH
from options import Options
from .constants import ENTRANCE_CONNECTIONS

import yaml


class LogicExprLoader:
    def __init__(
        self, options, entrance_connections, trial_connections, required_dungeons
    ):
        self.options = options
        self.entrance_connections = entrance_connections
        self.trial_connections = trial_connections
        self.required_dungeons = required_dungeons

    def load_logic(self):
        requirements_file = {
            "BiTless": "SS Rando Logic - Glitchless Requirements.yaml",
            "Glitched": "SS Rando Logic - Glitched Requirements.yaml",
            "No Logic": "SS Rando Logic - Glitched Requirements.yaml",  # TODO: no logic doesn't need requirements
        }[self.options["logic-mode"]]
        with (RANDO_ROOT_PATH / requirements_file).open("r") as f:
            macro_strings = yaml.safe_load(f)
        self.macros = {}
        # base
        for macro_name, req_string in macro_strings.items():
            self.macros[macro_name] = parse_logic_expression(req_string)

        # set option dependant macros
        # Update all the macros to take randomized entrances into account.
        for entrance_name, zone_name in self.entrance_connections.items():
            zone_access_macro_name = "Can Access " + zone_name
            entrance_access_macro_name = "Can Access " + entrance_name
            self.macros[zone_access_macro_name] = BaseLogicExpression(
                entrance_access_macro_name
            )
            # dungeon finishes
            zone_beat_macro_name = "Can Beat " + zone_name
            entrance_beat_macro_name = "Can Beat " + entrance_name
            self.macros[entrance_beat_macro_name] = BaseLogicExpression(
                zone_beat_macro_name
            )

        # trial entrances
        for trial_gate, trial in self.trial_connections.items():
            trial_gate_access_macro = "Can Open " + trial_gate
            trial_access_macro = "Can Access " + trial
            self.macros[trial_access_macro] = BaseLogicExpression(
                trial_gate_access_macro
            )

        # Beat game
        # needs to be able to open GoT and open it, requires required dungeons
        access_past_requirements = [
            "Can Access Sealed Temple",
            "Can Open GOT After Raising",
            "Can Raise Gate of Time",
        ]
        for dungeon in self.required_dungeons:
            access_past_requirements.append(f"Can Beat {dungeon}")
        self.macros["Can Access Past"] = parse_logic_expression(
            " & ".join(access_past_requirements)
        )

        for macro_name, expr in self.macros.items():
            self.macros[macro_name] = expr.simplify(self.options, self.macros)


def test():
    options = Options()
    trial_connections = {
        "Faron Silent Realm": "Trial Gate in Faron Woods",
        "Lanayru Silent Realm": "Trial Gate in Lanayru Desert",
        "Eldin Silent Realm": "Trial Gate in Eldin Volcano",
        "Skyloft Silent Realm": "Trial Gate on Skyloft",
    }
    loader = LogicExprLoader(
        options, ENTRANCE_CONNECTIONS, trial_connections, ["Skyview"]
    )
    loader.load_logic()
    for name, val in loader.macros.items():
        print(name)
        print(str(val))
        print()
