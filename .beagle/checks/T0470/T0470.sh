#!/bin/bash
# T0470: a new-route successor that ran is not reported as not opened (R58)
set -e
T=tests/test_beagle_example_extension.py
F=examples/extensions/beagle.py
bash .beagle/checks/fix/named_tests.sh $T 1 test_new_route_successor_killed_at_its_wall_is_not_reported_as_not_opened
uv run pytest -q $T
uv run ruff check $F $T
