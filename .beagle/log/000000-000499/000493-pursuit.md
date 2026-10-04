+++
id = "000493-pursuit"
ordinal = 493
kind = "pursuit"
timestamp = "2026-10-04T03:43:46+00:00"
summary = "pursuit prove T0123: WITNESSED — refuses when beagle.py's `readers = judges or tests` is put back as `readers = tests`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "11104116742d96fd2c1444f35d7f4081b62975262c13760f8a719673d48b4685  .beagle/checks/T0123/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0123/check.sh'
refutes: refuses when beagle.py's `readers = judges or tests` is put back as `readers = tests` (proven 2026-10-04T03:42:58+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_known_answers_task_whose_test_never_opens_the_cases_file_stays_open)
refused after 1s of a 32s check at: FAILED tests/test_beagle_example_extension.py::test_known_answers_task_whose_test_never_opens_the_cases_file_stays_open
refused with: 1 failed in 0.81s
