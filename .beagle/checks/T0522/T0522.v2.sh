#!/bin/bash
# T0522: an open contract milestone keeps its check (and scope) when the driver
# passes another, says so, and a substituted check is put back.
set -e
cd /home/choong/tautest/tau
uv run --quiet pytest -q -p no:cacheprovider tests/test_beagle_example_extension.py \
  -k "keeps_an_open_contract_milestone or scopes_the_contract_milestones_itself" \
  2>&1 | tail -1 | tee /dev/stderr | grep -qE '^2 passed'
