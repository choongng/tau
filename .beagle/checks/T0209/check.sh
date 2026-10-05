#!/bin/bash
# T0209: R22 classes 7 and 9
set -e
T=tests/test_beagle_example_extension.py
uv run pytest -q -x \
  "$T::test_root_plan_refuses_a_part_titled_like_a_live_task" \
  "$T::test_a_later_milestone_can_be_abandoned_as_a_duplicate" \
  "$T::test_model_facing_text_names_no_past_run"
uv run pytest -q "$T"
uv run ruff check examples/extensions/beagle.py "$T"
