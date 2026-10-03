+++
id = "000213-pursuit"
ordinal = 213
kind = "pursuit"
timestamp = "2026-10-03T18:30:46+00:00"
summary = "pursuit prove T0061: WITNESSED — refuses when beagle.py's `if not ours(names[0]) or any(present(name) for …` is put back as `if True: continue expected = candidates`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "16f5368aa55877cc23c3d548b62a56e25069fbae27033aa8e5be5d489e92bc0e  .beagle/checks/T0061/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0061/check.sh'
refutes: refuses when beagle.py's `if not ours(names[0]) or any(present(name) for …` is put back as `if True: continue expected = candidates` (proven 2026-10-03T18:30:21+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_check_importing_a_module_outside_scope_and_disk_is_refused)
refused after 1s of a 1s check at: FAILED tests/test_beagle_example_extension.py::test_check_importing_a_module_outside_scope_and_disk_is_refused
refused with: 1 failed, 1 passed, 257 deselected in 0.47s
