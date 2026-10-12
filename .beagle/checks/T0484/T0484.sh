#!/bin/bash
# T0484: the contract-guard PreToolUse hook refuses edits to sealed files.
set -eu
exec bash .beagle/checks/fix/beagle_named.sh tests/test_contract.py 2 \
  test_contract_guard_refuses_an_edit_to_a_sealed_file \
  test_contract_guard_is_silent_without_a_contract
