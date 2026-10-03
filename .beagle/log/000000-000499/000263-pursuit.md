+++
id = "000263-pursuit"
ordinal = 263
kind = "pursuit"
timestamp = "2026-10-03T19:57:23+00:00"
summary = "pursuit prove T0070: WITNESSED — refuses when tool_buffers.py's `max_lines = None if head and limit is not None …` is put back as `max_lines = limits.window_lines`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "06dd477427036a9299beadee58da41a3168810b76e6e790d084e6a80cf881f00  .beagle/checks/T0070/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0070/check.sh'
refutes: refuses when tool_buffers.py's `max_lines = None if head and limit is not None …` is put back as `max_lines = limits.window_lines` (proven 2026-10-03T19:56:53+00:00; refused at FAILED tests/test_tool_buffers.py::test_read_with_explicit_limit_fills_the_char_window[asyncio])
refused after 1s of a 1s check at: FAILED tests/test_tool_buffers.py::test_read_with_explicit_limit_fills_the_char_window[asyncio]
refused with: 1 failed, 2 passed, 8 deselected in 0.40s
