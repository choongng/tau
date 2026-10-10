#!/bin/bash
# Audit 13 on T0347: result lines hold across prompts (hex values and table rows in, code lines out)
set -e
T=tests/test_beagle_example_extension.py
bash .beagle/checks/fix/named_tests.sh $T 3 \
  test_known_answers_unsourced_result_names_reference_result_lines \
  test_result_lines_name_hex_table_rows_not_code_lines \
  test_result_lines_skip_code_statements
uv run pytest -q $T
uv run ruff check examples/extensions/beagle.py $T
