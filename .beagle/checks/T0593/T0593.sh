#!/bin/bash
# T0593: a pursuit run's workers run the harness tau, not ~/.local/bin/tau (the
# editable dev checkout), and meta.json records which tau binary they ran.
set -euo pipefail
f=/home/choong/tautest/itc-harness/launch.sh
bash -n "$f"
grep -qE 'TAU_BIN="?\$TAU_SRC/\.venv/bin/tau' "$f"
grep -q '"tau_bin"' "$f"
