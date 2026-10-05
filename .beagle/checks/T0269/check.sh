#!/bin/bash
# R31 classes 2 and 4: cut-off advice keeps generator scripts out of scope; helpers left in scope reported; heredoc store reads guarded
set -e
T=tests/test_beagle_example_extension.py
uv run pytest -q -x \
  "$T::test_truncated_call_advice_keeps_generator_out_of_scope" \
  "$T::test_step_report_names_unimported_helper_left_in_scope" \
  "$T::test_worker_guard_refuses_heredoc_store_read"
uv run pytest -q "$T"
uv run ruff check examples/extensions/beagle.py "$T"
