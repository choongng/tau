#!/bin/bash
# T0202: R21 classes 4 and 5, T0172 text
set -e
T=tests/test_beagle_example_extension.py
uv run pytest -q -x \
  "$T::test_worker_guard_explains_a_truncated_tool_call_instead_of_a_missing_path" \
  "$T::test_inline_script_write_after_cd_resolves_against_that_directory" \
  "$T::test_scratch_script_refusal_does_not_mention_the_implementation"
uv run pytest -q "$T"
uv run ruff check examples/extensions/beagle.py "$T"
