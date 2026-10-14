#!/bin/bash
# T0581: tau's slice text names the right-answer stand-in beagle's seal now requires (T0572)
set -e
T=tests/test_beagle_example_extension.py
uv run pytest -q -p no:cacheprovider "$T" -k "oracle_standin" 2>&1 | tee /dev/stderr | grep -qE '^[1-9][0-9]* passed(,| in)'
grep -q 'oracle/, laid out the same' examples/extensions/beagle.py
uv run ruff check examples/extensions/beagle.py "$T"
