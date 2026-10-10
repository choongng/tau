#!/bin/bash
# R38 diagnose: v6 diagnosed.sh, plus (criterion 2, 2026-10-09) every failure
# class says which earlier runs and models it also appeared in.
set -eu
bash .beagle/checks/runs/v7/diagnosed.sh R38
python3 - dev-notes/itc-runs/R38.md <<'PY'
import re, sys
md = open(sys.argv[1]).read()
sec = re.split(r"^## ", md.split("\n## Failure classes", 1)[1], maxsplit=1, flags=re.M)[0]
classes = re.split(r"^(?=### )", sec, flags=re.M)[1:]
bad = [c.splitlines()[0] for c in classes if not re.search(r"^Seen in: \S", c, re.M)]
assert not bad, "classes without 'Seen in:': " + "; ".join(bad)
print("OK")
PY
