+++
id = "001707-pursuit"
ordinal = 1707
kind = "pursuit"
timestamp = "2026-10-11T00:14:20+00:00"
summary = "pursuit prove T0392: WITNESSED — refuses when beagle.py's `if name is not None and _is_bool_expr(node.args…` is put back as `if False:`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "83977452e07bb62f66fb41574df5ffb1f1533f67ef68c6d1f9843148ec149d68  .beagle/checks/T0392/T0392.sh" | sha256sum -c --quiet && bash .beagle/checks/T0392/T0392.sh'
refutes: refuses when beagle.py's `if name is not None and _is_bool_expr(node.args…` is put back as `if False:` (proven 2026-10-11T00:14:19+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_open_refuses_a_python_c_check_with_a_bool_exit)
refused after 4s of a 2m12s check at: FAILED tests/test_beagle_example_extension.py::test_open_refuses_a_python_c_check_with_a_bool_exit
refused with: 2 failed, 1 passed, 725 deselected in 4.16s
