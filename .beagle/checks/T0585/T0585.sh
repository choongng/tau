#!/bin/bash
# T0585: R98's time outside the code, read from its traces, with ranked cuts.
set -e
F=dev-notes/contract-first/r98-time-recon.md
test -f "$F"
grep -qE '^Decision: ' "$F"
grep -qE '[0-9]+(\.[0-9])? min' "$F"
grep -q 'T0013' "$F"
grep -qE 'coverage' "$F"
