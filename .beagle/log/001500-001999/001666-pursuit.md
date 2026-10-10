+++
id = "001666-pursuit"
ordinal = 1666
kind = "pursuit"
timestamp = "2026-10-10T23:17:29+00:00"
summary = "pursuit prove T0389: WITNESSED — refuses when beagle.py's `elif root is not None and (root / rel).is_dir():` is put back as `elif False:`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "7e5d9d7ed0d32e2561dae0c9bf0dc6cbf4a3083ec6a874a74588d84d356c32f0  .beagle/checks/T0389/T0389.sh" | sha256sum -c --quiet && bash .beagle/checks/T0389/T0389.sh'
refutes: refuses when beagle.py's `elif root is not None and (root / rel).is_dir():` is put back as `elif False:` (proven 2026-10-10T23:17:28+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_data_test_unwritten_import_on_a_directory_scope)
refused after 1s of a 2m12s check at: FAILED tests/test_beagle_example_extension.py::test_data_test_unwritten_import_on_a_directory_scope
refused with: 2 failed, 718 deselected in 1.13s
