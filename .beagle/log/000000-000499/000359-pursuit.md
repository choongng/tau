+++
id = "000359-pursuit"
ordinal = 359
kind = "pursuit"
timestamp = "2026-10-03T21:06:00+00:00"
summary = "pursuit prove T0082: WITNESSED — refuses when beagle.py's `_OFF_PURSUIT_CALLS += 1` is put back as `_OFF_PURSUIT_CALLS += 0`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "918f9492fa2da16334d0ba72eec1f0075b6881e74b62240324f44b9e6f588551  .beagle/checks/T0082/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0082/check.sh'
refutes: refuses when beagle.py's `_OFF_PURSUIT_CALLS += 1` is put back as `_OFF_PURSUIT_CALLS += 0` (proven 2026-10-03T21:05:19+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_driver_non_pursuit_streak_after_founding_is_refused)
refused after 1s of a 1s check at: FAILED tests/test_beagle_example_extension.py::test_driver_non_pursuit_streak_after_founding_is_refused
refused with: 1 failed, 3 passed, 289 deselected in 0.49s
