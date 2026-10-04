#!/bin/bash
# usage: scored.sh RNN — runs/scored.sh, plus the launch facts in meta.json:
# the hour cap, a clean tau at a real commit, the model passed as --model, and
# the prompt passed byte for byte.
# env: ITC_RUNS_DIR (harness runs), ITC_NOTES_DIR (run notes), ITC_PROMPT, TAU_REPO.
set -eu
here=$(cd "$(dirname "$0")" && pwd)
R=$1
H=${ITC_RUNS_DIR:-/home/choong/tautest/itc-harness/runs}/$R
f=${ITC_NOTES_DIR:-dev-notes/itc-runs}/$R.md
P=${ITC_PROMPT:-/home/choong/tautest/itc_prompt.txt}
T=${TAU_REPO:-/home/choong/tautest/tau}
test -s "$H/exit.json"
python3 -c "import json; m=json.load(open('$H/meta.json')); assert m.get('session'), 'no session recorded'; assert m.get('tau_sha'), 'not launched by launch.sh'"
test -s "$H/scorecard.json"
test -s "$H/grade.json"
python3 -c "import json; c=json.load(open('$H/scorecard.json')); assert 'workers' in c, 'scorecard made without --meta'"
test -s "$f"
grep -q '^## Scorecard' "$f"
grep -qE '^grader: [0-9]+/[0-9]+' "$f"
python3 - "$H/scorecard.json" "$f" <<'PY'
import json, re, sys
c = json.load(open(sys.argv[1])); md = open(sys.argv[2]).read()
block = md.split("## Scorecard", 1)[1].split("```")[1]
for key in ("tasks_total", "tasks_done", "commits", "founded", "uncommitted_files"):
    m = re.search(rf"^{key}\s+(\S+)", block, re.M)
    assert m, f"no {key} in the Scorecard block"
    assert m.group(1) == str(c.get(key)), f"Scorecard {key} {m.group(1)} != scorecard.json {c.get(key)}"
g = json.load(open(sys.argv[1].replace("scorecard.json", "grade.json")))
m = re.search(r"^grader: (\d+)/(\d+)", md, re.M)
assert (int(m.group(1)), int(m.group(2))) == (g["passed"], g["total"]), f"grader line {m.group(0)} != grade.json {g['passed']}/{g['total']}"
PY
sha=$(python3 - "$H/meta.json" "$P" "$here" <<'PY'
import json, sys
sys.path.insert(0, sys.argv[3])
from launchargs import split
m = json.load(open(sys.argv[1]))
assert m.get("wall_cap_s") == 3600, f"wall_cap_s {m.get('wall_cap_s')!r} != 3600"
assert m.get("tau_dirty_files") == 0, f"tau_dirty_files {m.get('tau_dirty_files')!r} != 0"
model = m.get("model")
assert model, "no model recorded"
argv = split(m.get("launch_command") or "")
assert argv, "no launch_command recorded"
pairs = list(zip(argv, argv[1:]))
assert (b"--model", model.encode()) in pairs, f"launch_command has no '--model {model}'"
assert argv[-1] == open(sys.argv[2], "rb").read(), "launch_command's prompt differs from " + sys.argv[2]
print(m["tau_sha"])
PY
)
git -C "$T" cat-file -e "$sha^{commit}" 2>/dev/null || { echo "tau_sha $sha is not a commit in $T" >&2; exit 1; }
echo OK
