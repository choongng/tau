+++
id = "000970-pursuit"
ordinal = 970
kind = "pursuit"
timestamp = "2026-10-05T07:50:30+00:00"
summary = "pursuit prove T0238: WITNESSED — refuses when beagle.py's `if data_test == test:` is put back as `if False:`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "3fb0dc72db81355dd814d8eea68b647e022208caeeaecf07064f5d52c8023562  .beagle/checks/T0238/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0238/check.sh'
refutes: refuses when beagle.py's `if data_test == test:` is put back as `if False:` (proven 2026-10-05T07:50:21+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_data_test_route_does_not_propose_the_importing_test_itself)
refused after 2s of a 1m19s check at: FAILED tests/test_beagle_example_extension.py::test_data_test_route_does_not_propose_the_importing_test_itself
refused with: 1 failed in 2.04s
