#!/bin/bash
# Re-point R42.md's Tests lines to where T0377 and T0378 put the tests
set -e
N=dev-notes/itc-runs/R42.md
if grep -qE 'test_repeat_breaker_reset|test_session_thinking_off_twin' $N; then echo "R42.md still names the old test files"; exit 1; fi
bash .beagle/checks/fix/test_names_resolve.sh $N
echo OK
