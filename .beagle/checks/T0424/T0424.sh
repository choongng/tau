#!/bin/bash
# T0424: R58 q35 cobs run, scored and diagnosed (v8), thinking medium for driver and workers,
# arm lean (R0002) on the frozen tau sha, compared with the q35 baseline B05 and the other arm's run (-),
# with the mechanisms that fired and what each cost or caught.
set -eu
R=R58
ITC_MODEL_MAP="q35=qwen3.6-35b-q6-mtp-thinking-coding" bash .beagle/checks/runs/v8/scored.sh $R q35 cobs
bash .beagle/checks/runs/v8/diagnosed.sh $R
python3 - "$R" <<'PY'
import json, re, sys
R = sys.argv[1]
m = json.load(open(f'/home/choong/tautest/itc-harness/runs/{R}/meta.json'))
d = m.get('driver_thinking') or {}
assert m.get('mode') == 'pursuit', f"not a pursuit run: {m.get('mode')}"
assert d.get('level') == 'medium' and d.get('sent'), f"driver thinking not medium/sent: {d}"
assert m.get('worker_thinking') == 'medium', f"worker thinking not medium: {m.get('worker_thinking')}"
assert m.get('arm') == 'lean', f"arm is {m.get('arm')!r}, not lean"
frozen = open('.beagle/checks/runs/frozen-sha.txt').read().split()[0]
import subprocess
moved = subprocess.run(['git', 'diff', '--name-only', frozen, m.get('tau_sha', 'HEAD'), '--', '.', ':!.beagle', ':!dev-notes'],
                       capture_output=True, text=True, check=True).stdout.split()
assert not moved, f"tau {m.get('tau_sha')} differs from the frozen {frozen} in {moved[:5]}"
assert m.get('tau_dirty_code_files', 1) == 0, "tau had uncommitted code changes at launch"
md = open(f'dev-notes/itc-runs/{R}.md').read()
assert re.search(r'driver_thinking\S*\s+medium|driver thinking\S*\s+medium', md, re.I), "note does not record the driver's thinking level"
assert re.search(r'worker\S* thinking\S*\s+medium|worker_thinking\S*\s+medium', md, re.I), "note does not record the workers' thinking level"
assert re.search(r'^Against B05: \S', md, re.M), "no 'Against B05:' line comparing with the q35 baseline"
assert re.search(r'^Arm: lean\b', md, re.M), "no 'Arm: lean' line"
if '-' != '-':
    assert re.search(r'^Against -: \S', md, re.M), "no 'Against -:' line comparing with the other arm"
mech = re.search(r"^## Mechanisms\s*\n((?:.*\n)*?)(?=^## |\Z)", md, re.M)
assert mech and len(re.findall(r"^- M\d\d\b", mech.group(1), re.M)) >= 3,     "no '## Mechanisms' section with '- Mnn' lines (from itc-harness/ledger/mechanism-ledger.md): what fired, cost, caught"
assert re.search(r'^Wall: \S', md, re.M), "no 'Wall:' line (wall time, driver and worker tokens, tasks spawned per task done)"
sec = re.split(r"^## ", md.split("\n## Failure classes", 1)[1], maxsplit=1, flags=re.M)[0]
classes = re.split(r"^(?=### )", sec, flags=re.M)[1:]
bad = [c.splitlines()[0] for c in classes if not re.search(r"^Seen in: \S", c, re.M)]
assert not bad, "classes without 'Seen in:': " + "; ".join(bad)
untested = [c.splitlines()[0] for c in classes
            if "[tau]" in c.splitlines()[0] and not re.search(r"tests/[\w/]+\.py::test_\w+", c)]
assert not untested, "[tau] classes naming no test function: " + "; ".join(untested)
unwritten = []
for c in classes:
    if "[tau]" not in c.splitlines()[0]:
        continue
    names = set(re.findall(r"tests/[\w/]+\.py::(test_\w+)", c))
    absent = [n for n in names if subprocess.run(['git', 'grep', '-qE', rf'def {n}\b', '--', 'tests'], capture_output=True).returncode]
    if absent and not re.search(r"^(Deferred|Filed as): \S", c, re.M):
        unwritten.append(c.splitlines()[0] + " -> " + ", ".join(sorted(absent)))
assert not unwritten, "[tau] classes citing tests that do not exist, with no 'Deferred: <why>' or 'Filed as: TNNNN' line (audit 2026-10-12): " + "; ".join(unwritten)
assert re.search(r"^### Timeline\s*\n(?:.*\n){3,}", md, re.M), "no ### Timeline with entries"
assert re.search(r"^### The questions\s*\n(?:.*\n){3,}", md, re.M), "no ### The questions with answers"
noind = [c.splitlines()[0] for c in classes if not re.search(r"^Prompt- and model-independent: \S", c, re.M)]
assert not noind, "classes without a 'Prompt- and model-independent:' line: " + "; ".join(noind)
print("OK")
PY
for t in ; do grep -q "$t" dev-notes/itc-runs/$R.md || { echo "$R.md does not say what $t did"; exit 1; }; done
