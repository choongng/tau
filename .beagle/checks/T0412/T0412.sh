#!/bin/bash
# T0412: the bool-exit refusal is tested on every route and says what it cannot know
set -e
T=tests/test_beagle_example_extension.py
F=examples/extensions/beagle.py
bash .beagle/checks/fix/named_tests.sh $T 3 test_bool_exit_check_refused_on_the_amend_route test_bool_exit_check_refused_on_the_new_route test_bool_exit_refusal_does_not_say_a_failure_condition_passes_bad_work
uv run pytest -q $T
uv run ruff check $F $T
