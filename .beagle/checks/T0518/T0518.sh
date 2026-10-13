#!/bin/bash
# T0518: a check whose first word is not a program here could not start (rc 127),
# naming what is (python3, .venv/bin/python), so it is refused at open rather
# than read as failing, as R84's `python -m pytest` was under systemd-run.
set -e
cd /home/choong/tautest/tau
uv run --quiet pytest -q -p no:cacheprovider tests/test_beagle_example_extension.py \
  -k "program_is_not_here_could_not_start" \
  2>&1 | tail -1 | tee /dev/stderr | grep -qE '^1 passed'
echo "T0518: a check naming a program that is not here could not start, and says what is"
