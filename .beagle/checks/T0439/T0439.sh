#!/bin/bash
# T0439: an infeasible close that seals its parent says so
set -e
T=tests/test_beagle_example_extension.py
F=examples/extensions/beagle.py
bash .beagle/checks/fix/named_tests.sh $T 3 test_infeasible_close_that_seals_the_parent_says_so test_infeasible_offer_warns_it_would_seal_the_parent test_stop_hook_does_not_offer_pursuit_plan_for_a_sealed_container
uv run pytest -q $T
uv run ruff check $F $T
