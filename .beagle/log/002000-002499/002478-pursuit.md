+++
id = "002478-pursuit"
ordinal = 2478
kind = "pursuit"
timestamp = "2026-10-12T16:26:58+00:00"
summary = "pursuit open T0484: beagle: contract-guard PreToolUse hook"
metric_command = ""
drains = []
hooks = []
+++

criteria: beagle contract-first: a PreToolUse hook 'contract-guard' (Edit|Write|MultiEdit|NotebookEdit), registered, dispatched and paired in doctor, refuses an edit to a file the sealed contract holds, by relative or absolute path, unless an open task that is work on the contract (scope within the contract's paths, relative or absolute) is scoped to it; a task scoped to the whole tree does not let it through. Silent before the seal, without [contract], and on other files. Docs count ten hooks. 2 named tests; the file passes.
decided by: sh -c 'echo "59827c474fa267de99e5719caa55685d7e132e3028d6c3f356ec5ea6bcf0ae3e  .beagle/checks/T0484/T0484.sh" | sha256sum -c --quiet && bash .beagle/checks/T0484/T0484.sh'
budget: 200000 tokens
