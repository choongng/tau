+++
id = "001708-pursuit"
ordinal = 1708
kind = "pursuit"
timestamp = "2026-10-11T00:16:35+00:00"
summary = "pursuit prove T0392: WITNESSED — refuses when beagle.py's `return bool(bound) and _check_problem(bound) is…` is put back as `return bool(bound) and _check_problem(bound) is…`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "83977452e07bb62f66fb41574df5ffb1f1533f67ef68c6d1f9843148ec149d68  .beagle/checks/T0392/T0392.sh" | sha256sum -c --quiet && bash .beagle/checks/T0392/T0392.sh'
refutes: refuses when beagle.py's `return bool(bound) and _check_problem(bound) is…` is put back as `return bool(bound) and _check_problem(bound) is…` (proven 2026-10-11T00:16:34+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_kept_bound_note_refuses_an_inverted_bound_check)
refused after 2s of a 2m12s check at: FAILED tests/test_beagle_example_extension.py::test_kept_bound_note_refuses_an_inverted_bound_check
refused with: 1 failed, 2 passed, 725 deselected in 1.43s
replaces: refuses when beagle.py's `if name is not None and _is_bool_expr(node.args…` is put back as `if False:` (proven 2026-10-11T00:14:19+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_open_refuses_a_python_c_check_with_a_bool_exit)
