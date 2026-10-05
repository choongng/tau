#!/bin/bash
# T0253: fix route, title clash and container answer cannot deadlock
set -e
T=tests/test_beagle_example_extension.py
uv run pytest -q -x \
  "$T::test_fix_route_reuses_existing_fix_leaf" \
  "$T::test_fix_route_title_unique_when_title_exists" \
  "$T::test_title_clash_ignores_ancestor_and_container" \
  "$T::test_title_clash_never_says_work_a_container"
uv run pytest -q "$T"
uv run ruff check examples/extensions/beagle.py "$T"
