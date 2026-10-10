+++
id = "001524-pursuit"
ordinal = 1524
kind = "pursuit"
timestamp = "2026-10-10T04:49:37+00:00"
summary = "pursuit prove T0350: WITNESSED — refuses when beagle.py's `and not (root / path).exists()` is put back as `and (root / path).exists()`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "733979462aee4f8dd176f4dd1e08b58da7ed547d7c87641cd5d4e7f9b7009da5  .beagle/checks/T0350/T0350.sh" | sha256sum -c --quiet && bash .beagle/checks/T0350/T0350.sh'
refutes: refuses when beagle.py's `and not (root / path).exists()` is put back as `and (root / path).exists()` (proven 2026-10-10T04:49:37+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_open_refuses_check_running_absent_file_outside_scope)
refused after 2s of a 1m48s check at: FAILED tests/test_beagle_example_extension.py::test_open_refuses_check_running_absent_file_outside_scope
refused with: 2 failed, 1 passed, 684 deselected in 1.43s
