#!/bin/bash
# T0225: absent cases test
set -e
T=tests/test_beagle_example_extension.py
uv run pytest -q -x \
  "$T::test_known_answers_open_binds_data_test_when_the_cases_test_is_not_on_disk"
uv run pytest -q "$T"
uv run ruff check examples/extensions/beagle.py "$T"
