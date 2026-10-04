+++
id = "000521-pursuit"
ordinal = 521
kind = "pursuit"
timestamp = "2026-10-04T04:53:28+00:00"
summary = "pursuit prove T0126: WITNESSED — refuses when beagle.py's `if program.startswith(\"python\") and _judges_not…` is put back as `if False:`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "4165391e416576d1658632a6aa19dbf93bc985d43e403d5bada78b1963e8ed8e  .beagle/checks/T0126/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0126/check.sh'
refutes: refuses when beagle.py's `if program.startswith("python") and _judges_not…` is put back as `if False:` (proven 2026-10-04T04:52:38+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_python_c_that_only_constructs_and_calls_is_refused)
refused after 1s of a 35s check at: FAILED tests/test_beagle_example_extension.py::test_python_c_that_only_constructs_and_calls_is_refused
refused with: 1 failed in 0.63s
