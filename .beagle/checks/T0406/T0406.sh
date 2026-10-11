#!/bin/bash
# T0406: _already_passes offers done-by only for a done task _done_by would accept
set -e
T=tests/test_beagle_example_extension.py
F=examples/extensions/beagle.py
bash .beagle/checks/fix/named_tests.sh $T 3 test_already_passes_offers_no_done_by_that_needs_a_witness_it_lacks test_already_passes_offered_done_by_is_one_done_by_accepts test_already_passes_still_offers_a_witnessable_done_by
uv run pytest -q $T
uv run ruff check $F $T
