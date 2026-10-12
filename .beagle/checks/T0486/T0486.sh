#!/bin/bash
# T0486: open/bind/amend refuse a check that needs the whole tree clean; a pathspec'd one stands.
set -eu
exec bash .beagle/checks/fix/beagle_named.sh tests/test_pursuit.py 8 \
  test_open_refuses_a_check_that_needs_the_whole_tree_clean \
  test_a_check_of_the_work_s_own_paths_may_read_git_status
