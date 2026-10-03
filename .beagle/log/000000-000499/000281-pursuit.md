+++
id = "000281-pursuit"
ordinal = 281
kind = "pursuit"
timestamp = "2026-10-03T20:02:11+00:00"
summary = "pursuit prove T0067: WITNESSED — refuses when beagle.py's `entries.extend(_scope_dir_files(root, rel.rstri…` is put back as `pass`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "bba7aecda4842179c7e3411ad74de0da4026921a0a59f453db30bff6f1567fb5  .beagle/checks/T0067/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0067/check.sh'
refutes: refuses when beagle.py's `entries.extend(_scope_dir_files(root, rel.rstri…` is put back as `pass` (proven 2026-10-03T20:01:39+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_step_refuses_directory_scopes_holding_unlocked_data_and_source)
refused after 1s of a 1s check at: FAILED tests/test_beagle_example_extension.py::test_step_refuses_directory_scopes_holding_unlocked_data_and_source
refused with: 1 failed, 1 passed, 266 deselected in 0.77s
