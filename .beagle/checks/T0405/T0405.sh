#!/bin/bash
# T0405: the driver's bash close steer offers abandon only where _abandon_problem would take it
set -e
T=tests/test_beagle_example_extension.py
F=examples/extensions/beagle.py
bash .beagle/checks/fix/named_tests.sh $T 3 test_bash_close_steer_on_a_milestone_offers_no_abandon test_bash_close_steer_offered_call_passes_abandon_problem test_bash_close_steer_without_a_task_offers_only_a_duplicate_drop
uv run pytest -q $T
uv run ruff check $F $T
