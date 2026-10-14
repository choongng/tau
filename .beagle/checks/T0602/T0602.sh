#!/bin/bash
# T0602: tau's beagle extension takes 0.48's outputs as 0.48 gives them:
# prove --isolated beside a live worker, beagle's own `next:` relayed, JSON
# read past any line beagle adds, and workers allowed 0.48's read verbs.
set -euo pipefail
W=/home/choong/tautest/tau-wt-048
E=$W/examples/extensions/beagle.py
cd "$W"
[ "$(git branch --show-current)" = beagle-0.48 ]
grep -q -- '"--isolated"' "$E"
PATH=$(echo "$PATH" | tr ':' '\n' | grep -v '/beagle/venv' | paste -sd:)
py() { timeout 900 .venv/bin/python -m pytest -q --no-header -p no:cacheprovider "$@" 2>&1 | tail -1; }
must_pass() {  # every selected test passes, at least one is selected, none skips
  local out; out=$(py "$@"); echo "$* -> $out" >&2
  echo "$out" | grep -qE '^[1-9][0-9]* passed' || exit 1
  if echo "$out" | grep -qE 'failed|error|skipped'; then exit 1; fi
}
must_pass tests/test_beagle_example_extension.py -k "json_out and next"
must_pass tests/test_beagle_example_extension.py -k "prove and isolated"
must_pass tests/test_beagle_example_extension.py -k "relay and next"
must_pass tests/test_beagle_example_extension.py -k "worker and refs and rules"
must_pass -m real_beagle tests/
must_pass tests/test_beagle_example_extension.py
