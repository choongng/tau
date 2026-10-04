#!/bin/bash
# R11: print-mode pursuit_found infers delegation.
set -e
T=tests/test_beagle_example_extension.py
uv run pytest -q -x "$T::test_print_mode_found_infers_delegation_from_a_delegating_prompt" \
  "$T::test_print_mode_found_takes_a_resend_after_its_refusal_as_delegation" \
  "$T::test_print_mode_found_without_a_delegating_prompt_refuses_first" \
  "$T::test_interactive_found_never_infers_delegation"
uv run pytest -q "$T"
uv run ruff check examples/extensions/beagle.py "$T"
