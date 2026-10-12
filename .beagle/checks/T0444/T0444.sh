#!/bin/bash
# T0444: a locked cases test no code can pass is refused at the close
set -e
T=tests/test_beagle_example_extension.py
F=examples/extensions/beagle.py
bash .beagle/checks/fix/named_tests.sh $T 3 test_cases_test_problem_refuses_cases_the_test_cannot_tell_apart test_method_and_value_follows_an_attribute_into_a_dict test_locked_files_brief_says_to_report_an_unpassable_locked_test
uv run pytest -q $T
uv run ruff check $F $T
