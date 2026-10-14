#!/bin/bash
# T0609 (S02): a task with a source opens only on a check that runs its cases:
# pursuit_step refuses a done_when naming no test file, and upstream ask 9 is filed.
set -euo pipefail
W=/home/choong/tautest/tau-wt-048
cd "$W"
grep -qE '^## 9\. `open --cases` accepts a check that does not run the cases' dev-notes/beagle-0.48/upstream-asks.md
PATH=$(echo "$PATH" | tr ':' '\n' | grep -v '/beagle/venv' | paste -sd:)
must_pass() {
  out=$(timeout 900 .venv/bin/python -m pytest -q --no-header -p no:cacheprovider "$@" 2>&1 | tail -1)
  echo "$* -> $out" >&2
  echo "$out" | grep -qE '^[1-9][0-9]* passed' || exit 1
  if echo "$out" | grep -qE 'failed|error|skipped'; then exit 1; fi
}
must_pass tests/test_beagle_example_extension.py -k "source_task and runs_no_cases"
must_pass -m real_beagle tests/
must_pass tests/test_beagle_example_extension.py
