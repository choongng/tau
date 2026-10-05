#!/bin/bash
# R34 fix: workers get a short bash default timeout; the no-write guard counts in-scope paging and bash runs that write nothing
set -e
T=tests/test_beagle_example_extension.py
uv run pytest -q -x \
  "$T::test_worker_bash_default_timeout_is_short" \
  "tests/test_coding_tools.py::test_bash_default_timeout_from_env" \
  "$T::test_no_write_guard_counts_in_scope_paging" \
  "$T::test_no_write_guard_counts_bash_runs_without_writes"
uv run pytest -q "$T" tests/test_coding_tools.py
uv run ruff check examples/extensions/beagle.py "$T" src/tau_coding/tools.py tests/test_coding_tools.py
