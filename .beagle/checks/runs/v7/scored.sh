#!/bin/bash
# usage: scored.sh RNN mimo|qwen|gemma itc|cobs — runs/scored.sh, plus the launch
# facts in meta.json: the hour cap, a clean tau at a real commit, the model
# passed as --model, meta.model equal to the full name launch.sh maps the short
# model name to, and (new in v4) meta.task equal to TASK (a meta with no task
# is an itc run, from before launch.sh took one) and the prompt passed byte for
# byte equal to /home/choong/tautest/TASK_prompt.txt. New in v5: RNN.md's first
# line is exactly '# RNN — <meta.model> — <meta.task>_prompt.txt', the
# paragraph after it names 'tau <first 7 of meta.tau_sha>', and the project
# started clean: scorecard.json's first_commit_ts is not null and is at or
# after meta.start - 5. New in v6: gemma (gemma4-12b-q4) joins the model map.
# New in v7: a run that never founded (scorecard founded False, commits 0 and
# record_commits 0) made no repo, so it has no first commit to date; its
# first_commit_ts may be null. Any run with a commit still needs one dated.
# env: ITC_RUNS_DIR (harness runs), ITC_NOTES_DIR (run notes), ITC_PROMPT
# (replaces the task's prompt file; for the selftest), TAU_REPO,
# ITC_MODEL_MAP (space-separated short=full pairs replacing the launch.sh map;
# for the selftest).
set -eu
here=$(cd "$(dirname "$0")" && pwd)
MAP=${ITC_MODEL_MAP:-mimo=mimo-v2.6-9b-q4 qwen=qwen3.5-9b-q4-mtp-thinking-coding gemma=gemma4-12b-q4}
usage() { local n=; for kv in $MAP; do n="$n${n:+|}${kv%%=*}"; done; echo "usage: $0 RNN $n itc|cobs" >&2; exit 2; }
[ $# -eq 3 ] || usage
R=$1
want=
for kv in $MAP; do [ "${kv%%=*}" = "$2" ] && want=${kv#*=}; done
[ -n "$want" ] || { echo "unknown model '$2'" >&2; usage; }
TASK=$3
case "$TASK" in itc|cobs) ;; *) echo "unknown task '$TASK'" >&2; usage ;; esac
H=${ITC_RUNS_DIR:-/home/choong/tautest/itc-harness/runs}/$R
f=${ITC_NOTES_DIR:-dev-notes/itc-runs}/$R.md
P=${ITC_PROMPT:-/home/choong/tautest/${TASK}_prompt.txt}
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
sha=$(WANT_MODEL=$want WANT_TASK=$TASK python3 - "$H/meta.json" "$P" "$here" <<'PY'
import os
import json, sys
sys.path.insert(0, sys.argv[3])
from launchargs import split
m = json.load(open(sys.argv[1]))
task = m.get("task") or "itc"
assert task == os.environ["WANT_TASK"], f"meta task {task!r} != {os.environ['WANT_TASK']!r}, the task this run was meant for"
assert m.get("wall_cap_s") == 3600, f"wall_cap_s {m.get('wall_cap_s')!r} != 3600"
assert m.get("tau_dirty_files") == 0, f"tau_dirty_files {m.get('tau_dirty_files')!r} != 0"
model = m.get("model")
assert model, "no model recorded"
assert model == os.environ["WANT_MODEL"], f"meta model {model!r} != {os.environ['WANT_MODEL']!r}, the model this run was meant for"
argv = split(m.get("launch_command") or "")
assert argv, "no launch_command recorded"
pairs = list(zip(argv, argv[1:]))
assert (b"--model", model.encode()) in pairs, f"launch_command has no '--model {model}'"
assert argv[-1] == open(sys.argv[2], "rb").read(), "launch_command's prompt differs from " + sys.argv[2]
print(m["tau_sha"])
PY
)
python3 - "$H/meta.json" "$H/scorecard.json" "$f" "$R" <<'PY'
import json, sys
m = json.load(open(sys.argv[1])); c = json.load(open(sys.argv[2]))
lines = open(sys.argv[3]).read().split("\n")
R = sys.argv[4]
task = m.get("task") or "itc"
want = f"# {R} — {m['model']} — {task}_prompt.txt"
assert lines[0] == want, f"{R}.md header {lines[0]!r} != {want!r}"
para = []
for line in lines[1:]:
    if line.strip():
        para.append(line)
    elif para:
        break
sha7 = f"tau {m['tau_sha'][:7]}"
assert sha7 in " ".join(para), f"{R}.md summary paragraph does not name {sha7!r}"
ts = c.get("first_commit_ts")
unfounded = c.get("founded") is False and c.get("commits") == 0 and c.get("record_commits") == 0
if ts is None:
    assert unfounded, "scorecard.json first_commit_ts is null or missing: no root commit recorded"
else:
    assert m.get("start") is not None, "meta.json has no start"
    assert ts >= m["start"] - 5, f"first_commit_ts {ts} is before meta.start {m['start']} - 5: the project did not start clean"
PY
git -C "$T" cat-file -e "$sha^{commit}" 2>/dev/null || { echo "tau_sha $sha is not a commit in $T" >&2; exit 1; }
echo OK
