#!/bin/bash
# T0565: each standing check T0564's lint found (T0054 T0128 T0226 T0245 T0490 T0533) is now
# bound to a script with no dead `! cmd` step under set -e, or the task is retired.
set -e
cd /home/choong/tautest/tau
B=/home/choong/beagle-wt/contract-first/plugins/beagle-pursuit/bin/beagle
PY=/home/choong/.cache/beagle/venv-ops/bin/python
SRC=/home/choong/beagle-wt/contract-first/plugins/beagle-pursuit/tooling/beagle/src
for t in T0054 T0128 T0226 T0245 T0490 T0533; do
  view=$($B pursuit view $t 2>&1)
  if echo "$view" | grep -m1 -qE "^\s*retired"; then echo "$t retired"; continue; fi
  files=$(echo "$view" | grep -m1 'decided by:' | grep -oE '\.beagle/checks/[^ ]+\.sh' | sort -u)
  test -n "$files"
  for f in $files; do
    PYTHONPATH=$SRC PYTHONDONTWRITEBYTECODE=1 $PY -c 'import sys; from beagle.pursuit import refuse_negation_under_set_e as r; r(open(sys.argv[1]).read())' "$f"
    echo "$t $f clean"
  done
done
