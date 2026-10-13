#!/bin/bash
# T0526: two extractions of one reference are compared by its lines, not by
# what each calls it. R90's contract named the file by `cat` with its text as
# the output and the second named it by path; Reconcile reported all 22 of
# the second's entries as cited by no entry of the first.
set -e
W=/home/choong/beagle-wt/contract-same-document
here=/home/choong/tautest/tau/.beagle/checks/T0526
cd $W/plugins/beagle-pursuit/tooling/beagle
export UV_PROJECT_ENVIRONMENT=$HOME/.cache/beagle/venv-ops PYTHONPYCACHEPREFIX=$HOME/.cache/beagle/pycache-ops
uv run --quiet --with pytest --extra browser python -m pytest tests/test_contract.py -q -p no:cacheprovider \
  -k "by_document_not_name or identifies_an_experiment_by_its_command" 2>&1 | tail -1 | tee /dev/stderr | grep -qE '^2 passed'
uv run --quiet python - "$here/r90" <<'PY'
import sys
from pathlib import Path
from beagle import contract
d = contract.diff(Path(sys.argv[1]), "contract.json", "contract.second.json")
print(f"R90: {len(d.only_a)} only in the contract, {len(d.only_b)} only in the second",
      file=sys.stderr)
sys.exit(0 if d.exit_code == contract.EXIT_OK and not d.only_b else 1)
PY
