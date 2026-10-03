+++
id = "000036-pursuit"
ordinal = 36
kind = "pursuit"
timestamp = "2026-10-03T11:13:10+00:00"
summary = "pursuit prove T0023: WITNESSED — refuses when beagle.py's `cmd += [\"--max-turns\", str(_worker_max_turns())]` is put back as `pass`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "8a38c62c4251d3fc6e93fe05a520313706edc950f29f1205557ee6f4d412ff2a  .beagle/checks/T0023/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0023/check.sh'
refutes: refuses when beagle.py's `cmd += ["--max-turns", str(_worker_max_turns())]` is put back as `pass` (proven 2026-10-03T11:13:08+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_worker_argv_caps_turns - ...)
refused after 1s of a 1s check at: FAILED tests/test_beagle_example_extension.py::test_worker_argv_caps_turns - ...
refused with: 1 failed, 2 passed, 192 deselected in 0.64s
