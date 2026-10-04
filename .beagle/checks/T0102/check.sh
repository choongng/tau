#!/bin/bash
# T0102: the R11-R20 summary has a row per run whose grade matches that run's notes,
# the recurring classes, the comparison with R01-R10, and summary.md points to it.
set -e
D=dev-notes/itc-runs; F=$D/summary-R11-R20.md
test -f "$F"
for n in 11 12 13 14 15 16 17 18 19 20; do
  g=$(grep -m1 -oE '^grader: [0-9]+/42' $D/R$n.md | cut -d' ' -f2)
  grep -qE "^\| R$n \|.*\| $g \|" "$F" || { echo "R$n row missing or grade not $g"; exit 1; }
done
for h in "## Runs" "## Recurring failure classes" "## Compared with R01–R10" "## What changed in tau" "## Still open"; do
  grep -qF "$h" "$F" || { echo "missing $h"; exit 1; }
done
grep -qF "summary-R11-R20.md" $D/summary.md
echo OK
