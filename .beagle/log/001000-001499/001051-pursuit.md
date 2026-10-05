+++
id = "001051-pursuit"
ordinal = 1051
kind = "pursuit"
timestamp = "2026-10-05T11:17:59+00:00"
summary = "pursuit prove T0255: WITNESSED — refuses when beagle.py's `if _fixes_known_answers(title):` is put back as `if False:`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "8cec1472c97378e52dc04b0a540bece52f2cdeab8984bef559c535afc87eddd0  .beagle/checks/T0255/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0255/check.sh'
refutes: refuses when beagle.py's `if _fixes_known_answers(title):` is put back as `if False:` (proven 2026-10-05T11:17:59+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_done_by_refuses_fix_of_done_task)
refused after 3s of a 1m27s check at: FAILED tests/test_beagle_example_extension.py::test_done_by_refuses_fix_of_done_task
refused with: 1 failed in 2.33s
