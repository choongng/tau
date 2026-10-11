#!/bin/bash
# T0211: summary-R21-R44.md holds every run's row and the per model x prompt
# counts, recomputed here from the harness's own grade.json and meta.json, and
# its failure classes each cite runs and a commit that exists or say deferred.
set -e
TAU=/home/choong/tautest/tau
H=/home/choong/tautest/itc-harness
MD=$TAU/dev-notes/itc-runs/summary-R21-R44.md
test -f "$MD"
python3 - "$MD" "$H" "$TAU" <<'PY'
import json, os, re, subprocess, sys
md, h, tau = sys.argv[1:4]
text = open(md).read()
def model_short(m):
    for s in ("mimo", "qwen", "gemma"):
        if m.startswith(s):
            return s
    raise AssertionError(m)
def cells(line):
    return [c.strip().strip("`*") for c in line.strip().strip("|").split("|")]
rows = [cells(l) for l in text.splitlines() if l.startswith("|")]
def run_info(r):
    meta = json.load(open(f"{h}/runs/{r}/meta.json"))
    g = json.load(open(f"{h}/runs/{r}/grade.json"))
    dt = meta.get("driver_thinking")
    level = "off"
    if dt:
        level = re.search(r"'level': '(\w+)'", str(dt)).group(1) if "level" in str(dt) else str(dt)
    return model_short(meta["model"]), meta["task"], g["passed"], g["total"], level
runs = [f"R{n}" for n in range(21, 45)]
agg = {}
for r in runs:
    m, p, ok, tot, lvl = run_info(r)
    row = next((c for c in rows if c and c[0] == r), None)
    assert row, f"no table row for {r}"
    need = [m, p, f"{ok}/{tot}", lvl]
    for tok in need:
        assert tok in row, f"{r}: row {row} lacks {tok!r}"
    a = agg.setdefault((m, p), [0, 0, 0, (-1, tot)])
    a[0] += 1; a[1] += ok == tot; a[2] += ok > 0
    if ok > a[3][0]: a[3] = (ok, tot)
for (m, p), (n, comp, anyp, best) in sorted(agg.items()):
    want = [m, p, str(n), str(comp), str(anyp), f"{best[0]}/{best[1]}"]
    assert any(c[:6] == want for c in rows), f"no model x prompt row {want}"
for b in ("B01", "B02", "B03"):
    m, p, ok, tot, _ = run_info(b)
    row = next((c for c in rows if c and c[0] == b), None)
    assert row and m in row and p in row and f"{ok}/{tot}" in row, f"baseline {b}: {row}"
for head in ("## Runs", "## By model and prompt", "## Recurring failure classes",
             "## What carried across", "## What changed in tau"):
    assert re.search(rf"^{re.escape(head)}\b", text, re.M), f"no heading {head}"
assert re.search(r"R45.{0,80}(dropped|not run)|(dropped|not run).{0,80}R45", text, re.S), "does not say R45-R50 were dropped"
assert "mining.md" in text, "does not point at mining.md"
sec = re.search(r"^## Recurring failure classes\n(.*?)(?=^## )", text, re.S | re.M).group(1)
classes = re.split(r"^### ", sec, flags=re.M)[1:]
assert len(classes) >= 5, f"only {len(classes)} recurring classes"
repos = [tau, h, "/home/choong/beagle"]
def sha_ok(s):
    return any(subprocess.run(["git", "-C", d, "cat-file", "-e", f"{s}^{{commit}}"],
                              capture_output=True).returncode == 0 for d in repos)
for c in classes:
    name = c.splitlines()[0]
    cited = set(re.findall(r"\bR(2[1-9]|3\d|4[0-4])\b", c))
    assert len(cited) >= 2, f"class {name!r} cites {len(cited)} runs"
    shas = re.findall(r"`([0-9a-f]{7,12})`", c)
    assert shas or re.search(r"\bdeferred\b", c, re.I), f"class {name!r} names no fix commit and is not deferred"
for s in set(re.findall(r"`([0-9a-f]{7,12})`", text)):
    assert sha_ok(s), f"commit {s} not found in tau, itc-harness or beagle"
print(f"OK {len(runs)} runs, {len(agg)} model x prompt rows, {len(classes)} classes")
PY
