#!/bin/bash
# Audit 14 fix: every _scope_has_data caller sees data under a directory scope
set -e
T=tests/test_beagle_example_extension.py
F=examples/extensions/beagle.py
bash .beagle/checks/fix/named_tests.sh $T 2 test_directory_scope_data_reaches_every_scope_has_data_route test_data_test_unwritten_import_on_a_directory_scope
# No caller that has a project root left calling without it.
python3 - "$F" <<'PY'
import ast, sys
tree = ast.parse(open(sys.argv[1]).read())
bare = []
for fn in ast.walk(tree):
    if not isinstance(fn, (ast.FunctionDef, ast.AsyncFunctionDef)) or fn.name in ("_scope_has_data", "_scope_data"):
        continue
    names = {a.arg for a in fn.args.args + fn.args.kwonlyargs} | {n.id for n in ast.walk(fn) if isinstance(n, ast.Name) and isinstance(n.ctx, ast.Store)}
    if "root" not in names:
        continue
    for c in ast.walk(fn):
        if isinstance(c, ast.Call) and getattr(c.func, "id", None) == "_scope_has_data":
            if len(c.args) < 2 and not any(k.arg == "root" for k in c.keywords):
                bare.append((fn.name, c.lineno))
assert not bare, f"_scope_has_data called without root where root is in reach: {bare}"
print("OK every _scope_has_data call with root in reach passes it")
PY
uv run pytest -q $T
uv run ruff check $F $T
