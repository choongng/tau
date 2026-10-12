#!/bin/bash
# T0482: the done gate -- next, status and the loop-guard Stop hook judge an empty tree by the contract.
set -eu
exec bash .beagle/checks/fix/beagle_named.sh tests/test_contract.py 4 \
  test_done_gate_keeps_acceptance_with_the_tree_it_ran_on \
  test_next_runs_acceptance_when_nothing_is_ready_or_open \
  test_status_reports_the_seal_and_the_acceptance_kept \
  test_the_loop_guard_objects_to_an_end_the_contract_does_not_meet
