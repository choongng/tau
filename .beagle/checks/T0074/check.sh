#!/bin/bash
# T0074: pursuit_plan names uncommitted files in the split task's scope.
set -eu
bash .beagle/checks/fix/named_tests.sh tests/test_beagle_example_extension.py 2 \
  test_plan_names_uncommitted_files_in_the_split_tasks_scope \
  test_plan_says_nothing_of_a_clean_scope
.venv/bin/ruff check examples/extensions/beagle.py tests/test_beagle_example_extension.py
