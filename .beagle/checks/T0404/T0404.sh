#!/bin/bash
# T0404: the driver's bash guards see a bash -c script holding a heredoc, and touch/ln into .beagle
set -e
T=tests/test_beagle_example_extension.py
F=examples/extensions/beagle.py
bash .beagle/checks/fix/named_tests.sh $T 3 test_driver_bash_change_sees_a_bash_c_heredoc_write test_bash_writes_dot_beagle_sees_touch_and_ln test_driver_bash_change_lets_a_tmp_heredoc_run
uv run pytest -q $T
uv run ruff check $F $T
