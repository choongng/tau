#!/bin/bash
# Driver write/edit refusal names the pursuit_step call for the task next offers (refusal-only route, owner 2026-10-10)
set -e
T=tests/test_beagle_example_extension.py
bash .beagle/checks/fix/named_tests.sh $T 2 test_driver_edit_refusal_names_the_step_for_the_ready_task test_driver_edit_refusal_without_a_ready_task_names_bare_step
uv run pytest -q $T
uv run ruff check examples/extensions/beagle.py $T
