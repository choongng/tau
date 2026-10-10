#!/bin/bash
# Reference lookup through tilth (grep -n fallback): the brief, the reread refusal and the unanswered-case note say how to search references
set -e
T=tests/test_beagle_example_extension.py
bash .beagle/checks/fix/named_tests.sh $T 3 test_references_brief_says_how_to_search_references test_reread_refusal_on_reference_offers_search test_unanswered_case_note_says_how_to_search
uv run pytest -q $T
uv run ruff check examples/extensions/beagle.py $T
