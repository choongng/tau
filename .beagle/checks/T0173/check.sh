#!/bin/bash
# R20 class 4: worker sent though the check already passed on uncommitted work.
set -e
T=tests/test_beagle_example_extension.py
uv run pytest -q -x \
  "$T::test_open_closes_without_a_worker_when_uncommitted_work_already_passes" \
  "$T::test_open_on_uncommitted_pass_asks_only_for_a_witness_when_absence_is_the_only_proof"
uv run pytest -q "$T"
uv run ruff check examples/extensions/beagle.py "$T"
