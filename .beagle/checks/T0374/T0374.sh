#!/bin/bash
# R42 diagnose: v8 diagnosed.sh, plus every failure class says which earlier
# runs and models it also appeared in, and (audit 12) every [tau] class names
# at least one test function (tests/....py::test_...), not only a file.
set -eu
bash .beagle/checks/runs/v8/diagnosed.sh R42
python3 - dev-notes/itc-runs/R42.md <<'PY'
import re, sys
md = open(sys.argv[1]).read()
sec = re.split(r"^## ", md.split("\n## Failure classes", 1)[1], maxsplit=1, flags=re.M)[0]
classes = re.split(r"^(?=### )", sec, flags=re.M)[1:]
assert classes, "no ### failure classes"
bad = [c.splitlines()[0] for c in classes if not re.search(r"^Seen in: \S", c, re.M)]
assert not bad, "classes without 'Seen in:': " + "; ".join(bad)
untested = [c.splitlines()[0] for c in classes
            if "[tau]" in c.splitlines()[0] and not re.search(r"tests/[\w/]+\.py::test_\w+", c)]
assert not untested, "[tau] classes naming no test function: " + "; ".join(untested)
print("OK")
PY
# R42 is the first run with R41's fixes T0370-T0372 in
for t in T0370 T0371 T0372; do grep -q "$t" dev-notes/itc-runs/R42.md || { echo "R42.md does not say what $t did"; exit 1; }; done
