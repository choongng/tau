#!/bin/bash
# Audit 12 (T0336): tau-subagents' runtime-provider-config tests run against
# the choong-dev tau (the one runs load the extension into), not the PyPI
# tau-ai in the extension's own venv, where the twin test skips. Both must
# pass; a skip fails this check.
set -eu
TS="$HOME/.tau/extensions/tau-subagents"
cd "$HOME/tautest/tau"
out=$(PYTHONPATH="$TS/src" uv run --quiet pytest -q -p no:cacheprovider --rootdir "$TS" \
  "$TS/tests/test_extension.py" -k runtime_provider_config -rs 2>&1) || { echo "$out" | tail -20; exit 1; }
echo "$out" | tail -1
echo "$out" | tail -1 | grep -qE "^2 passed, [0-9]+ deselected in" || { echo "expected exactly 2 passed and nothing skipped"; exit 1; }
