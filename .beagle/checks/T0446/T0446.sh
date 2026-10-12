#!/bin/bash
# T0446: a killed worker's last words reach the driver and a new route
set -e
T=tests/test_beagle_example_extension.py
F=examples/extensions/beagle.py
bash .beagle/checks/fix/named_tests.sh $T 2 test_wall_kill_step_result_shows_the_killed_workers_last_words test_new_route_carries_killed_progress_to_the_sibling
uv run pytest -q $T
uv run ruff check $F $T
