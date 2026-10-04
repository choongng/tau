+++
id = "000783-pursuit"
ordinal = 783
kind = "pursuit"
timestamp = "2026-10-04T23:21:23+00:00"
summary = "pursuit prove T0201: WITNESSED — refuses when beagle.py's `if _own_files(waiter, rel, nodes, root):` is put back as `if False and _own_files(waiter, rel, nodes, roo…`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "552d522b936663a5de97955e83929d1e32ade80ed15f85fe1dbc2878fb6e7e68  .beagle/checks/T0201/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0201/check.sh'
refutes: refuses when beagle.py's `if _own_files(waiter, rel, nodes, root):` is put back as `if False and _own_files(waiter, rel, nodes, roo…` (proven 2026-10-04T23:21:02+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_check_running_a_waiting_siblings_file_is_refused_at_open)
refused after 2s of a 1m05s check at: FAILED tests/test_beagle_example_extension.py::test_check_running_a_waiting_siblings_file_is_refused_at_open
refused with: 1 failed in 2.12s
