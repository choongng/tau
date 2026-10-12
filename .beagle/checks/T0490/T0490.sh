#!/bin/bash
# T0490: tau's references come from `beagle refs fetch`; the extension keeps no fetcher of its own.
set -e
T=tests/test_beagle_example_extension.py
F=examples/extensions/beagle.py
bash .beagle/checks/fix/named_tests.sh $T 3 \
  test_references_are_fetched_by_beagle_refs \
  test_a_request_without_urls_is_recorded_without_beagle_refs \
  test_a_beagle_without_refs_records_each_url_as_failed
! grep -nE '^def _fetch_reference\(|^class _HtmlText|^def _pdf_text\(' $F
mkdir -p "$HOME/.cache/tau-pytest"
timeout 900 uv run --no-sync --with pytest-xdist pytest -q -p no:cacheprovider -n auto \
  --basetemp="$HOME/.cache/tau-pytest/T0490" $T 2>&1 | tail -1 | grep -E '^[0-9]+ passed in'
uv run --no-sync ruff check $F $T
uv run --no-sync ruff format --check $F $T
