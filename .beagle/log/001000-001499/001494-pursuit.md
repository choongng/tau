+++
id = "001494-pursuit"
ordinal = 1494
kind = "pursuit"
timestamp = "2026-10-10T04:06:45+00:00"
summary = "pursuit amend T0335"
metric_command = ""
drains = []
hooks = []
+++

audit 13: T0336 put tau-subagents test names on R38.md, which this check could not resolve; the shared resolver also looks in the tau-subagents repo
was: sh -c 'echo "449b5938ad86b2213f9f8313ae599e73d532800c027ba6dfdbd039cdd6aae4aa  .beagle/checks/T0335/T0335.sh" | sha256sum -c --quiet && bash .beagle/checks/T0335/T0335.sh'
  449b5938ad86b2213f9f8313ae599e73d532800c027ba6dfdbd039cdd6aae4aa  .beagle/checks/T0335/T0335.sh
now: sh -c 'echo "56b7de345ab610dc1bfacb75c912ed1b28c6ba0302f440a315d220cedbd6a80f  .beagle/checks/T0335/T0335b.sh" | sha256sum -c --quiet && bash .beagle/checks/T0335/T0335b.sh'
