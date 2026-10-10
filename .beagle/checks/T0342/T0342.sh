#!/bin/bash
# R39 class 5: a cases test that copies the data test does not close known answers; Cases-first offers an existing one
set -e
T=tests/test_beagle_example_extension.py
bash .beagle/checks/fix/named_tests.sh $T 2 \
  test_known_answers_close_refuses_cases_test_copying_data_test \
  test_cases_first_offers_existing_uncommitted_cases_test
uv run pytest -q $T
uv run ruff check examples/extensions/beagle.py $T
