+++
id = "001117-pursuit"
ordinal = 1117
kind = "pursuit"
timestamp = "2026-10-05T14:16:13+00:00"
summary = "pursuit prove T0270: WITNESSED — refuses when session.py's `arguments = _dedupe_lists(call.arguments)` is put back as `arguments = call.arguments`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "a4da49f54db675f0c92a1aef0c053306b82f7b9e24bb35fc3af5b5aeb4abcab9  .beagle/checks/T0270/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0270/check.sh'
refutes: refuses when session.py's `arguments = _dedupe_lists(call.arguments)` is put back as `arguments = call.arguments` (proven 2026-10-05T14:15:16+00:00; refused at FAILED tests/test_repeat_breaker_reset.py::test_call_key_ignores_duplicate_list_entries)
refused after 1s of a 3s check at: FAILED tests/test_repeat_breaker_reset.py::test_call_key_ignores_duplicate_list_entries
refused with: 1 failed in 0.41s
replaces: refuses when session.py's `arguments = _dedupe_lists(call.arguments)` is put back as `arguments = call.arguments` (proven 2026-10-05T14:14:07+00:00; refused at FAILED tests/test_repeat_breaker_reset.py::test_call_key_ignores_duplicate_list_entries)
