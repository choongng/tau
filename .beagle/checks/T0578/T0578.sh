#!/bin/bash
# T0578: no cases-first brief text survives T0493 (QUOTED_SOURCE_NOTE, the cases.json worked example);
# a data-file worker is not told of a close-time source judge that no longer exists.
set -e
cd /home/choong/tautest/tau
X() { env -u VIRTUAL_ENV -u UV_PROJECT_ENVIRONMENT PATH="$(echo "$PATH" | tr : '\n' | grep -v '/beagle/' | paste -sd:)" \
  timeout 900 uv run --quiet pytest -q -p no:cacheprovider tests/test_beagle_example_extension.py "$@" 2>&1 | tail -1 | tee /dev/stderr; }
X -k "data_task_brief_has_no_cases_first_text" | grep -qE '^[1-9][0-9]* passed(,| in)'
X | grep -qE '^[0-9]+ passed( in|,)'
if grep -nE 'QUOTED_SOURCE_NOTE|_worked_example_note|cases\.json|cases file' examples/extensions/beagle.py; then echo "cases-first text remains"; exit 1; fi
