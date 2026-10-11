#!/bin/bash
# T0399: mining.md carries the generated findings table, and every finding has a
# disposition that resolves: fixed (a commit and a test that exist), a filed task,
# deferred, not live or not a bug (each with its reason).
set -e
H=/home/choong/tautest/itc-harness
TAU=/home/choong/tautest/tau
MD=$TAU/dev-notes/itc-runs/mining.md
cd $H
python3 -m pytest -q mine/test_findings.py
OUT=$(mktemp -d)
python3 mine/events.py --runs runs --out "$OUT/events.jsonl"
python3 mine/refusals.py --events "$OUT/events.jsonl" --out "$OUT/refusals.json" --rows "$OUT/refused.jsonl"
python3 mine/contradictions.py --events "$OUT/events.jsonl" --refused "$OUT/refused.jsonl" --kinds "$OUT/refusals.json" --out "$OUT/contra.json"
python3 mine/indicators.py --events "$OUT/events.jsonl" --refused "$OUT/refused.jsonl" --kinds "$OUT/refusals.json" --out "$OUT/ind.json"
python3 mine/findings.py --kinds "$OUT/refusals.json" --contradictions "$OUT/contra.json" --indicators "$OUT/ind.json" \
  --dispositions mine/dispositions.json --out "$OUT/findings.json" --table "$OUT/table.md"
python3 - "$OUT" "$MD" "$TAU" <<'PY'
import json, os, re, subprocess, sys
out, md, tau = sys.argv[1:4]
f = json.load(open(f"{out}/findings.json"))
kinds = {k["id"]: k for k in json.load(open(f"{out}/refusals.json"))["kinds"]}
contra = json.load(open(f"{out}/contra.json"))
ind = json.load(open(f"{out}/ind.json"))
assert len(f) >= 15, f"only {len(f)} findings"
for x in f:
    for k in ("id", "rank", "class", "title", "count", "runs", "models", "live", "lines", "disposition"):
        assert k in x, f"{x.get('id')}: lacks {k}"
    assert x["count"] >= 1 and x["runs"] and x["models"] and x["lines"], x["id"]
assert [x["rank"] for x in f] == list(range(1, len(f) + 1)), "ranks not 1..n in order"
classes = {x["class"] for x in f}
for need in ("offered_then_refused", "repeated", "alternating", "unrecovered", "worker_outcome", "stop", "driver_work", "time_sink"):
    assert need in classes, f"no finding of class {need}"
# counts recomputed from the scripts' own outputs
pairs = {}
for o in contra["offered_then_refused"]:
    pairs.setdefault(tuple(o["kinds"]), 0)
    pairs[tuple(o["kinds"])] += 1
for x in f:
    if x["class"] == "offered_then_refused":
        assert pairs.get(tuple(x["kinds"])) == x["count"], f"{x['id']} count {x['count']} != {pairs.get(tuple(x['kinds']))}"
    if x["class"] == "unrecovered":
        assert ind["recovery"][x["kinds"][0]]["unrecovered"] == x["count"], x["id"]
    if x["class"] in ("offered_then_refused", "repeated", "alternating", "unrecovered"):
        assert all(k in kinds for k in x["kinds"]), f"{x['id']}: unknown kind"
        if any(not kinds[k]["live"] for k in x["kinds"]):
            assert x["live"] is False, f"{x['id']}: a kind no source produces cannot be live"
# every offered_then_refused pair seen twice or more is a finding
for p, n in pairs.items():
    if n >= 2:
        assert any(x["class"] == "offered_then_refused" and tuple(x["kinds"]) == p for x in f), f"pair {p} ({n}) has no finding"
# dispositions resolve
tree = os.path.join(tau, ".beagle/tree")
def git_has(repo, sha):
    return subprocess.run(["git", "-C", repo, "cat-file", "-e", sha + "^{commit}"], capture_output=True).returncode == 0
def test_exists(name):
    return subprocess.run(["grep", "-rqw", f"def {name}", f"{tau}/tests", f"{os.path.expanduser('~/beagle')}/plugins",
                           "/home/choong/tautest/itc-harness/mine"], capture_output=True).returncode == 0
for x in f:
    d = x["disposition"]
    kind = d.get("kind")
    assert kind in ("fixed", "task", "deferred", "not_live", "not_a_bug"), f"{x['id']}: disposition {d}"
    if kind == "fixed":
        assert git_has(tau, d["commit"]) or git_has(os.path.expanduser("~/beagle"), d["commit"]), f"{x['id']}: no commit {d['commit']}"
        assert test_exists(d["test"]), f"{x['id']}: no test {d['test']}"
    elif kind == "task":
        assert os.path.exists(f"{tree}/{d['task']}.md"), f"{x['id']}: no task {d['task']}"
    else:
        assert len(d.get("reason", "")) >= 40, f"{x['id']}: {kind} needs a reason of 40+ chars"
    if x["live"]:
        assert kind in ("fixed", "task", "deferred", "not_a_bug"), f"{x['id']}: live but {kind}"
    if kind == "not_live":
        assert re.search(r"[\w/.-]+\.py:\d+|[0-9a-f]{7,40}", d["reason"]), f"{x['id']}: not_live without file:line or commit"
# mining.md holds the generated table verbatim, and its sections
text = open(md).read()
for line in open(f"{out}/table.md").read().splitlines():
    if line.strip():
        assert line in text, f"mining.md lacks table line: {line[:100]}"
for h in ("## How to rerun", "## Known answers", "## Findings"):
    assert h in text, f"mining.md lacks {h}"
for script in ("events.py", "refusals.py", "contradictions.py", "indicators.py", "findings.py"):
    assert script in text, f"mining.md does not say how to run {script}"
print(f"OK {len(f)} findings, {sum(x['live'] for x in f)} live; dispositions " +
      str({k: sum(x['disposition']['kind'] == k for x in f) for k in ('fixed','task','deferred','not_live','not_a_bug')}))
PY
rm -rf "$OUT"
python3 -m ruff check mine/ 2>/dev/null || uvx ruff check mine/
