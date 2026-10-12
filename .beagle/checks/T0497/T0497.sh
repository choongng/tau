#!/bin/bash
# T0497: a worked-example table row is quotable as it stands (R71's contract sink).
set -e
WT=/home/choong/beagle-wt/contract-first
B=$WT/plugins/beagle-pursuit/tooling/beagle
# R71's own reference and contract (copied from ~/wrenfold.r71), with each example quoting its table row alone.
tmp=$(mktemp -d "$HOME/.cache/t0497.XXXXXX"); trap 'rm -rf "$tmp"' EXIT
cp -r "$(dirname "$0")/r71/." "$tmp/"
python3 - "$tmp/contract/contract.json" <<'PY'
import json, sys
p = sys.argv[1]; c = json.load(open(p))
rows = {"E001": "(none) | 3F", "E002": "0 | 00 3F", "E003": "5 | 05 3F", "E008": "2, 2, 2 | 02 02 02 3F"}
for e in c["entries"]:
    if e["id"] in rows: e["quote"] = rows[e["id"]]
json.dump(c, open(p, "w"), indent=1)
PY
(cd "$tmp" && "$WT/plugins/beagle-pursuit/bin/beagle" pursuit contract check --draft)
cd "$B"
export UV_PROJECT_ENVIRONMENT=$HOME/.cache/beagle-cf-venv
mkdir -p "$HOME/.cache/beagle-pytest"
uv run --with pytest pytest -q -p no:cacheprovider --basetemp="$HOME/.cache/beagle-pytest/T0497" \
  tests/test_contract.py::test_contract_quote_may_be_a_short_line_of_its_own_but_not_a_repeated_one tests/test_contract.py
find "$WT/plugins" -name __pycache__ -prune -exec rm -rf {} +
