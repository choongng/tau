#!/bin/bash
# T0579: the stand-in crash recon is written and committed, with a recommendation that names
# which S01 entries it refuses and what it falsely refuses in R96/R97.
set -e
cd /home/choong/tautest/tau
F=dev-notes/contract-first/standin-crash-recon.md
git ls-files --error-unmatch "$F" >/dev/null
git diff --quiet HEAD -- "$F"
grep -q '^## Recommendation' "$F"
grep -qE 'S01' "$F"
grep -qE 'R96' "$F"
grep -qE 'R97' "$F"
grep -qiE 'falsely|false refus' "$F"
