#!/bin/bash
# T0601: a milestone the driver gives a `source` is one spec-tied pursuit_step:
# a cases worker writes marked cases from the source (test files only), the
# task opens with --cites/--cases that the real beagle 0.48 accepts, then the
# code worker. A milestone with no source runs as before, with no cases worker.
set -euo pipefail
W=/home/choong/tautest/tau-wt-048
E=$W/examples/extensions/beagle.py
cd "$W"
[ "$(git branch --show-current)" = beagle-0.48 ]
grep -q '"source"' "$E"
grep -q -- '"--cites"' "$E"
grep -q -- '"--cases"' "$E"
PATH=$(echo "$PATH" | tr ':' '\n' | grep -v '/beagle/venv' | paste -sd:)
py() { timeout 900 .venv/bin/python -m pytest -q --no-header -p no:cacheprovider "$@" 2>&1 | tail -1; }
must_pass() {  # every selected test passes, at least one is selected, none skips
  local out; out=$(py "$@"); echo "$* -> $out" >&2
  echo "$out" | grep -qE '^[1-9][0-9]* passed' || exit 1
  if echo "$out" | grep -qE 'failed|error|skipped'; then exit 1; fi
}
must_pass -m real_beagle tests/ -k "spec_tied"
must_pass tests/test_beagle_example_extension.py -k "spec_tied"
must_pass tests/test_beagle_example_extension.py -k "no_source and cases"
must_pass tests/test_beagle_example_extension.py -k "cases and scope"
must_pass tests/test_beagle_example_extension.py -k "cases and fail"
must_pass tests/test_beagle_example_extension.py -k "plan and source"
must_pass -m real_beagle tests/
must_pass tests/test_beagle_example_extension.py
