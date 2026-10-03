#!/bin/bash
# T0089: the directory-scope walk skips tool cache directories.
set -eu
bash .beagle/checks/fix/named_tests.sh tests/test_beagle_example_extension.py 1 \
  test_scope_dir_walk_skips_cache_directories
.venv/bin/ruff check examples/extensions/beagle.py tests/test_beagle_example_extension.py
