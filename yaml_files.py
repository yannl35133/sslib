import os
from pathlib import Path
import yaml


def yaml_load(file_path: Path):
    with file_path.open("r") as f:
        return yaml.safe_load(f)


ROOT_DIR = Path(__file__).parent

beedle_texts_file = ROOT_DIR / "beedle_texts.yaml"
beedle_texts = yaml_load(beedle_texts_file)

checks_file = ROOT_DIR / "checks.yaml"
checks = yaml_load(checks_file)

eventpatches_file = ROOT_DIR / "eventpatches.yaml"
eventpatches = yaml_load(eventpatches_file)

hints_file = ROOT_DIR / "hints.yaml"
hints = yaml_load(hints_file)

items_file = ROOT_DIR / "items.yaml"
items = yaml_load(items_file)

map_exits_file = ROOT_DIR / "entrances.yaml"
map_exits = yaml_load(map_exits_file)

music_file = ROOT_DIR / "music.yaml"
music = yaml_load(music_file)

options_file = ROOT_DIR / "options.yaml"
options = yaml_load(options_file)

patches_file = ROOT_DIR / "patches.yaml"
patches = yaml_load(patches_file)

glitchless_requirements_file = (
    ROOT_DIR / "SS Rando Logic - Glitchless Requirements.yaml"
)
glitchless_requirements = yaml_load(glitchless_requirements_file)

glitched_requirements_file = ROOT_DIR / "SS Rando Logic - Glitched Requirements.yaml"
glitched_requirements = yaml_load(glitched_requirements_file)


def requirements(folder: Path):
    files = filter(lambda s: s[0].isupper() and s.endswith(".yaml"), os.listdir(folder))
    requirements = {
        os.path.splitext(filename)[0]: yaml_load(folder / filename)
        for filename in files
    } | {"allowed-time-of-day": "Both"}
    requirements["exits"] = {"Start": "Nothing"}
    if "macros.yaml" in os.listdir(folder):
        requirements["macros"] = yaml_load(folder / "macros.yaml")
    return requirements


graph_requirements_folder = ROOT_DIR / "graph_logic" / "requirements"
graph_requirements = requirements(graph_requirements_folder)
