#!/bin/bash
# T0448: the known-answers source judge never offers an input row as a result line (R52)
set -e
T=tests/test_beagle_example_extension.py
F=examples/extensions/beagle.py
bash .beagle/checks/fix/named_tests.sh $T 2 test_unanswered_case_note_names_no_result_lines test_unquoted_cases_rejects_example_index_row_as_source
uv run pytest -q $T
uv run ruff check $F $T
