#!/bin/bash
# T0241: compaction leaves headroom under the threshold
set -e
uv run pytest -q -x "tests/test_coding_session.py::test_compaction_leaves_half_threshold_headroom"
uv run pytest -q tests/test_coding_session.py tests/test_session.py tests/test_context_window.py
uv run ruff check src/tau_coding/session.py tests/test_coding_session.py
