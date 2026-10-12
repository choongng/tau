#!/bin/bash
# T0479: beagle's contract record and `pursuit contract check` (contract-first branch)
set -e
bash .beagle/checks/fix/beagle_named.sh tests/test_contract.py 9 \
  test_contract_check_passes_a_sourced_inventory \
  test_contract_check_refuses_a_quote_not_in_its_source \
  test_contract_quote_matches_across_pdf_line_breaks_and_hyphenation \
  test_contract_check_refuses_an_operation_nothing_exercises \
  test_contract_check_refuses_an_unsettled_gap \
  test_contract_check_refuses_acceptance_files_that_skip_a_property \
  test_contract_check_experiment_quote_must_be_in_its_output \
  test_read_contract_never_raises \
  test_cli_pursuit_contract_check_exit_codes
