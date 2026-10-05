#!/bin/bash
# T0210: v5 run checks add the RNN.md header and clean-start clauses; v4 is unchanged.
set -e
test -x .beagle/checks/runs/v5/scored.sh || test -f .beagle/checks/runs/v5/scored.sh
bash .beagle/checks/runs/v5/selftest.sh
git diff --quiet a995dd8 -- .beagle/checks/runs/v4/
python3 -c "
import json,subprocess
s=json.load(open('/home/choong/tautest/itc-harness/runs/R22/scorecard.json'))
assert 'first_commit_ts' in s, 'scorecard.json lacks first_commit_ts'
"
bash .beagle/checks/runs/v5/scored.sh R22 qwen cobs
