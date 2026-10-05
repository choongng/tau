#!/bin/bash
# T0239: calls at beagle's attempt limit
set -e
T=tests/test_beagle_example_extension.py
uv run pytest -q -x \
  "$T::test_unproven_call_at_spawn_limit_offers_no_new_route" \
  "$T::test_cases_first_does_not_send_to_open_unprovable_holder" \
  "$T::test_abandon_infeasible_closes_open_task_at_attempt_limit"
uv run pytest -q "$T"
uv run ruff check examples/extensions/beagle.py "$T"
