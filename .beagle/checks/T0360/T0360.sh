#!/bin/bash
# Audit 13 (T0360): the named tests on R36-R39's Tests: lines resolve, in tau or tau-subagents
set -eu
bash .beagle/checks/fix/test_names_resolve.sh dev-notes/itc-runs/R3{6,7,8,9}.md
