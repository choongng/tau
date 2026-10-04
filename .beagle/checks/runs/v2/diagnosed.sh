#!/bin/bash
# usage: diagnosed.sh RNN — runs/diagnosed.sh, plus: the run is in upstream.md
# (or says 'upstream: none'), every class cites Evidence:, and every [tau]
# class's Action names beagle.py, a tests/ path or a src/ path.
# env: ITC_NOTES_DIR (run notes).
set -eu
R=$1; N=${ITC_NOTES_DIR:-dev-notes/itc-runs}; f=$N/$R.md
grep -q '^## Trace analysis' "$f"
grep -q '^## Failure classes' "$f"
n=$(sed -n '/^## Failure classes/,/^## /p' "$f" | { grep -cE '^### \[(tau|beagle|model|harness)\] ' || true; })
test "$n" -ge 1
# every class says what is done about it
m=$(sed -n '/^## Failure classes/,/^## /p' "$f" | { grep -cE '^(Action|Disposition): ' || true; })
test "$m" -ge "$n"
grep -qE "^## $R\b" "$N/upstream.md" 2>/dev/null || grep -q 'upstream: none' "$f" \
  || { echo "$R has no '## $R' in upstream.md and does not say 'upstream: none'" >&2; exit 1; }
python3 - "$f" <<'PY'
import re, sys
md = open(sys.argv[1]).read()
sec = re.split(r"^## ", md.split("\n## Failure classes", 1)[1], maxsplit=1, flags=re.M)[0]
classes = re.split(r"^(?=### )", sec, flags=re.M)[1:]
bad = []
for c in classes:
    head = c.splitlines()[0]
    if not re.search(r"^Evidence: ", c, re.M):
        bad.append(f"no Evidence: line in {head}")
    if head.startswith("### [tau]"):
        a = re.search(r"^Action: (.*?)(?=^(?:Evidence|Action|Disposition): |\Z)", c, re.M | re.S)
        if not a or not re.search(r"beagle\.py|\btests/|\bsrc/", a.group(1)):
            bad.append(f"Action names no beagle.py, tests/ or src/ path in {head}")
assert not bad, "\n".join(bad)
PY
echo OK
