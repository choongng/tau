+++
id = "000208-pursuit"
ordinal = 208
kind = "pursuit"
timestamp = "2026-10-03T18:29:38+00:00"
summary = "pursuit prove T0060: WITNESSED — refuses when tool_buffers.py's `else first_line + index` is put back as `else index`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "0c801f9020570e56e945e1548a0599deb721235031abfcf4d0d812b959615ab2  .beagle/checks/T0060/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0060/check.sh'
refutes: refuses when tool_buffers.py's `else first_line + index` is put back as `else index` (proven 2026-10-03T18:29:12+00:00; refused at FAILED tests/test_tool_buffers.py::test_cut_read_of_python_lists_definitions_with_line_numbers[asyncio])
refused after 1s of a 1s check at: FAILED tests/test_tool_buffers.py::test_cut_read_of_python_lists_definitions_with_line_numbers[asyncio]
refused with: 1 failed, 1 passed, 4 deselected in 0.43s
