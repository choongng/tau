#!/bin/bash
# R44 fix: the step cap keeps a passing check, and the stop gate accepts the stop it offered
set -e
T=tests/test_beagle_example_extension.py
bash .beagle/checks/fix/named_tests.sh $T 3 test_source_judge_escalation_after_an_early_failed_check test_step_cap_keeps_a_passing_bound_check test_stop_gate_accepts_a_stop_the_step_cap_offered
uv run pytest -q $T
uv run ruff check examples/extensions/beagle.py $T
