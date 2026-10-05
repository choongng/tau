#!/bin/bash
# T0216: amended/new-route check
set -e
T=tests/test_beagle_example_extension.py
uv run pytest -q -x \
  "$T::test_amended_check_is_not_refused_as_already_passing" \
  "$T::test_refusals_without_a_worker_do_not_count_toward_escalation" \
  "$T::test_new_route_binds_a_bare_and_chain_like_open"
uv run pytest -q "$T"
uv run ruff check examples/extensions/beagle.py "$T"
