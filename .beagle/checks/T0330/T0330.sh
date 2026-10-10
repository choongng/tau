#!/bin/bash
# R38 class 3: the output-limit nudge's thinking-off request and in-a-row bound hold in a session
# with another follow-up queued (tau-subagents' empty-report prompt). Regression tests in their own file.
set -e
T=tests/test_session_output_limit_nudge.py
n=$(grep -c '^async def test_\|^def test_' "$T")
[ "$n" -ge 2 ] || { echo "want >= 2 tests in $T, have $n" >&2; exit 1; }
uv run pytest -q -x "$T"
uv run pytest -q tests/test_session_output_limit.py tests/test_session_template_tokens.py tests/test_session.py
uv run ruff check src/tau_coding/session.py "$T"
