#!/bin/bash
# T0503: a bare line-number cite is refused with the anchored cite and the text it names.
set -e
B=/home/choong/beagle-wt/contract-first/plugins/beagle-pursuit/tooling/beagle
BEAGLE=/home/choong/beagle-wt/contract-first/plugins/beagle-pursuit/bin/beagle
cd "$B"
UV_PROJECT_ENVIRONMENT=$HOME/.cache/beagle-cf-venv uv run --with pytest pytest -q -p no:cacheprovider \
  --basetemp=$HOME/.cache/beagle-pytest/T0503 tests/test_contract.py -k "cite or anchor or refs" 2>&1 | tail -2 | tee /dev/stderr | grep -qE '^[0-9]+ passed'
grep -q "bare_line_number_is_refused_with_the_anchor_to_cite" tests/test_contract.py
# A real source: R73's itc paper, line 350 of its PDF text.
t=$(mktemp -d); trap 'rm -rf "$t"' EXIT
mkdir -p "$t/references" "$t/contract" "$t/.beagle"
cp /home/choong/tautest/tau/.beagle/checks/T0498/r73/references/* "$t/references/"
cp /home/choong/tautest/tau/.beagle/checks/T0498/r73/.beagle/pursuit.toml "$t/.beagle/"
src=itc2008.txt; name=itc2008
cat > "$t/contract/contract.json" <<J
{"sources": {"$name": {"path": "references/$src"}},
 "entries": [{"id": "E001", "kind": "example", "operation": "x", "source": "$name",
              "cite": "350-351", "input": "a", "expect": "b"}]}
J
out=$(cd "$t" && "$BEAGLE" pursuit contract check --draft 2>&1 || true)
want=$(cd "$t" && "$BEAGLE" pursuit contract refs "$name" --lines 350-351 | sed -E 's/\| .*//' | paste -sd-)
echo "$out" | grep -F "is a line number, not an anchor: cite $want if" >/dev/null || { echo "$out" | grep E001; echo "want $want"; exit 1; }
find "$B" -name __pycache__ -prune -exec rm -rf {} +
echo "T0503: bare cite refused with $want and its text"
