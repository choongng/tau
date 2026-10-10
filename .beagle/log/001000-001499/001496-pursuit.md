+++
id = "001496-pursuit"
ordinal = 1496
kind = "pursuit"
timestamp = "2026-10-10T04:07:54+00:00"
summary = "pursuit prove T0335: WITNESSED — refuses when R36.md's `::test_tool_args_with_template_tokens_refused` is put back as `::test_tool_args_with_template_tokens_rejected`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "56b7de345ab610dc1bfacb75c912ed1b28c6ba0302f440a315d220cedbd6a80f  .beagle/checks/T0335/T0335b.sh" | sha256sum -c --quiet && bash .beagle/checks/T0335/T0335b.sh'
refutes: refuses when R36.md's `::test_tool_args_with_template_tokens_refused` is put back as `::test_tool_args_with_template_tokens_rejected` (proven 2026-10-10T04:07:54+00:00; refused at Traceback (most recent call last):)
refused after 0s of a 0s check at: Traceback (most recent call last):
refused with: dev-notes/itc-runs/R36.md: tests/test_session_template_tokens.py::test_tool_args_with_template_tokens_rejected
