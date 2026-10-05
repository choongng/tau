#!/bin/bash
set -e
f=dev-notes/itc-runs/R26.md
! grep -q "has no infeasible verdict" $f
grep -q "^upstream: .*close --outcome infeasible" $f
bash .beagle/checks/runs/v5/diagnosed.sh R26
