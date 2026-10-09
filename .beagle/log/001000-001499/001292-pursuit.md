+++
id = "001292-pursuit"
ordinal = 1292
kind = "pursuit"
timestamp = "2026-10-09T21:23:19+00:00"
summary = "pursuit prove T0308: WITNESSED — refuses when session.py's `\"\"\"Take the next reasoning delta; return whethe…` is put back as `\"\"\"Take the next reasoning delta; return whethe…`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "f88c1d66e61888978e5a7a549ed587e217c27da626ca9eb3f017e81ac9b61b7e  .beagle/checks/T0308/T0308.sh" | sha256sum -c --quiet && bash .beagle/checks/T0308/T0308.sh'
refutes: refuses when session.py's `"""Take the next reasoning delta; return whethe…` is put back as `"""Take the next reasoning delta; return whethe…` (proven 2026-10-09T21:22:21+00:00; refused at FAILED tests/test_session_output_limit.py::test_reasoning_repetition_stops_turn_as_output_limit[asyncio])
refused after 1s of a 4s check at: FAILED tests/test_session_output_limit.py::test_reasoning_repetition_stops_turn_as_output_limit[asyncio]
refused with: 1 failed in 0.44s
