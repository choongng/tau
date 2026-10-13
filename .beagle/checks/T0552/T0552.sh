#!/bin/bash
# T0552: the incremental-contract design note exists, answers its sections with file:line
# evidence from beagle and the tau extension, and names the build tasks it splits into.
set -e
F=/home/choong/tautest/tau/dev-notes/contract-first/incremental-contract.md
[ -f "$F" ] || { echo "no $F"; exit 1; }
for h in "## The flow" "## Slices and the seal" "## Coverage: what done means" "## Stand-ins" "## Re-reads on evidence" "## What changes in beagle" "## What changes in tau" "## Build tasks"; do
  grep -qF "$h" "$F" || { echo "missing section: $h"; exit 1; }
done
n=$(grep -cE '[a-z_/.]+\.(py|md):[0-9]+' "$F")
[ "$n" -ge 10 ] || { echo "only $n file:line citations"; exit 1; }
echo "T0552: incremental-contract design written, $n citations"
