+++
id = "001142-pursuit"
ordinal = 1142
kind = "pursuit"
timestamp = "2026-10-05T15:56:04+00:00"
summary = "pursuit prove T0275: WITNESSED — refuses when session.py's `head = _call_sentence(text, tools) or head` is put back as `pass`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "8029c80afeee665050867bee0474a6d1bb123b124018ebb6c9dc9a2968f181da  .beagle/checks/T0275/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0275/check.sh'
refutes: refuses when session.py's `head = _call_sentence(text, tools) or head` is put back as `pass` (proven 2026-10-05T15:55:05+00:00; refused at FAILED tests/test_repeat_breaker_reset.py::test_repeated_call_quotes_sentence_holding_the_call)
refused after 1s of a 3s check at: FAILED tests/test_repeat_breaker_reset.py::test_repeated_call_quotes_sentence_holding_the_call
refused with: 1 failed in 0.42s
