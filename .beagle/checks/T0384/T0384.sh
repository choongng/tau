#!/bin/bash
# R43 fix: a cut-off kill note says what filled the turn
set -e
T=tests/test_beagle_example_extension.py
bash .beagle/checks/fix/named_tests.sh $T 2 test_cut_off_kill_note_names_reply_text_reasoning test_cut_off_kill_note_says_write_in_parts_only_for_a_call_argument
uv run pytest -q $T
uv run ruff check examples/extensions/beagle.py $T
