#!/bin/bash
# T0556: done needs every normative source line (RFC 2119 keyword, code span, table row,
# formula, or a digit once page numbers, [n] citations, years and section numbers are
# stripped) cited by a live entry or excluded with a why over at most 40 lines; a retired
# entry's FAIL no longer blocks done (incremental-contract.md task 3, owner decisions).
set -e
W=/home/choong/beagle-wt/rotation-fixes
cd $W/plugins/beagle-pursuit/tooling/beagle
UV_PROJECT_ENVIRONMENT=$HOME/.cache/beagle/venv-ops PYTHONPYCACHEPREFIX=$HOME/.cache/beagle/pycache-ops \
  timeout 300 uv run --quiet --with pytest --extra browser python -m pytest -q -p no:cacheprovider tests/test_contract.py \
  -k "normative_rule_lines or coverage_counts_excluded or done_gate_needs_coverage or retired_entry_fail_ignored or coverage_wrenfold_fixture or exclusion_over_forty_lines_refused" \
  2>&1 | tail -1 | tee /dev/stderr | grep -qE '^6 passed'
cd $W && PYTHONDONTWRITEBYTECODE=1 timeout 900 bash ci/check.sh 2>&1 | tail -1 | tee /dev/stderr | grep -q "ci: all gates green"
