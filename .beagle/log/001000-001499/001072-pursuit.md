+++
id = "001072-pursuit"
ordinal = 1072
kind = "pursuit"
timestamp = "2026-10-05T11:53:18+00:00"
summary = "pursuit prove T0260: WITNESSED — refuses when beagle.py's `locks, outside = _root_relative_scope(_strings(…` is put back as `locks, outside = (_strings(arguments.get(\"locks…`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "aec6a4c92555d4c013cacc0826f44cbfa4d0e6e2196a51e22b3aef35402ebf6a  .beagle/checks/T0260/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0260/check.sh'
refutes: refuses when beagle.py's `locks, outside = _root_relative_scope(_strings(…` is put back as `locks, outside = (_strings(arguments.get("locks…` (proven 2026-10-05T11:53:18+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_step_locks_made_root_relative)
refused after 4s of a 1m46s check at: FAILED tests/test_beagle_example_extension.py::test_step_locks_made_root_relative
refused with: 1 failed in 3.22s
