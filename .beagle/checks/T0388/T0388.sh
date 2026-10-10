#!/bin/bash
# R44 diagnose: v8 diagnosed.sh, plus every failure class says which earlier
# runs and models it also appeared in, and (audit 12) every [tau] class names
# at least one test function (tests/....py::test_...), not only a file.
set -eu
bash .beagle/checks/runs/v8/diagnosed.sh R44
python3 - dev-notes/itc-runs/R44.md <<'PY'
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
# audit 10-10: the timeline, the questions, and each class's independence line
assert re.search(r"^### Timeline\s*\n(?:.*\n){3,}", md, re.M), "no ### Timeline with entries"
assert re.search(r"^### The questions\s*\n(?:.*\n){3,}", md, re.M), "no ### The questions with answers"
noind = [c.splitlines()[0] for c in classes if not re.search(r"^Prompt- and model-independent: \S", c, re.M)]
assert not noind, "classes without a 'Prompt- and model-independent:' line: " + "; ".join(noind)
print("OK")
PY
# R44 is the first run with R43's fixes T0382-T0385 in
for t in T0382 T0383 T0384 T0385; do grep -q "$t" dev-notes/itc-runs/R44.md || { echo "R44.md does not say what $t did"; exit 1; }; done
