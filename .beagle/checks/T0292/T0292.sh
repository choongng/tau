#!/bin/bash
# R35 fix: an escalation's offered route must change the call
set -e
T=tests/test_beagle_example_extension.py
uv run pytest -q -x \
  "$T::test_new_route_same_check_carries_not_done_count" \
  "$T::test_escalation_with_kept_check_offers_split_not_new_route" \
  "$T::test_new_route_identical_check_and_scope_refused_after_escalation"
uv run pytest -q "$T"
uv run ruff check examples/extensions/beagle.py "$T"
