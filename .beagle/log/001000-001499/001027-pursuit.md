+++
id = "001027-pursuit"
ordinal = 1027
kind = "pursuit"
timestamp = "2026-10-05T09:57:22+00:00"
summary = "pursuit prove T0250: WITNESSED — refuses when beagle.py's `imported = \" \" + _self_import_note(bound, scope…` is put back as `imported = \"\"`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "bdfce9d8c7fd7c1ba9fc36ea2eb488eac36dc8db34d4ac5735a169577887a953  .beagle/checks/T0250/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0250/check.sh'
refutes: refuses when beagle.py's `imported = " " + _self_import_note(bound, scope…` is put back as `imported = ""` (proven 2026-10-05T09:57:22+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_scope_guard_out_of_scope_import_from_data_test_says_remove_import)
refused after 4s of a 1m38s check at: FAILED tests/test_beagle_example_extension.py::test_scope_guard_out_of_scope_import_from_data_test_says_remove_import
refused with: 1 failed, 2 passed in 3.39s
