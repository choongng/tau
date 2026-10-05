#!/bin/bash
# T0244: unproven refusal fallback gives a pursuit_step call; no new_route at the limit
set -e
T=tests/test_beagle_example_extension.py
uv run pytest -q -x \
  "$T::test_unproven_call_tests_only_scope_importing_nothing_gives_step" \
  "$T::test_check_still_fails_at_spawn_limit_offers_infeasible"
uv run pytest -q "$T"
uv run ruff check examples/extensions/beagle.py "$T"
