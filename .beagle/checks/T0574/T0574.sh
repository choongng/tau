#!/bin/bash
# T0574: a run's tools do not see tau-harness's own venv on PATH (S01's python3/pytest came
# from it; R97 pip-installed its package into it). launch.sh --dry-run prints the run's PATH.
set -e
H=/home/choong/tautest/itc-harness
out=$(cd $H && BEAGLE_ROOT=/home/choong/beagle-wt/contract-first CAP_S=60 bash launch.sh --dry-run S99 q35 semver 2>&1)
p=$(printf '%s\n' "$out" | sed -n 's/^run PATH: //p')
test -n "$p"
if printf '%s' "$p" | tr : '\n' | grep -q 'tau-harness/\.venv'; then echo "tau-harness venv on the run's PATH: $p"; exit 1; fi
printf '%s' "$p" | tr : '\n' | grep -qx '/usr/bin'
printf '%s' "$p" | tr : '\n' | grep -q 'beagle-pursuit/bin$'
printf '%s\n' "$out" | grep -q 'tau-harness/\.venv/bin/tau -p'
