#!/bin/bash
# T0600: tau's beagle extension is exercised against the real, pinned beagle
# 0.48 CLI (not the fake beagle the unit tests use): founding, planning and a
# pursuit_step's open and close, with a stub worker. Marked real_beagle; none
# may skip, since a skipped real test passes vacuously.
set -euo pipefail
W=/home/choong/tautest/tau-wt-048
cd "$W"
[ "$(git branch --show-current)" = beagle-0.48 ]
grep -rqs 'beagle-wt/0.48' tests/
PATH=$(echo "$PATH" | tr ':' '\n' | grep -v '/beagle/venv' | paste -sd:)
out=$(timeout 600 .venv/bin/python -m pytest -q --no-header -p no:cacheprovider -m real_beagle -rs tests/ 2>&1 | tail -15)
echo "$out" >&2
last=$(echo "$out" | tail -1)
n=$(echo "$last" | grep -oE '^[0-9]+ passed' | grep -oE '^[0-9]+' || echo 0)
[ "$n" -ge 3 ]
if echo "$last" | grep -qE 'failed|error|skipped'; then echo "real_beagle: $last" >&2; exit 1; fi
for k in found step close; do
  timeout 600 .venv/bin/python -m pytest -q --no-header -p no:cacheprovider -m real_beagle --collect-only -q tests/ 2>/dev/null | grep -qi "$k" || { echo "no real_beagle test named for $k" >&2; exit 1; }
done
out=$(timeout 840 .venv/bin/python -m pytest -q --no-header -p no:cacheprovider tests/test_beagle_example_extension.py 2>&1 | tail -1)
echo "$out" >&2
echo "$out" | grep -qE '^[0-9]+ passed' && ! echo "$out" | grep -qE 'failed|error'
