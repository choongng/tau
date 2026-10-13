#!/bin/bash
# T0525: a case the acceptance cannot replay (an elided value, `01 02 ... FE`, or
# a description, `any input`) is a contract problem. R89's sealed contract is
# refused; R81's itc contract, 95 entries of real values, is not.
set -e
W=/home/choong/beagle-wt/contract-concrete-cases
here=/home/choong/tautest/tau/.beagle/checks/T0525
cd $W/plugins/beagle-pursuit/tooling/beagle
export UV_PROJECT_ENVIRONMENT=$HOME/.cache/beagle/venv-ops PYTHONPYCACHEPREFIX=$HOME/.cache/beagle/pycache-ops
uv run --quiet --with pytest --extra browser python -m pytest tests/test_contract.py -q -p no:cacheprovider \
  -k "cannot_replay" 2>&1 | tail -1 | tee /dev/stderr | grep -qE '^1 passed'
uv run --quiet python - "$here" <<'PY'
import json, sys
from beagle import contract
def refused(name):
    n = 0
    for e in json.load(open(f"{sys.argv[1]}/{name}"))["entries"]:
        if e.get("kind") in contract.CASE_KINDS and "input" in e and "expect" in e:
            n += len(contract._case_value_problems(e, e["id"], e["kind"]))
    return n
r89, r81 = refused("r89-contract.json"), refused("r81-itc-contract.json")
print(f"R89 refused {r89}, R81 itc refused {r81}", file=sys.stderr)
sys.exit(0 if r89 >= 15 and r81 == 0 else 1)
PY
