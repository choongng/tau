#!/bin/bash
# T0243: compaction headroom holds for a real summary
set -e
uv run pytest -q -x "tests/test_coding_session.py::test_compaction_headroom_holds_for_a_long_summary"
uv run pytest -q tests/test_coding_session.py tests/test_session.py tests/test_context_window.py
uv run ruff check src/tau_coding/session.py tests/test_coding_session.py
