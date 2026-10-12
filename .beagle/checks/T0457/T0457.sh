#!/bin/bash
# T0457: prove witness outside scope does not pre-empt own-file absence; retry asks no out-of-scope write (R54)
set -e
T=tests/test_beagle_example_extension.py
F=examples/extensions/beagle.py
bash .beagle/checks/fix/named_tests.sh $T 2 test_prove_witness_outside_scope_does_not_preempt_absence_of_the_tasks_own_file test_not_proven_retry_does_not_ask_for_a_test_when_scope_has_none
uv run pytest -q $T
uv run ruff check $F $T
