+++
id = "001415-pursuit"
ordinal = 1415
kind = "pursuit"
timestamp = "2026-10-10T02:18:55+00:00"
summary = "pursuit open T0337: Audit 12: R38.md names class 3's tests and its tau-subagents cause"
metric_command = ""
drains = []
hooks = []
+++

criteria: R38.md's output-limit class names the tests written for it (T0330, T0331) and the tau-subagents cause with its commit 0236dfe; R38.md points at upstream.md's ## R38 instead of saying upstream: none; R38's diagnose check still passes.
decided by: sh -c 'echo "717f80bae7b4392eca7fafee5cb44c619c6b11e95b6b0325b0918a2339e6178b  .beagle/checks/T0337/T0337.sh" | sha256sum -c --quiet && bash .beagle/checks/T0337/T0337.sh'
budget: 8000 tokens
