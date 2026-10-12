#!/bin/bash
# T0459: drop-import brief skips a task whose criteria name the import (R55)
set -e
T=tests/test_beagle_example_extension.py
F=examples/extensions/beagle.py
bash .beagle/checks/fix/named_tests.sh $T 1 test_drop_import_brief_skips_a_task_whose_criteria_name_the_import
uv run pytest -q $T
uv run ruff check $F $T
