#!/bin/bash
# T0529: the worker brief says to write the code and run it before tracing a
# case by hand. R91: encode workers traced the C encoder in their reasoning
# until the output limit cut them off, with no code written.
set -e
cd /home/choong/beagle-wt/worker-run-dont-trace/plugins/beagle-pursuit/tooling/beagle
export UV_PROJECT_ENVIRONMENT=$HOME/.cache/beagle/venv-ops PYTHONPYCACHEPREFIX=$HOME/.cache/beagle/pycache-ops
uv run --quiet --with pytest --extra browser python -m pytest tests/test_pursuit.py -q -p no:cacheprovider \
  -k "run_code_before_tracing or parks_unfinished_work or runs_heavy_commands_contained" 2>&1 \
  | tail -1 | tee /dev/stderr | grep -qE '^3 passed'
