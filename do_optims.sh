#!/bin/sh
set -e

python -c "from graph_logic.optimisations.optimize import *; main()" > /dev/null
(cd graph_logic/optimisations; dune exec ./logic.exe > /dev/null)
python -c "from graph_logic.optimisations.optimize import *; post_optimize()" > /dev/null
