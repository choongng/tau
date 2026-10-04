#!/bin/bash
# R18 class 1: already-passes vs use-the-data-test cycle.
set -e
T=tests/test_beagle_example_extension.py
uv run pytest -q -x \
  "$T::test_open_on_a_check_passing_only_by_uncommitted_scope_work_is_not_refused_as_already_passing" \
  "$T::test_data_test_route_is_not_offered_when_the_data_test_already_passes" \
  "$T::test_amend_to_a_check_passing_only_by_own_uncommitted_work_is_accepted"
uv run pytest -q "$T"
uv run ruff check examples/extensions/beagle.py "$T"
