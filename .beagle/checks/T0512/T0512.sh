#!/bin/bash
# T0512: an operation entry naming a signature is exercised by examples naming the
# bare operation, and the refusal for one truly unexercised says what was compared.
set -e
B=/home/choong/beagle-wt/contract-first/plugins/beagle-pursuit/tooling/beagle
BEAGLE=/home/choong/beagle-wt/contract-first/plugins/beagle-pursuit/bin/beagle
SRC=/home/choong/tautest/tau/.beagle/checks/T0513/r82/cobs.txt
t=$(mktemp -d); trap 'rm -rf "$t"' EXIT
mkdir -p "$t/references" "$t/.beagle"
cp "$SRC" "$t/references/"
printf '[goal]\nstatement="x"\ncriteria=["y"]\n[contract]\npath="contract/contract.json"\nfiles=["contract/"]\n' > "$t/.beagle/pursuit.toml"
(cd "$t" && git init -q)
at=$(cd "$t" && "$BEAGLE" pursuit contract refs cobs --grep "11 22 00 33" | head -1 | sed -E 's/\| .*//')
# R82's shape: the operation by signature, its examples by bare name.
(cd "$t" && "$BEAGLE" pursuit contract add >/dev/null <<J || true
[{"id": "op-encode", "kind": "operation", "operation": "encode(data: bytes) -> bytes",
  "source": "cobs", "cite": "$at", "statement": "stuffs the zero bytes out"},
 {"id": "op-decode", "kind": "operation", "operation": "decode(data: bytes) -> bytes",
  "source": "cobs", "cite": "$at", "statement": "restores them"},
 {"id": "ex-4", "kind": "example", "operation": "encode", "source": "cobs", "cite": "$at",
  "input": {"hex": "11 22 00 33"}, "expect": {"hex": "03 11 22 02 33 00"}}]
J
)
out=$(cd "$t" && "$BEAGLE" pursuit contract check --draft 2>&1 || true)
echo "$out" | grep -q "operation encode(data: bytes)" && { echo "$out"; exit 1; }
echo "$out" | grep -qF "operation decode(data: bytes) -> bytes (op-decode) is defined and nothing exercises it" || { echo "$out"; exit 1; }
echo "$out" | grep -qF "(Compared by bare name, 'decode'; the examples, limits, invalid inputs and properties name: encode.)" || { echo "$out"; exit 1; }
cd "$B"
UV_PROJECT_ENVIRONMENT=$HOME/.cache/beagle-cf-venv uv run --with pytest pytest -q -p no:cacheprovider \
  --basetemp=$HOME/.cache/beagle-pytest/T0512 tests/test_contract.py -k "operation or second" 2>&1 | tail -1 | tee /dev/stderr | grep -qE '^[0-9]+ passed'
find "$B" -name __pycache__ -prune -exec rm -rf {} +
echo "T0512: operations match by bare name; the refusal names what it compared"
