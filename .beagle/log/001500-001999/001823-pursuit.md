+++
id = "001823-pursuit"
ordinal = 1823
kind = "pursuit"
timestamp = "2026-10-11T22:35:41+00:00"
summary = "pursuit prove T0440: WITNESSED — refuses when beagle.py's `and any(given(arg) for arg in [*node.args, *(k.…` is put back as ``"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "779eb2910c0ef353a378b22e74bb8ba29eddc0d5e0099d5f45fa7026fa51d7c4  .beagle/checks/T0440/T0440.sh" | sha256sum -c --quiet && bash .beagle/checks/T0440/T0440.sh'
refutes: refuses when beagle.py's `and any(given(arg) for arg in [*node.args, *(k.…` is put back as `` (proven 2026-10-11T22:35:39+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_cases_test_with_only_a_data_loader_is_not_an_own_copy)
refused after 9s of a 5m04s check at: FAILED tests/test_beagle_example_extension.py::test_cases_test_with_only_a_data_loader_is_not_an_own_copy
refused with: 1 failed, 1 passed, 758 deselected in 8.02s
