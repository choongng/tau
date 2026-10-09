+++
id = "001253-pursuit"
ordinal = 1253
kind = "pursuit"
timestamp = "2026-10-09T19:15:30+00:00"
summary = "pursuit prove T0292: WITNESSED — refuses when beagle.py's `_carry_not_done(root, task, successor)` is put back as `pass`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "54ad0d23b1876a5e81062d007eff02a7f2d4358e10c006cca6c253e32e421850  .beagle/checks/T0292/T0292.sh" | sha256sum -c --quiet && bash .beagle/checks/T0292/T0292.sh'
refutes: refuses when beagle.py's `_carry_not_done(root, task, successor)` is put back as `pass` (proven 2026-10-09T19:15:30+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_new_route_same_check_carries_not_done_count)
refused after 1s of a 1m40s check at: FAILED tests/test_beagle_example_extension.py::test_new_route_same_check_carries_not_done_count
refused with: 1 failed in 1.19s
