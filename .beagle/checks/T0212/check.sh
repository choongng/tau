#!/bin/bash
# T0212: dispatch text names only calls the driver can make
set -e
T=tests/test_beagle_example_extension.py
uv run pytest -q -x \
  "$T::test_dispatch_text_in_a_founded_session_names_no_guard_refused_bash_command"
uv run pytest -q "$T"
uv run ruff check examples/extensions/beagle.py "$T"
