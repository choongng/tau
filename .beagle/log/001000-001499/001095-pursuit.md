+++
id = "001095-pursuit"
ordinal = 1095
kind = "pursuit"
timestamp = "2026-10-05T13:28:32+00:00"
summary = "pursuit prove T0264: WITNESSED — refuses when beagle.py's `if stopped is not None and own_hang:` is put back as `if False:`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "2b691256ff61c05cb47e7e0c05db22430b6fc2ab8efb850f1931d37af35393b1  .beagle/checks/T0264/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0264/check.sh'
refutes: refuses when beagle.py's `if stopped is not None and own_hang:` is put back as `if False:` (proven 2026-10-05T13:28:32+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_open_proceeds_when_check_killed_on_uncommitted_scope_code[False])
refused after 3s of a 1m30s check at: FAILED tests/test_beagle_example_extension.py::test_open_proceeds_when_check_killed_on_uncommitted_scope_code[False]
refused with: 1 failed in 2.19s
