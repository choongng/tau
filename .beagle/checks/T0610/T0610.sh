# T0610: all 30 round-robin rounds ran, were graded, and have an eval.md row.
python3 - <<'PY'
import re
rr = open("dev-notes/beagle-0.48/round-robin.md").read()
rows = [r for r in rr.splitlines() if re.match(r"\| \d+ \| R1\d\d \|", r)]
assert len(rows) == 30, len(rows)
unfilled = [r.split("|")[2].strip() for r in rows if not r.split("|")[5].strip()]
assert not unfilled, f"rounds without a result: {unfilled}"
ev = open("dev-notes/contract-first/eval.md").read()
missing = [f"R{n}" for n in range(104, 134) if not re.search(rf"^\| R{n} \|", ev, re.M)]
assert not missing, f"no eval.md row: {missing}"
PY
