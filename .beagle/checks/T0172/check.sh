#!/bin/bash
# R20 class 3: scope refusal sent project code to /tmp.
set -e
T=tests/test_beagle_example_extension.py
uv run pytest -q -x \
  "$T::test_scope_refusal_of_project_code_does_not_point_to_tmp" \
  "$T::test_scope_refusal_of_the_checks_import_says_the_check_cannot_pass"
uv run pytest -q "$T"
uv run ruff check examples/extensions/beagle.py "$T"
