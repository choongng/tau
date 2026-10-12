+++
id = "002142-pursuit"
ordinal = 2142
kind = "pursuit"
timestamp = "2026-10-12T09:24:04+00:00"
summary = "pursuit prove T0458: WITNESSED — refuses when beagle.py's `{'pass' if _lean() else 'be locked'}` is put back as `be locked`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "6ccc0a33f7d284742a65e140e75e7448b6b4329507ef7c9109542a616b8dae8c  .beagle/checks/T0458/T0458.sh" | sha256sum -c --quiet && bash .beagle/checks/T0458/T0458.sh'
refutes: refuses when beagle.py's `{'pass' if _lean() else 'be locked'}` is put back as `be locked` (proven 2026-10-12T09:24:03+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_lean_switch_drops_lock_promises_from_driver_texts)
refused after 4s of a 2m48s check at: FAILED tests/test_beagle_example_extension.py::test_lean_switch_drops_lock_promises_from_driver_texts
refused with: 1 failed, 806 deselected in 3.29s
