+++
id = "000268-pursuit"
ordinal = 268
kind = "pursuit"
timestamp = "2026-10-03T19:58:22+00:00"
summary = "pursuit prove T0076: WITNESSED — refuses when tool_buffers.py's `max_lines = None if head and limit is not None …` is put back as `max_lines = None if head and limit is not None …`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "046fa8749ef5e333f87f5a872ea0ebc2a83338eed1a46f70e111fb0c39a47889  .beagle/checks/T0076/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0076/check.sh'
refutes: refuses when tool_buffers.py's `max_lines = None if head and limit is not None …` is put back as `max_lines = None if head and limit is not None …` (proven 2026-10-03T19:57:51+00:00; predates the task: T0076 confirms T0070's commit 779903b, which wrote both tests; the mutation drops the read offset 
refused after 1s of a 1s check at: FAILED tests/test_tool_buffers.py::test_cut_read_through_session_outline_carries_file_line_numbers[asyncio]
refused with: 1 failed, 1 passed, 9 deselected in 0.43s
