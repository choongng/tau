#!/bin/bash
# B02 baseline (mimo, itc): the v8 run check against the baseline prompt, launched as a baseline (plain tau, no extensions)
set -eu
ITC_PROMPT=/home/choong/tautest/itc-harness/prompts/itc_baseline_prompt.txt bash .beagle/checks/runs/v8/scored.sh B02 mimo itc
python3 -c "import json; m=json.load(open('/home/choong/tautest/itc-harness/runs/B02/meta.json')); assert m.get('mode') == 'baseline', m.get('mode'); assert '--no-extensions' in m['launch_command'], 'not run without extensions'"
grep -qE '^(Ended|How it ended):' dev-notes/itc-runs/B02.md || { echo "B02.md does not say how the run ended"; exit 1; }
grep -qE '^Built:' dev-notes/itc-runs/B02.md || { echo "B02.md does not say what the run built"; exit 1; }
