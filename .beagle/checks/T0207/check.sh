#!/bin/bash
# T0207: R22 class 5
set -e
T=tests/test_beagle_example_extension.py
uv run pytest -q -x \
  "$T::test_driver_guard_reads_bash_c_behind_env_assignments" \
  "$T::test_driver_refusals_do_not_name_the_override_env" \
  "$T::test_locked_ignores_files_not_in_the_manifest"
uv run pytest -q "$T"
uv run ruff check examples/extensions/beagle.py "$T"
