#!/bin/bash
# Audit 12 (T0335): every test a run note names on its Tests: lines exists.
# `tests/f.py::test_x` names a test in f; a bare `::test_y` after it means the
# same file. Checks R36-R38, whose fixes are all built.
set -eu
python3 - dev-notes/itc-runs/R36.md dev-notes/itc-runs/R37.md dev-notes/itc-runs/R38.md <<'PY'
import re, sys, pathlib
missing, seen = [], 0
for note in sys.argv[1:]:
    for line in open(note):
        if not line.startswith("Tests:"):
            continue
        current = None
        for m in re.finditer(r"(tests/[\w/]+\.py)?::(test_\w+)", line):
            current = m.group(1) or current
            assert current, f"{note}: bare ::{m.group(2)} with no file before it"
            seen += 1
            p = pathlib.Path(current)
            if not p.is_file() or not re.search(rf"^(async )?def {m.group(2)}\(", p.read_text(), re.M):
                missing.append(f"{note}: {current}::{m.group(2)}")
assert seen, "no test names found on Tests: lines"
assert not missing, "named tests that do not exist:\n  " + "\n  ".join(missing)
print(f"OK: {seen} named tests resolve")
PY
