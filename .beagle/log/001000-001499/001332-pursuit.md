+++
id = "001332-pursuit"
ordinal = 1332
kind = "pursuit"
timestamp = "2026-10-09T22:13:53+00:00"
summary = "pursuit prove T0316: WITNESSED — refuses when R36.md's `Tests: tests/test_beagle_example_extension.py::…` is put back as `Tests: tests/test_beagle_extension.py::test_quo…`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "f241518d924cf4b1806af0695802f4a1d7f691d5469f1d4f498ab07f320acf78  .beagle/checks/T0316/T0316.sh" | sha256sum -c --quiet && bash .beagle/checks/T0316/T0316.sh'
refutes: refuses when R36.md's `Tests: tests/test_beagle_example_extension.py::…` is put back as `Tests: tests/test_beagle_extension.py::test_quo…` (proven 2026-10-09T22:13:53+00:00; predates the task: the fix was committed (80dfc9a8) before the task could open, while the audit was being kept; refused at nam
refused after 0s of a 0s check at: names tests/test_beagle_extension.py
refused with: names tests/test_beagle_extension.py
