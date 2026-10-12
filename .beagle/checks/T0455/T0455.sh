#!/bin/bash
# T0455: already-passes offers no done-by or abandon its own rules refuse (R54)
set -e
T=tests/test_beagle_example_extension.py
F=examples/extensions/beagle.py
bash .beagle/checks/fix/named_tests.sh $T 3 test_already_passes_offers_no_done_by_whose_only_witness_is_an_imported_module test_already_passes_offers_no_duplicate_abandon_for_a_founding_milestone test_done_by_released_tail_starts_at_a_line
uv run pytest -q $T
uv run ruff check $F $T
