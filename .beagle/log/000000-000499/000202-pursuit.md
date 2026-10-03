+++
id = "000202-pursuit"
ordinal = 202
kind = "pursuit"
timestamp = "2026-10-03T18:26:53+00:00"
summary = "pursuit prove T0059: WITNESSED — refuses when beagle.py's `if not data or not source: return None return (…` is put back as `if True: return None return ( f\"scope holds kno…`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "40c745dc2079317c28b5a8b90c78f526f00c543f0235d21039ce81bb0e724d11  .beagle/checks/T0059/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0059/check.sh'
refutes: refuses when beagle.py's `if not data or not source: return None return (…` is put back as `if True: return None return ( f"scope holds kno…` (proven 2026-10-03T18:26:28+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_step_refuses_a_scope_mixing_known_answer_data_with_source)
refused after 1s of a 1s check at: FAILED tests/test_beagle_example_extension.py::test_step_refuses_a_scope_mixing_known_answer_data_with_source
refused with: 1 failed, 1 passed, 255 deselected in 0.78s
