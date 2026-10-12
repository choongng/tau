#!/bin/bash
# T0481: contract seal, status, run, and the order and drift gates, in beagle's contract-first worktree.
set -eu
exec bash .beagle/checks/fix/beagle_named.sh tests/test_contract.py 9 \
  test_contract_status_moves_from_none_to_draft_ready_sealed_altered \
  test_contract_seal_refuses_a_contract_that_does_not_check \
  test_contract_seal_records_each_sealed_files_sha \
  test_open_refuses_non_contract_work_before_the_seal \
  test_open_before_contract_records_why \
  test_close_done_refuses_a_task_that_altered_the_sealed_contract \
  test_contract_run_runs_acceptance_under_run_contain \
  test_a_check_may_run_contract_check_but_not_contract_seal \
  test_cli_pursuit_contract_seal_status_run
