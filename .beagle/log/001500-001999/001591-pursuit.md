+++
id = "001591-pursuit"
ordinal = 1591
kind = "pursuit"
timestamp = "2026-10-10T17:15:32+00:00"
summary = "pursuit prove T0370: WITNESSED — refuses when beagle.py's `self_imported = _data_test_unwritten_import(che…` is put back as `self_imported = None`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "f955ac78d7088cec51c9968ab9fd2acd8ac4551892f9c5d7668203b86c85f643  .beagle/checks/T0370/T0370.sh" | sha256sum -c --quiet && bash .beagle/checks/T0370/T0370.sh'
refutes: refuses when beagle.py's `self_imported = _data_test_unwritten_import(che…` is put back as `self_imported = None` (proven 2026-10-10T17:15:31+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_not_done_names_data_test_importing_unwritten_module)
refused after 2s of a 1m48s check at: FAILED tests/test_beagle_example_extension.py::test_not_done_names_data_test_importing_unwritten_module
refused with: 2 failed, 699 deselected in 1.64s
