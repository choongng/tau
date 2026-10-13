#!/bin/bash
# T0534: B07 graded (grade.json 75/76 from grade_semver.py over runs/B07/adapter.py),
# and eval.md has its table row and its own section.
set -e
cd /home/choong/tautest/itc-harness
python3 -c "import json; g=json.load(open('runs/B07/grade.json')); assert (g['passed'], g['total']) == (75, 76), g"
E=/home/choong/tautest/tau/dev-notes/contract-first/eval.md
grep -qE '^\| *B07 *\|.*75/76' "$E" || { echo "no B07 row with 75/76 in eval.md"; exit 1; }
grep -qE '^#+ .*B07' "$E" || { echo "no B07 section in eval.md"; exit 1; }
echo "T0534: B07 graded 75/76 and written up"
