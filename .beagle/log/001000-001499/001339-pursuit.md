+++
id = "001339-pursuit"
ordinal = 1339
kind = "pursuit"
timestamp = "2026-10-09T22:30:25+00:00"
summary = "pursuit prove T0317: WITNESSED — refuses when beagle.py's `for name, source in flagged[1:]:` is put back as `for name, source in flagged[1:1]:`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "1a132151a94eb213635e5414830ab7b428707a7bed8f54eefdd2af5af3e931e6  .beagle/checks/T0317/T0317.sh" | sha256sum -c --quiet && bash .beagle/checks/T0317/T0317.sh'
refutes: refuses when beagle.py's `for name, source in flagged[1:]:` is put back as `for name, source in flagged[1:1]:` (proven 2026-10-09T22:30:25+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_unquoted_cases_verdict_shows_each_named_case_source)
refused after 1s of a 1m40s check at: FAILED tests/test_beagle_example_extension.py::test_unquoted_cases_verdict_shows_each_named_case_source
refused with: 1 failed, 1 passed in 0.99s
