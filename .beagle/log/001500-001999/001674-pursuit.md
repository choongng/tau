+++
id = "001674-pursuit"
ordinal = 1674
kind = "pursuit"
timestamp = "2026-10-10T23:29:36+00:00"
summary = "pursuit prove T0390: WITNESSED — refuses when beagle.py's `return bool(_result_numbers(value))` is put back as `return bool(value) and all(isinstance(v, int) a…`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "9e9230d8c1000ecc676ef3ac9b547926accfb4ddc709e105d2ffe489900e1857  .beagle/checks/T0390/T0390.sh" | sha256sum -c --quiet && bash .beagle/checks/T0390/T0390.sh'
refutes: refuses when beagle.py's `return bool(_result_numbers(value))` is put back as `return bool(value) and all(isinstance(v, int) a…` (proven 2026-10-10T23:29:36+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_result_unquoted_requires_a_nested_result_not_one_scalar)
refused after 3s of a 2m10s check at: FAILED tests/test_beagle_example_extension.py::test_result_unquoted_requires_a_nested_result_not_one_scalar
refused with: 2 failed, 720 deselected in 3.14s
