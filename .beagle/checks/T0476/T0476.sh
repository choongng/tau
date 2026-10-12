#!/bin/bash
# T0476: the seat guard offers a new route for an out-of-scope fix (R60)
set -e
T=tests/test_beagle_example_extension.py
F=examples/extensions/beagle.py
bash .beagle/checks/fix/named_tests.sh $T 1 test_seat_guard_refusal_outside_the_open_task_scope_offers_a_new_route
uv run pytest -q $T
uv run ruff check $F $T
