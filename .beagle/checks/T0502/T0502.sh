#!/bin/bash
# T0502: a worker runs the contract's read verbs (refs, check, status, diff, run) and is still
# refused the ones that change it (seal), named as such.
set -e
cd /home/choong/tautest/tau
uv run pytest -q -p no:cacheprovider tests/test_beagle_example_extension.py \
  -k "worker_may_read_the_pursuit_but_not_change_it" 2>&1 | tail -3 | tee /dev/stderr | grep -qE '^[0-9]+ passed'
python3 - <<'PY'
import re
s = open("tests/test_beagle_example_extension.py").read()
for row in ("pursuit contract refs", "pursuit contract check", "pursuit contract seal"):
    assert re.search(rf'\("[^"]*{row}[^"]*",', s), f"no worker-guard row for `{row}`"
assert '"contract seal")' in s, "a contract write is not refused by name"
PY
echo "T0502: workers read the contract; seal refused by name"
