#!/bin/bash
# progress.py reports the furthest stage per run and per cell
set -eu
out=$(python3 /home/choong/tautest/itc-harness/progress.py)
echo "$out" | head -40
line(){ echo "$out" | grep -E "^$1 " | head -1; }
for want in "R38 .*\bnone\b" "R40 .*\bfounded\b" "R34 .*\bany-pass\b" "R39 .*\bany-pass\b" "R36 .*\bfounded\b"; do
  r=${want%% *}
  line "$r" | grep -qE "$want" || { echo "stage wrong for $r: $(line $r)"; exit 1; }
done
echo "$out" | grep -qE "furthest|stage" || { echo "no stage column"; exit 1; }
python3 -m py_compile /home/choong/tautest/itc-harness/progress.py
