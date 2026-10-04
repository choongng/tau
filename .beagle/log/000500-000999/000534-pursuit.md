+++
id = "000534-pursuit"
ordinal = 534
kind = "pursuit"
timestamp = "2026-10-04T05:13:09+00:00"
summary = "pursuit prove T0127: WITNESSED — refuses when beagle.py's `usage = rc in (2, 64) and any(line.lower().star…` is put back as `usage = False`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "e86c4262f98309838477b3d6a26e8671ddae650fe188d2127df27183819f33fd  .beagle/checks/T0127/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0127/check.sh'
refutes: refuses when beagle.py's `usage = rc in (2, 64) and any(line.lower().star…` is put back as `usage = False` (proven 2026-10-04T05:13:09+00:00; predates the task: T0127 adds tests that guard T0118's usage clause; the audit found nothing failed when it was broken; refused at FAILED tests/test_beagle_ex
refused after 2s of a 38s check at: FAILED tests/test_beagle_example_extension.py::test_open_refuses_a_check_that_prints_usage
refused with: 1 failed, 1 passed in 1.22s
