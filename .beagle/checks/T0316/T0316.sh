#!/bin/bash
# R36.md's Tests: lines name tau's real beagle test file
set -e
f=dev-notes/itc-runs/R36.md
if grep -q 'tests/test_beagle_extension\.py' "$f"; then echo "names tests/test_beagle_extension.py"; exit 1; fi
test "$(grep '^Tests:' "$f" | grep -c 'tests/test_beagle_example_extension\.py')" -ge 4
