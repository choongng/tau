#!/bin/bash
# T0331: sub-agent sessions get a runtime provider config (tau-subagents), and
# tau warns instead of silently sending a nudge with thinking on.
set -euo pipefail
TS="$HOME/.tau/extensions/tau-subagents"
out=$(cd "$TS" && uv run --quiet pytest -q -p no:cacheprovider tests/test_extension.py -k "runtime_provider_config" 2>&1) || { echo "$out" | tail -20; exit 1; }
echo "$out" | tail -1
echo "$out" | grep -qE "^[0-9]+ passed" || { echo "no tau-subagents runtime_provider_config test ran"; exit 1; }
(cd "$TS" && uv run --quiet pytest -q -p no:cacheprovider tests/test_extension.py 2>&1 | tail -1) | grep -qv failed || { echo "tau-subagents test_extension.py fails"; exit 1; }
cd "$HOME/tautest/tau"
out=$(uv run --quiet pytest -q -p no:cacheprovider tests -k "thinking_off_twin" 2>&1) || { echo "$out" | tail -20; exit 1; }
echo "$out" | tail -1
echo "$out" | grep -qE "^[0-9]+ passed" || { echo "no tau thinking_off_twin test ran"; exit 1; }
uv run --quiet pytest -q -p no:cacheprovider tests/test_session_output_limit_nudge.py tests/test_session_output_limit.py 2>&1 | tail -1
uv run --quiet ruff check src/tau_coding/session.py
grep -q "runtime_provider_config" "$TS/src/tau_subagents/extension.py"
grep -q "tau-subagents" dev-notes/itc-runs/upstream.md
