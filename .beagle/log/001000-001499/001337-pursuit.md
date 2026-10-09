+++
id = "001337-pursuit"
ordinal = 1337
kind = "pursuit"
timestamp = "2026-10-09T22:25:13+00:00"
summary = "pursuit prove T0318: WITNESSED — refuses when beagle.py's `_renders_result(text, result, whole=True)` is put back as `_renders_result(text, result, whole=False)`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "c0eebbedcd2c039acd1f640fe1978453038f9b630a989ba608858f353619e37a  .beagle/checks/T0318/T0318.sh" | sha256sum -c --quiet && bash .beagle/checks/T0318/T0318.sh'
refutes: refuses when beagle.py's `_renders_result(text, result, whole=True)` is put back as `_renders_result(text, result, whole=False)` (proven 2026-10-09T22:25:13+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_narrow_result_inside_a_larger_token_on_next_line_is_not_found)
refused after 1s of a 1m42s check at: FAILED tests/test_beagle_example_extension.py::test_narrow_result_inside_a_larger_token_on_next_line_is_not_found
refused with: 1 failed in 0.65s
