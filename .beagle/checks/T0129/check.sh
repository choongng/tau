#!/bin/bash
# _changed_files lost the first path's first letter to _run's strip.
set -e
T=tests/test_beagle_example_extension.py
uv run pytest -q -x \
  "$T::test_changed_files_keeps_the_first_path_whole"
uv run pytest -q "$T"
uv run ruff check examples/extensions/beagle.py "$T"
