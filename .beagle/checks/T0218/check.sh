#!/bin/bash
# T0218: html table cells
set -e
T=tests/test_beagle_example_extension.py
uv run pytest -q -x \
  "$T::test_html_text_keeps_table_cells_apart_and_drops_page_chrome"
uv run pytest -q "$T"
uv run ruff check examples/extensions/beagle.py "$T"
