#!/bin/bash
# T0598: runs take beagle from a pinned 0.48 checkout, not ~/beagle (whose main
# moves under other work), and R99 is recorded in the contract-first eval.
set -euo pipefail
f=/home/choong/tautest/itc-harness/launch.sh
bash -n "$f"
grep -q 'BEAGLE_ROOT:-$HOME/beagle-wt/0.48}' "$f"
w=/home/choong/beagle-wt/0.48
[ -z "$(git -C "$w" branch --show-current)" ]          # detached: nothing advances it
git -C "$w" merge-base --is-ancestor 08e642c HEAD      # 0.48.0 or a pinned successor
"$w/plugins/beagle-pursuit/bin/beagle" --version | grep -q '^beagle 0\.4[89]'
out=$(cd /home/choong/tautest/itc-harness && ./launch.sh --dry-run S99 q35 wrenfold 2>&1)
echo "$out" | grep -q "^beagle: $w (beagle 0.4"
e=/home/choong/tautest/tau/dev-notes/contract-first/eval.md
grep -qE '^\| *R99 .*75/76' "$e"
