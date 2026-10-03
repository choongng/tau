+++
id = "000127-pursuit"
ordinal = 127
kind = "pursuit"
timestamp = "2026-10-03T15:32:28+00:00"
summary = "pursuit prove T0044: WITNESSED — refuses when beagle.py's `alone = not interactive()` is put back as `alone = False`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "74d183e355a25a79c0eda551ba2ee43b6acc65c4a7531fd7ab703907c9f336e2  .beagle/checks/T0044/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0044/check.sh'
refutes: refuses when beagle.py's `alone = not interactive()` is put back as `alone = False` (proven 2026-10-03T15:32:07+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_print_mode_stop_gate_objects_once_to_an_unfounded_stop_after_a_conf…)
refused after 1s of a 1s check at: FAILED tests/test_beagle_example_extension.py::test_print_mode_stop_gate_objects_once_to_an_unfounded_stop_after_a_conf…
refused with: 1 failed, 2 passed, 233 deselected in 0.64s
