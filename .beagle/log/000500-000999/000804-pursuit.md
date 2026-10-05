+++
id = "000804-pursuit"
ordinal = 804
kind = "pursuit"
timestamp = "2026-10-05T01:05:50+00:00"
summary = "pursuit prove T0206: WITNESSED — refuses when beagle.py's `keys = {str(key) for key in raw} if isinstance(…` is put back as `keys = set()`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "e4646eb70aaaddf988aeb7ed8c14ee0994bfa90d0131f6f25e91d173d6339d8e  .beagle/checks/T0206/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0206/check.sh'
refutes: refuses when beagle.py's `keys = {str(key) for key in raw} if isinstance(…` is put back as `keys = set()` (proven 2026-10-05T01:05:29+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_cases_test_indexing_the_top_level_key_is_not_an_absent_case)
refused after 2s of a 1m07s check at: FAILED tests/test_beagle_example_extension.py::test_cases_test_indexing_the_top_level_key_is_not_an_absent_case
refused with: 1 failed in 1.70s
