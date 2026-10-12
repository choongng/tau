#!/bin/bash
# T0473: the locked-data route does not repeat a scoped test (R59)
set -e
T=tests/test_beagle_example_extension.py
F=examples/extensions/beagle.py
bash .beagle/checks/fix/named_tests.sh $T 1 test_cases_first_locked_data_route_does_not_repeat_a_scoped_test
uv run pytest -q $T
uv run ruff check $F $T
