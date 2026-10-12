#!/bin/bash
# T0445: worker read guards let a known-answers worker read and search the references once
set -e
T=tests/test_beagle_example_extension.py
F=examples/extensions/beagle.py
bash .beagle/checks/fix/named_tests.sh $T 3 test_known_answers_worker_ranged_reference_read_is_not_refused test_reference_search_offered_by_a_read_refusal_is_not_refused test_nth_reread_of_a_reference_window_is_still_refused
uv run pytest -q $T
uv run ruff check $F $T
