#!/bin/bash
# T0410: the spawn-limit offer for a task not open is one tau accepts
set -e
T=tests/test_beagle_example_extension.py
F=examples/extensions/beagle.py
bash .beagle/checks/fix/named_tests.sh $T 2 test_spawn_refused_at_the_limit_for_a_blocked_task_offers_no_infeasible_close test_spawn_limit_offer_for_an_open_task_still_offers_the_infeasible_close
uv run pytest -q $T
uv run ruff check $F $T
