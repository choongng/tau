#!/bin/bash
# T0488: founding declares beagle's [contract], adds its criterion, and seeds Contract and Second extraction ahead of the milestones.
set -e
T=tests/test_beagle_example_extension.py
F=examples/extensions/beagle.py
bash .beagle/checks/fix/named_tests.sh $T 2 \
  test_founding_declares_the_contract_and_seeds_it_first \
  test_founding_drops_a_known_answers_milestone_for_the_contract
mkdir -p "$HOME/.cache/tau-pytest"
timeout 900 uv run --no-sync --with pytest-xdist pytest -q -p no:cacheprovider -n auto \
  --basetemp="$HOME/.cache/tau-pytest/T0488" $T 2>&1 | tail -1 | grep -E '^[0-9]+ passed in'
uv run --no-sync ruff check $F $T
uv run --no-sync ruff format --check $F $T
