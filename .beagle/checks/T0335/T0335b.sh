#!/bin/bash
# Audit 12 (T0335), re-pointed by audit 13 (T0360): every test R36-R38 name on
# their Tests: lines exists, in tau or tau-subagents.
set -eu
bash .beagle/checks/fix/test_names_resolve.sh dev-notes/itc-runs/R3{6,7,8}.md
