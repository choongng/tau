+++
id = "000877-pursuit"
ordinal = 877
kind = "pursuit"
timestamp = "2026-10-05T04:06:53+00:00"
summary = "pursuit prove T0221: WITNESSED — refuses when beagle.py's `return name == \"__init__.py\" and _in_tests_dir(…` is put back as `return _in_tests_dir(rel)`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "65bc62f2e2dc3f411a980b96305bf9c14f47d9a04c384ba6650c283fca5766e4  .beagle/checks/T0221/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0221/check.sh'
refutes: refuses when beagle.py's `return name == "__init__.py" and _in_tests_dir(…` is put back as `return _in_tests_dir(rel)` (proven 2026-10-05T04:06:35+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_non_test_py_under_tests_is_refused_as_scope_with_a_root_module_call)
refused after 2s of a 1m09s check at: FAILED tests/test_beagle_example_extension.py::test_non_test_py_under_tests_is_refused_as_scope_with_a_root_module_call
refused with: 1 failed in 1.97s
