#!/bin/bash
# audit 13: T0243's summary truncation tested over the cap
set -e
T=tests/test_coding_session.py
uv run pytest -q -x "$T::test_compaction_summary_over_cap_is_truncated_with_marker"
uv run pytest -q "$T"
uv run ruff check src/tau_coding/session.py "$T"
