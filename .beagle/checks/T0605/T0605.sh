#!/bin/bash
# T0605: the 0.48 rotation ran and is recorded: R100-R103 (wrenfold, semver
# bare goal, itc, cobs) each ended and was graded on beagle 0.48.0, each has an
# eval.md row and section, and eval.md has the before/after table.
set -euo pipefail
E=/home/choong/tautest/tau/dev-notes/contract-first/eval.md
H=/home/choong/tautest/itc-harness/runs
declare -A TASK=([R100]=wrenfold [R101]=semver [R102]=itc [R103]=cobs)
for r in R100 R101 R102 R103; do
  [ -f $H/$r/exit.json ] && [ -f $H/$r/grade.json ] || { echo "$r not ended and graded" >&2; exit 1; }
  python3 -c 'import json,sys; m=json.load(open(sys.argv[1])); assert m["task"]==sys.argv[2] and m["beagle_version"]=="beagle 0.48.0" and m["tau_dirty_code_files"]==0, m' $H/$r/meta.json "${TASK[$r]}"
  grep -qE "^\| $r \|" $E && grep -qE "^## $r " $E || { echo "$r not in eval.md" >&2; exit 1; }
done
grep -qiE '^## .*before/after' $E
