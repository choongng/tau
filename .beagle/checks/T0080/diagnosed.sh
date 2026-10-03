#!/bin/bash
# usage: diagnosed.sh RNN — the trace analysis names its failure classes with an owner each.
set -eu
R=$1; f=dev-notes/itc-runs/$R.md
grep -q '^## Trace analysis' "$f"
grep -q '^## Failure classes' "$f"
n=$(sed -n '/^## Failure classes/,/^## /p' "$f" | { grep -cE '^### \[(tau|beagle|model|harness)\] ' || true; })
test "$n" -ge 1
# every class says what is done about it
m=$(sed -n '/^## Failure classes/,/^## /p' "$f" | { grep -cE '^(Action|Disposition): ' || true; })
test "$m" -ge "$n"
echo OK
