#!/bin/bash
# Baseline comparison: baselines.md tabulates B01-B03 beside the same model+prompt pursuit runs, with grades matching each run's grade.json, and says what that implies and what to do for R41-R50
set -eu
f=dev-notes/itc-runs/baselines.md
H=/home/choong/tautest/itc-harness/runs
test -f $f || { echo "no $f"; exit 1; }
python3 - "$f" "$H" <<'PY'
import json, re, sys
md, runs = open(sys.argv[1]).read(), sys.argv[2]
for sec in ("## Comparison", "## What it implies", "## Recommendation for R41-R50"):
    assert sec in md, f"missing section {sec}"
table = md.split("## Comparison", 1)[1].split("\n## ", 1)[0]
rows = {m.group(1): m.group(0) for m in re.finditer(r"^\|\s*((?:B|R)\d\d)\b.*$", table, re.M)}
for b in ("B01", "B02", "B03"):
    assert b in rows, f"{b} not a row of the comparison table"
pursuit = [r for r in rows if r.startswith("R")]
assert len(pursuit) >= 3, f"only {len(pursuit)} pursuit rows"
for r, line in rows.items():
    try:
        g = json.load(open(f"{runs}/{r}/grade.json"))
    except FileNotFoundError:
        continue
    passed, total = g.get("passed"), g.get("total")
    if passed is None or total is None:
        continue
    assert f"{passed}/{total}" in line, f"{r}: row does not show its grade {passed}/{total}: {line}"
for col in ("stage", "wall", "ended"):
    assert re.search(col, table.splitlines()[next(i for i, l in enumerate(table.splitlines()) if l.startswith("|"))], re.I), f"table header lacks {col}"
print("OK")
PY
