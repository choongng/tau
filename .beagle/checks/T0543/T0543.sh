#!/bin/bash
# T0543: R97 (q35 semver, bare goal) is graded through its own adapter, and eval.md has its row
# and its own section.
set -e
cd /home/choong/tautest/itc-harness
python3 -c "import json; g=json.load(open('runs/R97/grade.json')); assert (g['passed'], g['total']) == (58, 76), g"
E=/home/choong/tautest/tau/dev-notes/contract-first/eval.md
grep -qE '^\| *R97 *\|.*58/76' "$E" || { echo "no R97 row with 58/76 in eval.md"; exit 1; }
grep -qE '^#+ .*R97' "$E" || { echo "no R97 section in eval.md"; exit 1; }
echo "T0543: R97 graded 58/76 and written up"
