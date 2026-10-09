+++
id = "001322-pursuit"
ordinal = 1322
kind = "pursuit"
timestamp = "2026-10-09T22:03:07+00:00"
summary = "pursuit prove T0315: WITNESSED — refuses when beagle.py's `|<\\|(?:tool_call|channel)>|<(?:tool_call|channe…` is put back as ``"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "cd7882e7037a4ff4b18078367b9de78ab1964a9ec2682003f442abb9d637ce61  .beagle/checks/T0315/T0315.sh" | sha256sum -c --quiet && bash .beagle/checks/T0315/T0315.sh'
refutes: refuses when beagle.py's `|<\|(?:tool_call|channel)>|<(?:tool_call|channe…` is put back as `` (proven 2026-10-09T22:03:07+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_tool_call_markup_matches_channel_tokens)
refused after 1s of a 1m40s check at: FAILED tests/test_beagle_example_extension.py::test_tool_call_markup_matches_channel_tokens
refused with: 1 failed in 0.83s
