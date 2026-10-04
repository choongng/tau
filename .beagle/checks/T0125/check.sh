#!/bin/bash
# R14 class 3: locked tests restored even when the lock store is rewritten; whole-tree ruff format refused.
set -e
T=tests/test_beagle_example_extension.py
uv run pytest -q -x \
  "$T::test_restore_locked_undoes_a_change_made_to_the_store_as_well" \
  "$T::test_worker_guard_refuses_ruff_format_over_the_whole_tree"
uv run pytest -q "$T"
uv run ruff check examples/extensions/beagle.py "$T"
