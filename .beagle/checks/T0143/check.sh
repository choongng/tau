#!/bin/bash
# R16 classes 7 and 8: symlinks out of scope; a worker read an earlier run's tree beside the project.
set -e
T=tests/test_beagle_example_extension.py
uv run pytest -q -x \
  "$T::test_worker_guard_refuses_python_os_symlink_out_of_scope" \
  "$T::test_worker_guard_judges_in_tree_symlink_by_its_own_path" \
  "$T::test_worker_guard_refuses_reading_a_sibling_project_tree"
uv run pytest -q "$T"
uv run ruff check examples/extensions/beagle.py "$T"
