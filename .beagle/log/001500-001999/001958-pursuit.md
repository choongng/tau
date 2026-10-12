+++
id = "001958-pursuit"
ordinal = 1958
kind = "pursuit"
timestamp = "2026-10-12T04:40:51+00:00"
summary = "pursuit open T0451: Fix commits carry a Task: trailer"
metric_command = ""
drains = []
hooks = []
+++

criteria: Every fix task since the 2026-10-12 audit (T0447, T0449, T0452) has its beagle.py commits carrying a 'Task: TNNNN' trailer, so git log --grep finds them
decided by: sh -c 'echo "1b6e6035a144655c641c375afefd0054602d9f5e400621b73900dcfd3349d2f7  .beagle/checks/T0451/T0451.sh" | sha256sum -c --quiet && bash .beagle/checks/T0451/T0451.sh'
budget: 150000 tokens
opened over T0419: R0002
