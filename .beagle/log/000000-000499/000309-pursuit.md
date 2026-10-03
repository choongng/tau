+++
id = "000309-pursuit"
ordinal = 309
kind = "pursuit"
timestamp = "2026-10-03T20:16:26+00:00"
summary = "pursuit open T0074: pursuit_plan names uncommitted files in the split task's scope"
metric_command = ""
drains = []
hooks = []
+++

criteria: pursuit_plan's result, when it splits an open task whose scope holds uncommitted files (git status --porcelain over the scope paths: modified, added or untracked), lists them and says to give each to the part that writes it (with locks when it is data), since the split task's work will otherwise go out in a later part's commit. A clean scope adds nothing. R09: T0007 was split while open with tests/cases.json uncommitted, and T0009's commit took it beside src/itc/*.py, unlocked.
decided by: sh -c 'echo "b354dabeb732ce15b2335d893ef9e86609b36461f53a71db9e21b79495ab7e96  .beagle/checks/T0074/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0074/check.sh'
budget: 25000 tokens
