#!/bin/bash
# R42 fix: the repeat refusal of a cut read quotes its continuation note
set -e
T=tests/test_tool_history.py
bash .beagle/checks/fix/named_tests.sh $T 2 test_repeat_refusal_quotes_the_read_cut_continuation test_repeat_refusal_head_is_first_line_for_an_uncut_result
uv run pytest -q $T tests/test_repeat_breaker_reset.py tests/test_coding_session.py
uv run ruff check src/tau_coding/session.py $T
