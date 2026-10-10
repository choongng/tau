#!/bin/bash
# R42 fix: a task that wrote no cases data is not judged as known answers
set -e
T=tests/test_beagle_example_extension.py
bash .beagle/checks/fix/named_tests.sh $T 2 test_close_does_not_lock_docs_and_test_of_a_task_that_wrote_no_cases test_unread_cases_skips_a_test_importing_no_project_code_for_earlier_locked_data
uv run pytest -q $T 
uv run ruff check examples/extensions/beagle.py $T
