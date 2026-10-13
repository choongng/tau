#!/bin/bash
# T0535: a worker's default turn cap is 60 (R94: 3 of 7 workers cut at 30
# mid-edit while the ~900 s wall already bounds a worker).
set -e
cd /home/choong/tautest/tau
grep -qE '^DEFAULT_WORKER_MAX_TURNS = 60$' examples/extensions/beagle.py
timeout 540 uv run --quiet pytest -q -p no:cacheprovider tests/test_beagle_example_extension.py \
  -k "worker_argv_caps_turns or turn_cap" 2>&1 | tail -1 | tee /dev/stderr | grep -qE '^[0-9]+ passed'
