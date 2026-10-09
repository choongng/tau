+++
id = "001261-pursuit"
ordinal = 1261
kind = "pursuit"
timestamp = "2026-10-09T19:37:04+00:00"
summary = "pursuit prove T0293: WITNESSED — refuses when beagle.py's `if narrow or not is_narrow` is put back as `if not is_narrow`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "3c8056cf56b42515e88daa6f2833bbb46e7501c31a9cdddfd1b9ba09b89c84b6  .beagle/checks/T0293/T0293.sh" | sha256sum -c --quiet && bash .beagle/checks/T0293/T0293.sh'
refutes: refuses when beagle.py's `if narrow or not is_narrow` is put back as `if not is_narrow` (proven 2026-10-09T19:37:04+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_short_result_checked_against_quoted_reference_line)
refused after 3s of a 1m39s check at: FAILED tests/test_beagle_example_extension.py::test_short_result_checked_against_quoted_reference_line
refused with: 1 failed in 2.84s
