#!/bin/bash
# T0249: cut-off calls and silent worker ends reach the driver
set -e
T=tests/test_beagle_example_extension.py
uv run pytest -q -x \
  "$T::test_truncated_call_names_char_budget" \
  "$T::test_worker_events_counts_truncated_refusal_as_length_stop" \
  "$T::test_timeout_after_cutoffs_names_output_limit" \
  "$T::test_second_truncated_call_says_it_repeats" \
  "$T::test_step_result_names_earlier_worker_without_report"
uv run pytest -q "$T"
uv run ruff check examples/extensions/beagle.py "$T"
