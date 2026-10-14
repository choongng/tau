#!/bin/bash
# T0319: no check a task binds (done_when in .beagle/tree/T*.md) carries a
# '! cmd' line, which set -e never fails on, except superseded T0245's and a retired
# task's (no longer live; T0565). A bound
# script that calls another check (bash .beagle/checks/...) is read too. The
# three amended checks still pass.
set -eu
python3 - <<'PY'
import glob, re, pathlib
bound = set()
for t in glob.glob(".beagle/tree/T*.md"):
    if t.endswith("T0245.md") or re.search(r'^retired_by = "T\d+"$', pathlib.Path(t).read_text(), re.M):
        continue
    m = re.search(r'^done_when = "(.*)"$', pathlib.Path(t).read_text(), re.M)
    if m:
        bound |= set(re.findall(r"\.beagle/checks/[\w/.-]+\.sh", m.group(1)))
todo, seen, bad = list(bound), set(), []
while todo:
    p = todo.pop()
    if p in seen or not pathlib.Path(p).is_file():
        continue
    seen.add(p)
    text = pathlib.Path(p).read_text()
    if re.search(r"^\s*! ", text, re.M):
        bad.append(p)
    todo += re.findall(r"\.beagle/checks/[\w/.-]+\.sh", text)
assert len(seen) > 100, f"only {len(seen)} bound checks found"
assert not bad, "bound checks with a '! cmd' line: " + ", ".join(sorted(bad))
print(f"{len(seen)} bound checks, none with a '! cmd' line")
PY
for s in T0054/T0054.sh T0128/T0128.sh T0226/T0226.v2.sh; do bash .beagle/checks/$s >/dev/null; done
echo OK
