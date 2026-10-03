#!/bin/bash
set -eu
c=.beagle/checks/fix/named_tests.sh
bash $c tests/test_beagle_example_extension.py 2 test_found_drops_setup_milestone_and_says_so test_found_shortens_long_milestone_title
bash $c tests/test_repeat_breaker_reset.py 1 test_repeat_refusal_quotes_earlier_result
echo OK
