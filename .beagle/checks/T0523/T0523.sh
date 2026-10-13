#!/bin/bash
# T0523: beagle contract-first's full CI is green, every gate and the whole suite.
# The one standing run of it for the branch: T0498, T0503, T0512, T0513, T0514
# and T0516 claim "beagle CI green" and their own checks run -k subsets.
cd /home/choong/beagle-wt/contract-first || exit 1
out=$(bash ci/check.sh 2>&1); rc=$?
echo "$out" | grep -E '^(=== |ci: )|FAIL|failed|passed' | tail -40
[ "$rc" = 0 ] || { echo "ci/check.sh exited $rc"; exit 1; }
echo "$out" | grep -qx "ci: all gates green" || { echo "ci/check.sh did not say all gates green"; exit 1; }
echo "T0523: beagle contract-first ci/check.sh green"
