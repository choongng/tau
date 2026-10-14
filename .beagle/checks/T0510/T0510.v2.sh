#!/bin/bash
# T0510: after the seal a milestone is checked with `contract run --operation`:
# the seal note says so and names the operations, pursuit_step accepts that
# command, and an inline check asserting answers is refused under a sealed contract.
set -e
cd /home/choong/tautest/tau
uv run --quiet pytest -q -p no:cacheprovider tests/test_beagle_example_extension.py \
  -k "copied_answers or asserts_answers_inline or may_run_the_contract or seals_the_contract_once" \
  2>&1 | tail -1 | tee /dev/stderr | grep -qE '^5 passed'
