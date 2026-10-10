#!/bin/bash
# R39 class 1: a template-token leak only in an optional argument runs the clean call
set -e
T=tests/test_session_template_tokens.py
bash .beagle/checks/fix/named_tests.sh $T 3 \
  test_leak_in_optional_argument_runs_the_clean_call \
  test_leak_inside_required_argument_still_refused \
  test_refusal_names_the_clean_prefix
uv run pytest -q $T tests/test_session_output_limit_nudge.py
uv run pytest -q tests/test_beagle_example_extension.py -k "template or channel_tokens"
uv run ruff check src/tau_coding/session.py $T
