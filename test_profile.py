import cProfile

from ssrando import Randomizer
from options import Options
from logic.placement_file import PlacementFile


def do_profile():
    opts = Options()
    opts.set_option("dry-run", True)
    opts.set_option("seed", 0)
    rando = Randomizer(opts)
    cProfile.runctx("rando.logic.randomize_items()", globals=globals(), locals=locals())


do_profile()
