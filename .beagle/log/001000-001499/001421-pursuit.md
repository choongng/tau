+++
id = "001421-pursuit"
ordinal = 1421
kind = "pursuit"
timestamp = "2026-10-10T02:21:43+00:00"
summary = "pursuit prove T0336: WITNESSED — refuses when extension.py's `session._runtime_provider_config = selection.pr…` is put back as `pass`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "1f496e64c7f0ef3712f1b79366ec31c0d4d71f1b62db01f324cfdc2c94ed3461  .beagle/checks/T0336/T0336.sh" | sha256sum -c --quiet && bash .beagle/checks/T0336/T0336.sh'
refutes: refuses when extension.py's `session._runtime_provider_config = selection.pr…` is put back as `pass` (proven 2026-10-10T02:20:46+00:00; refused at ../../tau-subagents/tests/test_extension.py:3030: AssertionError)
refused after 1s of a 1s check at: ../../tau-subagents/tests/test_extension.py:3030: AssertionError
refused with: 2 failed, 81 deselected in 0.59s
standing checks red: T0335
