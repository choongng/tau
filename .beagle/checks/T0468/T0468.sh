#!/bin/bash
# T0468: the reasoning loop cut catches a sentence group repeated within one line (R58)
set -e
T=tests/test_session_output_limit.py
F=src/tau_coding/session.py
bash .beagle/checks/fix/named_tests.sh $T 1 test_sentences_repeated_within_one_line_are_cut
uv run pytest -q $T
uv run ruff check $F $T
