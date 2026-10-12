#!/bin/bash
# T0467: a new route held at close sends its notes to a worker (R57)
set -e
T=tests/test_beagle_example_extension.py
F=examples/extensions/beagle.py
bash .beagle/checks/fix/named_tests.sh $T 1 test_new_route_held_at_close_sends_its_notes_to_a_worker
uv run pytest -q $T
uv run ruff check $F $T
