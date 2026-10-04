#!/bin/bash
# T0091: v2 run checks pass on R10 and refuse a run whose launch facts or diagnosis are short.
set -eu
d=.beagle/checks/runs/v2
bash $d/scored.sh R10 >/dev/null
bash $d/diagnosed.sh R10 >/dev/null
bash $d/selftest.sh
