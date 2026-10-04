#!/bin/bash
# R15 class 7: workers read .beagle/ and re-read the references.
set -e
T=tests/test_beagle_example_extension.py
uv run pytest -q -x \
  "$T::test_worker_guard_refuses_reading_dot_beagle" \
  "$T::test_worker_guard_refuses_git_show_of_a_dot_beagle_path" \
  "$T::test_bash_write_targets_sees_uv_init_dir" \
  "$T::test_retry_brief_carries_the_previous_attempts_report"
uv run pytest -q "$T"
uv run ruff check examples/extensions/beagle.py "$T"
