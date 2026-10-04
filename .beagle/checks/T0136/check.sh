#!/bin/bash
# R15 classes 5 and 6: worker reports lost to the wall and to raw tool-call markup.
set -e
T=tests/test_beagle_example_extension.py
uv run pytest -q -x \
  "$T::test_second_worker_timeout_keeps_the_first_attempts_report_and_check" \
  "$T::test_worker_timeout_names_output_limit_turns_not_the_env_var" \
  "$T::test_report_ending_in_a_raw_tool_call_keeps_the_text_before_it" \
  "$T::test_bare_raw_tool_call_report_is_still_replaced"
uv run pytest -q "$T"
uv run ruff check examples/extensions/beagle.py "$T"
