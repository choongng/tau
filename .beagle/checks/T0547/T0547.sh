#!/bin/bash
# T0547: pursuit_step judges a worker's DISPUTE <id> at a sub-agent boundary and routes
# an upheld one to a contract amend that pins the judge's value; an altered contract
# is re-sealed with the dispute's reason (R96: a sealed test invented 319 for 81664).
set -e
cd /home/choong/tautest/tau
timeout 300 uv run --quiet pytest -q -p no:cacheprovider tests/test_beagle_example_extension.py \
  -k "dispute_is_judged_and_an_upheld_one_amends_the_contract or dispute_without_a_failing_entry_is_not_judged or reseals_an_altered_contract_with_the_dispute_reason" \
  2>&1 | tail -1 | tee /dev/stderr | grep -qE '^3 passed'
