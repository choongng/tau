+++
id = "000898-pursuit"
ordinal = 898
kind = "pursuit"
timestamp = "2026-10-05T04:45:14+00:00"
summary = "pursuit prove T0225: WITNESSED — refuses when beagle.py's `absent_route = _absent_test_route(done_when, sc…` is put back as `absent_route = None`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "6162c01b661603eea4fc2a31a4083621778787742be58a7fbb2444b870dae567  .beagle/checks/T0225/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0225/check.sh'
refutes: refuses when beagle.py's `absent_route = _absent_test_route(done_when, sc…` is put back as `absent_route = None` (proven 2026-10-05T04:45:00+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_known_answers_open_binds_data_test_when_the_cases_test_is_not_on_di…)
refused after 2s of a 1m13s check at: FAILED tests/test_beagle_example_extension.py::test_known_answers_open_binds_data_test_when_the_cases_test_is_not_on_di…
refused with: 1 failed in 1.93s
