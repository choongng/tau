#!/bin/bash
# T0403: a worker's repeated out-of-scope write of one path is told it was refused before, and to finish with its report
set -e
T=tests/test_beagle_example_extension.py
F=examples/extensions/beagle.py
bash .beagle/checks/fix/named_tests.sh $T 3 test_scope_refusal_of_a_path_refused_before_counts_and_sends_to_report test_scope_refusal_first_time_is_unchanged test_scope_refusal_counts_each_path_apart
uv run pytest -q $T
uv run ruff check $F $T
