#!/bin/bash
# T0417: R51 q35 itc run, scored and diagnosed (v8), thinking medium for driver and workers,
# compared with the q35 baseline B04, and saying what the fixes first in it (T0437 T0438 T0439 T0440 T0441 T0442) did.
set -eu
R=R51
ITC_MODEL_MAP="q35=qwen3.6-35b-q6-mtp-thinking-coding" bash .beagle/checks/runs/v8/scored.sh $R q35 itc
bash .beagle/checks/runs/v8/diagnosed.sh $R
python3 - "$R" <<'PY'
import json, re, sys
R = sys.argv[1]
m = json.load(open(f'/home/choong/tautest/itc-harness/runs/{R}/meta.json'))
d = m.get('driver_thinking') or {}
assert m.get('mode') == 'pursuit', f"not a pursuit run: {m.get('mode')}"
assert d.get('level') == 'medium' and d.get('sent'), f"driver thinking not medium/sent: {d}"
assert m.get('worker_thinking') == 'medium', f"worker thinking not medium: {m.get('worker_thinking')}"
md = open(f'dev-notes/itc-runs/{R}.md').read()
assert re.search(r'driver_thinking\S*\s+medium|driver thinking\S*\s+medium', md, re.I), "note does not record the driver's thinking level"
assert re.search(r'worker\S* thinking\S*\s+medium|worker_thinking\S*\s+medium', md, re.I), "note does not record the workers' thinking level"
assert re.search(r'^Against B04: \S', md, re.M), "no 'Against B04:' line comparing with the q35 baseline"
assert re.search(r'^Wall: \S', md, re.M), "no 'Wall:' line (wall time, driver and worker tokens, tasks spawned per task done)"
sec = re.split(r"^## ", md.split("\n## Failure classes", 1)[1], maxsplit=1, flags=re.M)[0]
classes = re.split(r"^(?=### )", sec, flags=re.M)[1:]
bad = [c.splitlines()[0] for c in classes if not re.search(r"^Seen in: \S", c, re.M)]
assert not bad, "classes without 'Seen in:': " + "; ".join(bad)
untested = [c.splitlines()[0] for c in classes
            if "[tau]" in c.splitlines()[0] and not re.search(r"tests/[\w/]+\.py::test_\w+", c)]
assert not untested, "[tau] classes naming no test function: " + "; ".join(untested)
assert re.search(r"^### Timeline\s*\n(?:.*\n){3,}", md, re.M), "no ### Timeline with entries"
assert re.search(r"^### The questions\s*\n(?:.*\n){3,}", md, re.M), "no ### The questions with answers"
noind = [c.splitlines()[0] for c in classes if not re.search(r"^Prompt- and model-independent: \S", c, re.M)]
assert not noind, "classes without a 'Prompt- and model-independent:' line: " + "; ".join(noind)
print("OK")
PY
for t in T0437 T0438 T0439 T0440 T0441 T0442; do grep -q "$t" dev-notes/itc-runs/$R.md || { echo "$R.md does not say what $t did"; exit 1; }; done
