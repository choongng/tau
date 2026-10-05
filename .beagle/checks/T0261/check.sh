#!/bin/bash
# R29 class 2: a non-code task under tests/ is refused at open and plan; unproven with no module offers abandon
set -e
T=tests/test_beagle_example_extension.py
uv run pytest -q -x \
  "$T::test_open_refuses_doc_only_check_under_tests" \
  "$T::test_plan_refuses_reading_only_part" \
  "$T::test_not_proven_without_module_offers_abandon"
uv run pytest -q "$T"
uv run ruff check examples/extensions/beagle.py "$T"
