+++
id = "000415-pursuit"
ordinal = 415
kind = "pursuit"
timestamp = "2026-10-04T00:51:23+00:00"
summary = "pursuit prove T0107: WITNESSED — refuses when beagle.py's `inferred = _inferred_delegation(statement) if a…` is put back as `inferred = None`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "d25e9a33433f75f3c29264c708e64f0e22636bf420676a52e9e62fc832e40e35  .beagle/checks/T0107/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0107/check.sh'
refutes: refuses when beagle.py's `inferred = _inferred_delegation(statement) if a…` is put back as `inferred = None` (proven 2026-10-04T00:50:35+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_print_mode_found_infers_delegation_from_a_delegating_prompt)
refused after 1s of a 29s check at: FAILED tests/test_beagle_example_extension.py::test_print_mode_found_infers_delegation_from_a_delegating_prompt
refused with: 1 failed in 0.45s
