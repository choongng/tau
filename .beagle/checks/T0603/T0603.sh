#!/bin/bash
# T0603: the extension's policy text is sorted by who carries it under 0.48
# ("beagle decides, hosts carry"): dev-notes/beagle-0.48/decide-carry.md has
# one table row per audited text, | `<name or phrase>` | <where> | deleted|kept|ask | <why> |.
# Each `deleted` row's backticked text is absent from the extension; each
# `ask` row is filed in upstream-asks.md; the suites still pass.
set -euo pipefail
W=/home/choong/tautest/tau-wt-048
E=$W/examples/extensions/beagle.py
D=$W/dev-notes/beagle-0.48/decide-carry.md
A=$W/dev-notes/beagle-0.48/upstream-asks.md
cd "$W"
[ "$(git branch --show-current)" = beagle-0.48 ]
python3 - "$E" "$D" "$A" <<'PY'
import re, sys
ext, doc, asks = (open(p).read() for p in sys.argv[1:4])
rows = [r for r in doc.splitlines() if re.match(r"^\|\s*`", r)]
verdicts = {}
for r in rows:
    cells = [c.strip() for c in r.strip().strip("|").split("|")]
    if len(cells) < 4 or cells[2] not in ("deleted", "kept", "ask"):
        sys.exit(f"bad row: {r}")
    verdicts.setdefault(cells[2], []).append(cells)
if len(rows) < 8:
    sys.exit(f"only {len(rows)} audited rows")
for cells in verdicts.get("deleted", []):
    for name in re.findall(r"`([^`]+)`", cells[0]):
        if name in ext:
            sys.exit(f"deleted, but still in the extension: {name}")
n_asks = len(re.findall(r"^## \d+\.", asks, re.M))
if n_asks < 3 + len(verdicts.get("ask", [])) or "dispatch role" not in asks:
    sys.exit(f"upstream-asks.md has {n_asks} asks; the ask rows and the cases dispatch role need filing")
print(f"{len(rows)} rows: " + ", ".join(f"{k} {len(v)}" for k, v in verdicts.items()), file=sys.stderr)
PY
PATH=$(echo "$PATH" | tr ':' '\n' | grep -v '/beagle/venv' | paste -sd:)
py() { timeout 900 .venv/bin/python -m pytest -q --no-header -p no:cacheprovider "$@" 2>&1 | tail -1; }
for sel in "-m real_beagle tests/" "tests/test_beagle_example_extension.py"; do
  out=$(py $sel); echo "$sel -> $out" >&2
  echo "$out" | grep -qE '^[1-9][0-9]* passed' || exit 1
  if echo "$out" | grep -qE 'failed|error|skipped'; then exit 1; fi
done
