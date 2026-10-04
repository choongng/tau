#!/bin/bash
# R18 class 2: data-test resend superseded an open task and hid the spawn.
set -e
T=tests/test_beagle_example_extension.py
uv run pytest -q -x \
  "$T::test_data_test_resend_on_an_open_task_amends_instead_of_spawning" \
  "$T::test_refusal_after_a_new_route_spawn_names_the_successor" \
  "$T::test_new_route_successor_keeps_the_predecessor_scope"
uv run pytest -q "$T"
uv run ruff check examples/extensions/beagle.py "$T"
