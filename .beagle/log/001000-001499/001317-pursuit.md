+++
id = "001317-pursuit"
ordinal = 1317
kind = "pursuit"
timestamp = "2026-10-09T21:58:45+00:00"
summary = "pursuit prove T0314: WITNESSED — refuses when beagle.py's `any(_renders_result(text, result) for text in t…` is put back as `any(_renders_result(text, result) for text in t…`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "3923bd3b915ee476e6bf36df8f3565455dff8748757bc211b5a24e7fce83e729  .beagle/checks/T0314/T0314.sh" | sha256sum -c --quiet && bash .beagle/checks/T0314/T0314.sh'
refutes: refuses when beagle.py's `any(_renders_result(text, result) for text in t…` is put back as `any(_renders_result(text, result) for text in t…` (proven 2026-10-09T21:58:45+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_result_unquoted_requires_each_changed_field)
refused after 1s of a 1m39s check at: FAILED tests/test_beagle_example_extension.py::test_result_unquoted_requires_each_changed_field
refused with: 1 failed, 1 passed in 0.85s
