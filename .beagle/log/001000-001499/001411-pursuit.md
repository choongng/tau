+++
id = "001411-pursuit"
ordinal = 1411
kind = "pursuit"
timestamp = "2026-10-10T02:18:37+00:00"
summary = "pursuit prove T0335: WITNESSED — refuses when R36.md's `tests/test_session_template_tokens.py::test_too…` is put back as `tests/test_tools.py::test_tool_args_with_templa…`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "449b5938ad86b2213f9f8313ae599e73d532800c027ba6dfdbd039cdd6aae4aa  .beagle/checks/T0335/T0335.sh" | sha256sum -c --quiet && bash .beagle/checks/T0335/T0335.sh'
refutes: refuses when R36.md's `tests/test_session_template_tokens.py::test_too…` is put back as `tests/test_tools.py::test_tool_args_with_templa…` (proven 2026-10-10T02:17:39+00:00; refused at Traceback (most recent call last):)
refused after 0s of a 0s check at: Traceback (most recent call last):
refused with: dev-notes/itc-runs/R36.md: tests/test_tools.py::test_extension_tool_args_with_template_tokens_refused
