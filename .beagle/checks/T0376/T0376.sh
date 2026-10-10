#!/bin/bash
# R42 fix: an open task's not-run refusal offers no route it then refuses
set -e
T=tests/test_beagle_example_extension.py
bash .beagle/checks/fix/named_tests.sh $T 2 test_open_task_whose_check_imports_unwritten_module_runs_with_drop_import_brief test_open_task_not_run_offers_no_abandon_done_by
uv run pytest -q $T 
uv run ruff check examples/extensions/beagle.py $T
