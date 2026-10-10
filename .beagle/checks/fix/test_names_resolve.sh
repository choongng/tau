#!/bin/bash
# usage: test_names_resolve.sh NOTE.md... — every test a run note names on its
# Tests: lines exists. `tests/f.py::test_x` names a test in f; a bare
# `::test_y` after it means the same file. A name resolves in tau, or in the
# tau-subagents extension repo (its tests are named the same way).
set -eu
python3 - "$@" <<'PY'
import re, sys, pathlib
roots = [pathlib.Path("."), pathlib.Path.home() / ".tau/extensions/tau-subagents"]
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
            pat = re.compile(rf"^\s*(async )?def {m.group(2)}\(", re.M)
            if not any((r / current).is_file() and pat.search((r / current).read_text()) for r in roots):
                missing.append(f"{note}: {current}::{m.group(2)}")
assert seen, "no test names found on Tests: lines"
assert not missing, "named tests that do not exist:\n  " + "\n  ".join(missing)
print(f"OK: {seen} named tests resolve")
PY
