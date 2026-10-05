#!/bin/bash
# T0242: at the attempt limit, unproven results offer the infeasible close
set -e
T=tests/test_beagle_example_extension.py
uv run pytest -q -x \
  "$T::test_unproven_step_at_spawn_limit_offers_infeasible_not_new_route" \
  "$T::test_spawn_refusal_relay_offers_infeasible_close" \
  "$T::test_infeasible_abandon_refused_below_the_limit"
uv run pytest -q "$T"
uv run ruff check examples/extensions/beagle.py "$T"
