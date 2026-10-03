+++
id = "000299-pursuit"
ordinal = 299
kind = "pursuit"
timestamp = "2026-10-03T20:12:57+00:00"
summary = "pursuit prove T0069: WITNESSED — refuses when beagle.py's `superseded = _SUPERSEDED_REPORT_NOTE if rc == 0…` is put back as `superseded = \"\"`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "88ed18552cdf0da9d8134cc39ecf33b9893c3a201fd89060ad5d1ab2480d733d  .beagle/checks/T0069/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0069/check.sh'
refutes: refuses when beagle.py's `superseded = _SUPERSEDED_REPORT_NOTE if rc == 0…` is put back as `superseded = ""` (proven 2026-10-03T20:12:22+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_closed_done_step_marks_a_failing_report_superseded)
refused after 1s of a 1s check at: FAILED tests/test_beagle_example_extension.py::test_closed_done_step_marks_a_failing_report_superseded
refused with: 1 failed, 1 passed, 273 deselected in 0.76s
