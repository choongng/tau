#!/bin/bash
# T0408: Cases first checks the spawn limit for a holder that is not open
set -e
T=tests/test_beagle_example_extension.py
F=examples/extensions/beagle.py
bash .beagle/checks/fix/named_tests.sh $T 2 test_cases_first_offers_the_infeasible_close_for_a_holder_at_the_spawn_limit_not_open test_cases_first_still_offers_opening_a_holder_under_the_limit
uv run pytest -q $T
uv run ruff check $F $T
