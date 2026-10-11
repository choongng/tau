#!/bin/bash
# T0441: offers and refusals around new_route, attempt limits and container amend agree
set -e
T=tests/test_beagle_example_extension.py
F=examples/extensions/beagle.py
bash .beagle/checks/fix/named_tests.sh $T 5 test_spawn_refusal_does_not_offer_new_route_and_forbid_it test_attempt_limit_arithmetic_reads_true test_pending_spawn_refusal_says_to_drop_new_route test_bash_amend_of_a_container_is_not_sent_to_pursuit_step test_infeasible_on_a_pending_task_offers_a_move_tau_accepts
uv run pytest -q $T
uv run ruff check $F $T
