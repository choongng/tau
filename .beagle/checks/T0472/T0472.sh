#!/bin/bash
# T0472: a tests-only task importing an unwritten module is offered a route prove accepts (R59)
set -e
T=tests/test_beagle_example_extension.py
F=examples/extensions/beagle.py
bash .beagle/checks/fix/named_tests.sh $T 1 test_tests_only_task_importing_unwritten_module_is_offered_the_cases_first_route
uv run pytest -q $T
uv run ruff check $F $T
