#!/bin/bash
# T0494: the clauses of T0479/T0480 the audit could remove with their checks green, each now tested.
set -eu
exec bash .beagle/checks/fix/beagle_named.sh tests/test_contract.py 3 \
  test_contract_quote_folds_curly_quotes_to_straight \
  test_contract_check_refuses_an_entry_without_id_kind_or_operation \
  test_contract_diff_identifies_an_experiment_by_its_command
