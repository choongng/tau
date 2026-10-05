+++
id = "000929-pursuit"
ordinal = 929
kind = "pursuit"
timestamp = "2026-10-05T06:31:19+00:00"
summary = "pursuit prove T0231: WITNESSED — refuses when beagle.py's `retry_note = _last_failure_note((str(root), tas…` is put back as `retry_note = \"\"`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "55b6110fd00786bb784d4b2f70983cef0649bf71d3ad1864ea059030f39e92f3  .beagle/checks/T0231/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0231/check.sh'
refutes: refuses when beagle.py's `retry_note = _last_failure_note((str(root), tas…` is put back as `retry_note = ""` (proven 2026-10-05T06:31:11+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_first_worker_of_step_is_briefed_with_last_failure)
refused after 3s of a 1m18s check at: FAILED tests/test_beagle_example_extension.py::test_first_worker_of_step_is_briefed_with_last_failure
refused with: 1 failed in 2.71s
