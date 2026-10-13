#!/bin/bash
# T0516: the second extraction is independent. Founding seeds Contract, Second
# extraction and Reconcile; pursuit_step gives each its scope and check; the guard
# keeps the second's worker from the first and every other worker from the second;
# beagle briefs the second to its own check and the full check names whose it is.
set -e
B=/home/choong/beagle-wt/contract-first/plugins/beagle-pursuit/tooling/beagle
BEAGLE=/home/choong/beagle-wt/contract-first/plugins/beagle-pursuit/bin/beagle
cd /home/choong/tautest/tau
uv run --quiet pytest -q -p no:cacheprovider tests/test_beagle_example_extension.py \
  -k "second_extraction_reads_nothing or only_the_second_extraction or scopes_the_contract_milestones or founding_declares_the_contract" \
  2>&1 | tail -1 | tee /dev/stderr | grep -qE '^4 passed'
t=$(mktemp -d); trap 'rm -rf "$t"' EXIT
mkdir -p "$t/references" "$t/.beagle" "$t/contract"
cp .beagle/checks/T0513/r82/cobs.txt "$t/references/"
printf '[goal]\nstatement="x"\ncriteria=["y"]\n[contract]\npath="contract/contract.json"\nsecond="contract/contract.second.json"\nfiles=["contract/"]\n' > "$t/.beagle/pursuit.toml"
(cd "$t" && git init -q)
at=$(cd "$t" && "$BEAGLE" pursuit contract refs cobs --grep "11 22 00 33" | head -1 | sed -E 's/\| .*//')
(cd "$t" && "$BEAGLE" pursuit contract add >/dev/null <<J || true
[{"id": "ex-4", "kind": "example", "operation": "encode", "source": "cobs", "cite": "$at",
  "input": {"hex": "11 22 00 33"}, "expect": {"hex": "03 11 22 02 33 00"}}]
J
)
out=$(cd "$t" && "$BEAGLE" pursuit contract check 2>&1 || true)
echo "$out" | grep -qF "in a task of its own, not by this one" || { echo "$out"; exit 1; }
cd "$B"
UV_PROJECT_ENVIRONMENT=$HOME/.cache/beagle-cf-venv uv run --with pytest pytest -q -p no:cacheprovider \
  --basetemp=$HOME/.cache/beagle-pytest/T0516 tests/test_contract.py -k "second" 2>&1 | tail -1 | tee /dev/stderr | grep -qE '^[0-9]+ passed'
find "$B" -name __pycache__ -prune -exec rm -rf {} +
echo "T0516: the second extraction is scoped to itself, kept from the first, and the only writer of the second"
