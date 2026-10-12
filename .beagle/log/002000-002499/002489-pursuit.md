+++
id = "002489-pursuit"
ordinal = 2489
kind = "pursuit"
timestamp = "2026-10-12T16:39:20+00:00"
summary = "pursuit prove T0486: WITNESSED — refuses when pursuit.py's `refuse_whole_tree_status(check, what=what)` is put back as `pass`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "3bc32e40573f9e2a3beae2a59691e3d9546c11fa43668ded3d089d2b09e2342f  .beagle/checks/T0486/T0486.sh" | sha256sum -c --quiet && bash .beagle/checks/T0486/T0486.sh'
refutes: refuses when pursuit.py's `refuse_whole_tree_status(check, what=what)` is put back as `pass` (proven 2026-10-12T16:38:23+00:00; refused at FAILED tests/test_pursuit.py::test_open_refuses_a_check_that_needs_the_whole_tree_clean)
refused after 1s of a 14s check at: FAILED tests/test_pursuit.py::test_open_refuses_a_check_that_needs_the_whole_tree_clean
refused with: 1 failed, 7 passed, 502 deselected in 0.33s
standing checks red: T0335, T0360, T0368, T0386, T0419, T0420, T0421, T0422, T0423, T0424, T0425, T0426, T0336
