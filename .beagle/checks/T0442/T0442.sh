#!/bin/bash
# T0442: the worker wall fits the model's decode speed and a killed worker's progress reaches the next
set -e
T=tests/test_beagle_example_extension.py
F=examples/extensions/beagle.py
bash .beagle/checks/fix/named_tests.sh $T 3 test_worker_wall_scales_with_max_tokens_and_measured_rate test_worker_wall_default_unchanged_without_a_measured_rate test_killed_worker_progress_reaches_the_next_attempts_notes
uv run pytest -q $T
uv run ruff check $F $T
