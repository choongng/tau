#!/bin/bash
# Audit 7 defects 4-5: other readers of .beagle/, short reports before markup, output-limit blame over the whole run.
set -e
T=tests/test_beagle_example_extension.py
uv run pytest -q -x \
  "$T::test_worker_guard_refuses_other_readers_of_dot_beagle" \
  "$T::test_worker_guard_refuses_git_cat_file_of_dot_beagle" \
  "$T::test_short_report_before_markup_is_kept" \
  "$T::test_timeout_blames_output_limit_only_when_last_turns_hit_it"
uv run pytest -q "$T"
uv run ruff check examples/extensions/beagle.py "$T"
