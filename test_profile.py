import cProfile

from ssrando import Randomizer
from options import Options
from logic.placement_file import PlacementFile
from graph_logic.logic_input import Areas

from yaml_files import graph_requirements, checks, hints, map_exits


def do_profile():
    areas = Areas(graph_requirements, checks, hints, map_exits)
    opts = Options()
    opts.set_option("dry-run", True)
    opts.set_option("seed", 0)
    rando = Randomizer(areas, opts)
    cProfile.runctx("rando.logic.randomize_items()", globals=globals(), locals=locals())


do_profile()
