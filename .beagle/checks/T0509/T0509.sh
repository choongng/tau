#!/bin/bash
# T0509: `contract check` runs the acceptance and wants every entry reported by
# id; `contract run --operation` judges one operation's entries by those lines.
# R86's own accept.sh (it crashes before any entry) must be refused.
set -e
W=/home/choong/beagle-wt/contract-run-ops
BEAGLE=$W/plugins/beagle-pursuit/bin/beagle
here=/home/choong/tautest/tau/.beagle/checks/T0509
(cd $W/plugins/beagle-pursuit/tooling/beagle &&
 UV_PROJECT_ENVIRONMENT=$HOME/.cache/beagle/venv-ops PYTHONPYCACHEPREFIX=$HOME/.cache/beagle/pycache-ops \
 uv run --quiet --with pytest --extra browser python -m pytest tests/test_contract.py -q -p no:cacheprovider \
   -k "verdicts or wants_every or judges" 2>&1 | tail -1 | tee /dev/stderr | grep -qE '^3 passed')
t=$(mktemp -d); trap 'rm -rf "$t"' EXIT
mkdir -p "$t/.beagle" "$t/contract"
cp -r "$here/r86/references" "$t/"
cp "$here"/r86/*.json "$here/r86/accept.sh" "$t/contract/"
printf '[goal]\nstatement="x"\ncriteria=["y"]\n[contract]\npath="contract/contract.json"\nsecond="contract/contract.second.json"\nacceptance="sh contract/accept.sh"\nfiles=["contract/"]\n' > "$t/.beagle/pursuit.toml"
(cd "$t" && git init -q)
out=$(cd "$t" && "$BEAGLE" pursuit contract check 2>&1) && { echo "R86's acceptance passed the check"; exit 1; }
echo "$out" | grep -E "the acceptance .* reported 0 of [0-9]+ entries" | tee /dev/stderr | grep -q "No module named 'cobs'"
