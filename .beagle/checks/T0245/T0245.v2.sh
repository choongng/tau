#!/bin/bash
set -e
f=dev-notes/itc-runs/R26.md
if grep -q "has no infeasible verdict" $f; then echo "R26.md still says beagle close has no infeasible verdict"; exit 1; fi
grep -q "^upstream: .*close --outcome infeasible" $f
bash .beagle/checks/runs/v5/diagnosed.sh R26
