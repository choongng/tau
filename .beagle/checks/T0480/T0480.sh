#!/bin/bash
# T0480: contract diff and the second-extraction coverage rule, in beagle's contract-first worktree.
set -eu
exec bash .beagle/checks/fix/beagle_named.sh tests/test_contract.py 5 \
  test_contract_diff_reports_spans_and_operations_only_one_side_cites \
  test_contract_check_refuses_a_second_span_the_primary_does_not_cover \
  test_contract_excluded_covers_a_second_span_with_a_reason \
  test_contract_check_draft_skips_the_second_extraction \
  test_cli_pursuit_contract_diff_exit_codes
