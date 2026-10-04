+++
id = "000509-pursuit"
ordinal = 509
kind = "pursuit"
timestamp = "2026-10-04T04:19:42+00:00"
summary = "pursuit prove T0115: WITNESSED — refuses when beagle.py's `if cases and 2 * len(unfound) > len(cases):` is put back as `if False:`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "0dfc8d7bd5efdc4c1293479402008663e8f852740b8b16dbce04ac8ba880e48f  .beagle/checks/T0115/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0115/check.sh'
refutes: refuses when beagle.py's `if cases and 2 * len(unfound) > len(cases):` is put back as `if False:` (proven 2026-10-04T04:18:53+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_close_keeps_cases_open_when_most_sources_quote_nothing)
refused after 1s of a 32s check at: FAILED tests/test_beagle_example_extension.py::test_close_keeps_cases_open_when_most_sources_quote_nothing
refused with: 1 failed in 0.84s
