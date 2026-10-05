+++
id = "000923-pursuit"
ordinal = 923
kind = "pursuit"
timestamp = "2026-10-05T06:12:34+00:00"
summary = "pursuit open T0230: The amend path keeps the data-only bind"
metric_command = ""
drains = []
hooks = []
+++

criteria: When pursuit_step amends an open known-answers task's done_when to one naming a cases test not on disk, or one importing an unwritten module, tau binds the data test only, as the open path does (T0225), with the same lead; it never binds a check that its own result says cannot pass.
decided by: sh -c 'echo "af079428ee0eeea09eafebb9306216a839adfdbce8e6af4a016bf15fb98e347c  .beagle/checks/T0230/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0230/check.sh'
budget: 60000 tokens
