#!/bin/bash
# T0407: a done-by close opens past beagle's rank gate with a recorded reason
set -e
T=tests/test_beagle_example_extension.py
F=examples/extensions/beagle.py
bash .beagle/checks/fix/named_tests.sh $T 2 test_done_by_open_passes_over_naming_the_done_task test_done_by_close_of_a_lower_ranked_task_is_not_refused_by_rank
uv run pytest -q $T
uv run ruff check $F $T
