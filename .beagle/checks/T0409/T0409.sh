#!/bin/bash
# T0409: the locked-test done_when offer is checked against already-passes
set -e
T=tests/test_beagle_example_extension.py
F=examples/extensions/beagle.py
bash .beagle/checks/fix/named_tests.sh $T 3 test_locked_test_offer_does_not_name_a_locked_test_that_already_passes test_locked_test_offer_still_names_a_locked_test_that_fails test_driver_edit_refusal_offers_a_step_pursuit_step_accepts
uv run pytest -q $T
uv run ruff check $F $T
