#!/bin/bash
# R32 class 4: the breaker quotes the sentence of a refusal that holds its call
set -e
uv run pytest -q -x tests/test_repeat_breaker_reset.py::test_repeated_call_quotes_sentence_holding_the_call
uv run pytest -q tests/test_repeat_breaker_reset.py tests/test_coding_session.py
uv run ruff check src/tau_coding/session.py tests/test_repeat_breaker_reset.py
