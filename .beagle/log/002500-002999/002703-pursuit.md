+++
id = "002703-pursuit"
ordinal = 2703
kind = "pursuit"
timestamp = "2026-10-13T15:07:33+00:00"
summary = "pursuit prove T0527: WITNESSED — refuses when loop.py's `if not isinstance(message, AssistantMessage) or…` is put back as `if not isinstance(message, AssistantMessage) or…`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "64cfc54562745acdbf515c35c91642ef91b9c7b703650fe52c8d41e887136699  .beagle/checks/T0527/T0527.sh" | sha256sum -c --quiet && bash .beagle/checks/T0527/T0527.sh'
refutes: refuses when loop.py's `if not isinstance(message, AssistantMessage) or…` is put back as `if not isinstance(message, AssistantMessage) or…` (proven 2026-10-13T15:06:34+00:00; refused at 1 failed, 14 passed in 1.29s)
refused after 2s of a 1s check at: 1 failed, 14 passed in 1.29s
refused with: 1 failed, 14 passed in 1.29s
