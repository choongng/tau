+++
id = "000079-pursuit"
ordinal = 79
kind = "pursuit"
timestamp = "2026-10-03T13:03:12+00:00"
summary = "pursuit prove T0036: WITNESSED — refuses when openai_compatible.py's `\"enable_thinking\": reasoning_enabled, \"preserve…` is put back as `\"enable_thinking\": True, \"preserve_thinking\": T…`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "61f8d2b6d07d1b3d90d30bc15d13dda5edeee787b714ebe416c88c2465804856  .beagle/checks/T0036/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0036/check.sh'
refutes: refuses when openai_compatible.py's `"enable_thinking": reasoning_enabled, "preserve…` is put back as `"enable_thinking": True, "preserve_thinking": T…` (proven 2026-10-03T13:03:00+00:00; predates the task: the task's change is only tests, and one of them refused; refused at FAILED tests/test_tau_ai
refused after 1s of a 0s check at: FAILED tests/test_tau_ai.py::test_qwen_chat_template_thinking_off_disables_in_payload[asyncio]
refused with: 1 failed, 91 deselected in 0.26s
standing checks red: T0030
