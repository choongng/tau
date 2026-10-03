#!/bin/bash
# T0017: summary.md covers all ten runs, the recurring failure classes, and what is still open.
set -eu
f=dev-notes/itc-runs/summary.md
test -s "$f"
for h in "## Runs" "## Recurring failure classes" "## What changed in tau" "## Still open" "## Next"; do
  grep -qF "$h" "$f" || { echo "missing heading: $h"; exit 1; }
done
for r in R01 R02 R03 R04 R05 R06 R07 R08 R09 R10; do
  g=$(grep -m1 '^grader:' dev-notes/itc-runs/$r.md | grep -oE '[0-9]+/42')
  grep -qE "^\| *$r *\|.*\| *$g *\|" "$f" || { echo "table row for $r missing or grader != $g"; exit 1; }
done
n=$(grep -c '^### ' "$f"); [ "$n" -ge 4 ] || { echo "only $n failure classes"; exit 1; }
[ "$(grep -c '^Runs: ' "$f")" -ge 4 ] || { echo "each class needs a 'Runs:' line"; exit 1; }
[ "$(grep -cE '^Status: (fixed|partly fixed|open|model)' "$f")" -ge 4 ] || { echo "each class needs a Status: line"; exit 1; }
