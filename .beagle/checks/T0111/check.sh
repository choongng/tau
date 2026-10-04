#!/bin/bash
# R12 class 3: the worker scope guard sees writes through os.system/subprocess in inline scripts.
set -e
T=tests/test_beagle_example_extension.py
uv run pytest -q -x "$T::test_worker_guard_blocks_sed_through_os_system_in_inline_python" \
  "$T::test_worker_guard_blocks_subprocess_write_outside_scope" \
  "$T::test_worker_guard_allows_os_system_write_inside_scope"
uv run pytest -q "$T"
uv run ruff check examples/extensions/beagle.py "$T"
