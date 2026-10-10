#!/bin/bash
# R44 fix: the unwritten-import hint applies to a directory scope
set -e
T=tests/test_beagle_example_extension.py
bash .beagle/checks/fix/named_tests.sh $T 2 test_data_test_unwritten_import_on_a_directory_scope test_scope_has_data_counts_a_data_file_under_a_directory_entry
uv run pytest -q $T
uv run ruff check examples/extensions/beagle.py $T
