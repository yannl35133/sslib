#!/bin/sh
set -e

echo "Export"
python -c "from graph_logic.optimisations.optimize import *; main()" > /dev/null

echo "OCaml simplifications"
(cd graph_logic/optimisations; dune exec ./logic.exe > /dev/null)

echo "Python further simplifications"
python -c "from graph_logic.optimisations.optimize import *; post_optimize()" > /dev/null
