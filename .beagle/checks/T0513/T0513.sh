#!/bin/bash
# T0513: `contract add` checks each entry against its source as it lands and keeps
# only those that pass; a contract worker may run it and it counts as writing; the
# brief, the founding milestone and a cut-off whole-contract write all point at it.
set -e
B=/home/choong/beagle-wt/contract-first/plugins/beagle-pursuit/tooling/beagle
BEAGLE=/home/choong/beagle-wt/contract-first/plugins/beagle-pursuit/bin/beagle
HERE=/home/choong/tautest/tau/.beagle/checks/T0513
# A real source: R82's cobs reference. One entry right, one with a guessed anchor.
t=$(mktemp -d); trap 'rm -rf "$t"' EXIT
mkdir -p "$t/references" "$t/.beagle"
cp "$HERE/r82/cobs.txt" "$t/references/"
printf '[goal]\nstatement="x"\ncriteria=["y"]\n[contract]\npath="contract/contract.json"\nfiles=["contract/"]\n' > "$t/.beagle/pursuit.toml"
(cd "$t" && git init -q)
at=$(cd "$t" && "$BEAGLE" pursuit contract refs cobs --grep "11 22 00 33" | head -1 | sed -E 's/\| .*//')
rc=0
out=$(cd "$t" && "$BEAGLE" pursuit contract add <<J
[{"id": "ex-4", "kind": "example", "operation": "encode", "source": "cobs", "cite": "$at",
  "input": {"hex": "11 22 00 33"}, "expect": {"hex": "03 11 22 02 33 00"}},
 {"id": "ex-x", "kind": "example", "operation": "encode", "source": "cobs", "cite": "81#a00",
  "input": {"hex": "00"}, "expect": {"hex": "01 01 00"}}]
J
) || rc=$?
echo "$out"
[ "$rc" = 1 ]
echo "$out" | grep -q "^added ex-4 (example of encode, line ${at%%#*}: "
echo "$out" | grep -q "^refused ex-x, not added:"
echo "$out" | grep -q "line 81's anchor is 81#"
python3 -c "import json,sys; d=json.load(open('$t/contract/contract.json')); assert [e['id'] for e in d['entries']]==['ex-4'], d; assert d['sources']=={'cobs': {'path': 'references/cobs.txt'}}, d"
cd "$B"
UV_PROJECT_ENVIRONMENT=$HOME/.cache/beagle-cf-venv uv run --with pytest pytest -q -p no:cacheprovider \
  --basetemp=$HOME/.cache/beagle-pytest/T0513 tests/test_contract.py -k "contract_add" 2>&1 | tail -1 | tee /dev/stderr | grep -qE '^2 passed'
grep -q 'pursuit contract add`, which takes the JSON' src/beagle/contract.py
find "$B" -name __pycache__ -prune -exec rm -rf {} +
cd /home/choong/tautest/tau
uv run pytest -q -p no:cacheprovider tests/test_beagle_example_extension.py \
  -k "contract_worker_adds_entries_by_contract_add or contract_worker_reads_the_references_by_contract_refs or worker_guard_refuses_beagle_commands" \
  2>&1 | tail -1 | tee /dev/stderr | grep -qE '^3 passed'
echo "T0513: contract add checks each entry as it lands; workers may run it; briefs name it"
