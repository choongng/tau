#!/bin/bash
# T0231: first worker hears the last failure
set -e
T=tests/test_beagle_example_extension.py
uv run pytest -q -x \
  "$T::test_first_worker_of_step_is_briefed_with_last_failure" \
  "$T::test_runner_note_skips_test_the_check_does_not_run"
uv run pytest -q "$T"
uv run ruff check examples/extensions/beagle.py "$T"
