import sys
import os
from graph_logic.logic_input import Areas

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from ssrando import Randomizer
from options import Options
from graph_logic.placement_file import PlacementFile
from yaml_files import graph_requirements, checks, hints, map_exits


def test_roundtrip():
    areas = Areas(graph_requirements, checks, hints, map_exits)
    opts = Options()
    opts.set_option("dry-run", True)
    for i in range(5):
        opts.set_option("seed", i)
        rando = Randomizer(areas, opts)
        rando.rando.randomize()
        rando.hints.do_hints()
        plcmt_file = rando.get_placement_file()
        round_tripped_file = PlacementFile()
        round_tripped_file.read_from_str(plcmt_file.to_json_str())
        assert plcmt_file.dungeon_connections == round_tripped_file.dungeon_connections
        assert plcmt_file.gossip_stone_hints == round_tripped_file.gossip_stone_hints
        assert plcmt_file.hash_str == round_tripped_file.hash_str
        assert plcmt_file.item_locations == round_tripped_file.item_locations
        assert plcmt_file.options.get_permalink(
            exclude_seed=True
        ) == round_tripped_file.options.get_permalink(exclude_seed=True)
        assert plcmt_file.required_dungeons == round_tripped_file.required_dungeons
        assert plcmt_file.starting_items == round_tripped_file.starting_items
        assert plcmt_file.trial_hints == round_tripped_file.trial_hints
        assert plcmt_file.version == round_tripped_file.version
