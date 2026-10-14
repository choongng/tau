#!/bin/bash
# T0517: does the incremental contract already turn sources silent on invalid input
# into a gap the reader is asked about? A read, with a decision either way.
set -e
F=dev-notes/contract-first/invalid-silence-recon.md
test -f "$F"
grep -qE '^Decision: (covered|build|defer)' "$F"
grep -qE 'contract\.py:[0-9]+' "$F"
grep -qE 'beagle\.py:[0-9]+' "$F"
grep -q 'R84' "$F"
