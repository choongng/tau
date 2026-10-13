#!/bin/bash
# T0514: the declared second extraction is a listing (id, kind, operation, source,
# cite), held to its cites and compared as before, and not to inputs, results or
# statements; the contract still is; both briefs say so.
set -e
B=/home/choong/beagle-wt/contract-first/plugins/beagle-pursuit/tooling/beagle
BEAGLE=/home/choong/beagle-wt/contract-first/plugins/beagle-pursuit/bin/beagle
SRC=/home/choong/tautest/tau/.beagle/checks/T0513/r82/cobs.txt
t=$(mktemp -d); trap 'rm -rf "$t"' EXIT
mkdir -p "$t/references" "$t/.beagle"
cp "$SRC" "$t/references/"
printf '[goal]\nstatement="x"\ncriteria=["y"]\n[contract]\npath="contract/contract.json"\nsecond="contract/contract.second.json"\nfiles=["contract/"]\n' > "$t/.beagle/pursuit.toml"
(cd "$t" && git init -q)
at=$(cd "$t" && "$BEAGLE" pursuit contract refs cobs --grep "11 22 00 33" | head -1 | sed -E 's/\| .*//')
item='{"id": "L1", "kind": "example", "operation": "encode", "source": "cobs", "cite": "'"$at"'"}'
# Listed in the second: added, and the second checks clean on its own.
out=$(cd "$t" && echo "$item" | "$BEAGLE" pursuit contract add --file contract/contract.second.json) || { echo "$out"; exit 1; }
echo "$out" | grep -q "^added L1 (example of encode, line ${at%%#*}: "
(cd "$t" && "$BEAGLE" pursuit contract check --file contract/contract.second.json)
# The same bare entry in the contract itself is refused: it needs its input and result.
rc=0; out=$(cd "$t" && echo "$item" | "$BEAGLE" pursuit contract add) || rc=$?
[ "$rc" = 1 ] || { echo "$out"; exit 1; }
echo "$out" | grep -q "^refused L1, not added:"
# And the listing still has to be covered: with the contract citing another
# passage only, the full check names L1's line.
other=$(cd "$t" && "$BEAGLE" pursuit contract refs cobs --grep "11 22 33 44" | head -1 | sed -E 's/\| .*//')
(cd "$t" && "$BEAGLE" pursuit contract add <<J
{"id": "E1", "kind": "example", "operation": "encode", "source": "cobs", "cite": "$other",
 "input": {"hex": "11 22 33 44"}, "expect": {"hex": "05 11 22 33 44 00"}}
J
) | grep -q "^added E1"
rc=0; out=$(cd "$t" && "$BEAGLE" pursuit contract check 2>&1) || rc=$?
echo "$out" | grep -q "second extraction's entry L1 cites references/cobs.txt line ${at%%#*}" || { echo "$out"; exit 1; }
cd "$B"
UV_PROJECT_ENVIRONMENT=$HOME/.cache/beagle-cf-venv uv run --with pytest pytest -q -p no:cacheprovider \
  --basetemp=$HOME/.cache/beagle-pytest/T0514 tests/test_contract.py -k "second" 2>&1 | tail -1 | tee /dev/stderr | grep -qE '^5 passed'
grep -q 'is a listing, not a second contract' src/beagle/contract.py
find "$B" -name __pycache__ -prune -exec rm -rf {} +
cd /home/choong/tautest/tau
uv run pytest -q -p no:cacheprovider tests/test_beagle_example_extension.py \
  -k "founding_declares_the_contract_and_seeds_it_first" 2>&1 | tail -1 | tee /dev/stderr | grep -qE "^1 passed"
grep -q "each entry only an id, kind, operation, source and line-anchor cite" tests/test_beagle_example_extension.py
echo "T0514: the second extraction lists by anchor; the contract keeps its full entries"
