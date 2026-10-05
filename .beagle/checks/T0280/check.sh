#!/bin/bash
# R33 classes 4 and 5: workers stop re-reading past half the turn cap with nothing written; output-cap cut-offs end the worker on the second over the run
set -e
T=tests/test_beagle_example_extension.py
uv run pytest -q -x \
  "$T::test_worker_guard_refuses_reads_past_half_cap_with_nothing_written" \
  "$T::test_worker_ended_on_second_output_cap_cutoff_over_run" \
  "$T::test_cutoff_advice_sizes_parts_to_output_limit"
uv run pytest -q "$T"
uv run ruff check examples/extensions/beagle.py "$T"
