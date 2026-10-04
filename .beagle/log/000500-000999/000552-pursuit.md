+++
id = "000552-pursuit"
ordinal = 552
kind = "pursuit"
timestamp = "2026-10-04T06:52:50+00:00"
summary = "pursuit prove T0133: WITNESSED — refuses when beagle.py's `if arguments.get(\"new_route\") is not True:` is put back as `if False:`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "97a005730249b545fb11d2a6d092d5a8d9456d72416a04d6b48856db3b466a78  .beagle/checks/T0133/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0133/check.sh'
refutes: refuses when beagle.py's `if arguments.get("new_route") is not True:` is put back as `if False:` (proven 2026-10-04T06:52:02+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_escalation_names_the_missing_new_route_flag)
refused after 1s of a 39s check at: FAILED tests/test_beagle_example_extension.py::test_escalation_names_the_missing_new_route_flag
refused with: 1 failed in 1.10s
