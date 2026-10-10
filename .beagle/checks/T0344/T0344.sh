#!/bin/bash
# T0344: the cached extension module's BEAGLE_BIN follows the beagle/fake_beagle fixtures,
# whatever test loaded the module first
set -e
T=tests/test_beagle_example_extension.py
out=$(uv run pytest -q -p no:cacheprovider \
  "$T::test_stop_gate_says_nothing_unfounded_in_an_interactive_session" \
  "$T::test_stop_gate_founded_session_gets_no_unfounded_followup" 2>&1) || { echo "$out" | tail -20; exit 1; }
echo "$out" | grep -qE "^2 passed" || { echo "$out" | tail -5; exit 1; }
uv run pytest -q -p no:cacheprovider $T -k session
uv run pytest -q -p no:cacheprovider $T
uv run ruff check $T
