#!/bin/bash
set -eu
c=.beagle/checks/fix/named_tests.sh
bash $c tests/test_beagle_example_extension.py 3 test_worker_argv_caps_turns test_worker_argv_thinking_level test_step_and_dispatch_timeout_clamped
bash $c tests/test_agent_loop_turn_cap.py 2 test_turn_cap_warns_before_last_turn test_turn_cap_ends_with_report_not_error
echo OK
