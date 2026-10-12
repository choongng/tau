#!/bin/bash
# T0496: the run notes name only tests that exist, after 88f99810 removed the thinking-off twin.
set -eu
bash .beagle/checks/fix/test_names_resolve.sh dev-notes/itc-runs/R3{6,7,8}.md
bash .beagle/checks/T0360/T0360.sh
