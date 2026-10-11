#!/bin/bash
# B04 baseline (q35, itc): the v8 run check against the baseline prompt, launched as a baseline (plain tau, no extensions); q35 added to the model map
set -eu
ITC_MODEL_MAP="q35=qwen3.6-35b-q6-mtp-thinking-coding" ITC_PROMPT=/home/choong/tautest/itc-harness/prompts/itc_baseline_prompt.txt bash .beagle/checks/runs/v8/scored.sh B04 q35 itc
python3 -c "import json; m=json.load(open('/home/choong/tautest/itc-harness/runs/B04/meta.json')); assert m.get('mode') == 'baseline', m.get('mode'); assert '--no-extensions' in m['launch_command'], 'not run without extensions'"
grep -qE '^(Ended|How it ended):' dev-notes/itc-runs/B04.md || { echo "B04.md does not say how the run ended"; exit 1; }
grep -qE '^Built:' dev-notes/itc-runs/B04.md || { echo "B04.md does not say what the run built"; exit 1; }
grep -qE '^Wall:' dev-notes/itc-runs/B04.md || { echo "B04.md does not give the wall time"; exit 1; }
