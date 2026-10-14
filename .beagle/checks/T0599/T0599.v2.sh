#!/bin/bash
# T0599: the contract mode is gone from tau's beagle extension (branch beagle-0.48,
# worktree ~/tautest/tau-wt-048): no contract verb, slice, seal-the-contract or
# dispute code; founding on a bare goal plans no task before the first milestone;
# the extension's tests pass, with the contained beagle venv off PATH (T0550).
# (v2: the line cap the strip closed under, 16300, was a size at the close,
# not a standard; T0601's spec-tied step grew the file past it.)
set -euo pipefail
W=/home/choong/tautest/tau-wt-048
E=$W/examples/extensions/beagle.py
cd "$W"
[ "$(git branch --show-current)" = beagle-0.48 ]
if grep -nE 'CONTRACT_FIRST_NOTE|CONTRACT_MILESTONES|SLICE_PREFIX|_seal_when_ready|_judge_dispute|_contract_verdict|"pursuit", "contract"|pursuit contract ' "$E"; then
  echo "contract-mode code left in $E" >&2; exit 1
fi
PATH=$(echo "$PATH" | tr ':' '\n' | grep -v '/beagle/venv' | paste -sd:)
out=$(timeout 840 .venv/bin/python -m pytest -q --no-header -p no:cacheprovider tests/test_beagle_example_extension.py 2>&1 | tail -3)
echo "$out" >&2
echo "$out" | grep -qE '^[0-9]+ passed' || exit 1
echo "$out" | grep -qE 'failed|error' && exit 1
out=$(timeout 120 .venv/bin/python -m pytest -q --no-header -p no:cacheprovider tests/test_beagle_example_extension.py -k "bare_goal and no_slice" 2>&1 | tail -1)
echo "$out" >&2
echo "$out" | grep -qE '^[1-9][0-9]* passed' && ! echo "$out" | grep -qE 'failed|error'
