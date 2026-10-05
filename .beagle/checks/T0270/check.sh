#!/bin/bash
# R31 class 3: the repeat breaker's call key ignores duplicate list entries
set -e
uv run pytest -q -x tests/test_repeat_breaker_reset.py::test_call_key_ignores_duplicate_list_entries
uv run pytest -q tests/test_repeat_breaker_reset.py tests/test_coding_session.py
uv run ruff check src/tau_coding/session.py tests/test_repeat_breaker_reset.py
