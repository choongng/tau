#!/bin/bash
# T0532: R96 graded (grade.json 50/54 from grade_wrenfold.py over runs/R96/adapter.py),
# and eval.md has its table row and its own section.
set -e
cd /home/choong/tautest/itc-harness
python3 -c "import json; g=json.load(open('runs/R96/grade.json')); assert (g['passed'], g['total']) == (50, 54), g"
E=/home/choong/tautest/tau/dev-notes/contract-first/eval.md
grep -qE '^\| *R96 *\|.*50/54' "$E" || { echo "no R96 row with 50/54 in eval.md"; exit 1; }
grep -qE '^#+ .*R96' "$E" || { echo "no R96 section in eval.md"; exit 1; }
echo "T0532: R96 graded 50/54 and written up"
