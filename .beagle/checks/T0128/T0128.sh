#!/bin/bash
# audit 6 defect 4: runs/v3/scored.sh RNN MODEL asserts meta.model is the model the run was meant for.
set -eu
V=.beagle/checks/runs/v3
bash $V/selftest.sh
bash $V/scored.sh R14 qwen >/dev/null
bash $V/scored.sh R13 mimo >/dev/null
if bash $V/scored.sh R14 mimo >/dev/null 2>&1; then echo "scored.sh R14 mimo passed"; exit 1; fi
if bash $V/scored.sh R13 qwen >/dev/null 2>&1; then echo "scored.sh R13 qwen passed"; exit 1; fi
if bash $V/scored.sh R14 >/dev/null 2>&1; then echo "scored.sh R14 passed"; exit 1; fi
echo OK
