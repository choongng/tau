+++
id = "002960-pursuit"
ordinal = 2960
kind = "pursuit"
timestamp = "2026-10-14T03:25:44+00:00"
summary = "pursuit open T0576: beagle: contract add's unnamed-source refusal says how to name a source (S01 #1)"
metric_command = ""
drains = []
hooks = []
+++

criteria: When contract add (and check) refuses an entry because its source is not named in the contract's sources, the refusal gives, in one line, the exact way to name it (the command, e.g. beagle refs fetch / a contract verb, or the sources field and its shape); contract add --help says the same; test(s) *unnamed_source_refusal_says_how* pass; ci/check.sh green.
decided by: sh -c 'echo "17cf03560dbce44f04dc0923b3ceb9b254fd0aa5148e34e21ff38423c7f75a0e  .beagle/checks/T0576/T0576.sh" | sha256sum -c --quiet && bash .beagle/checks/T0576/T0576.sh'
budget: 50000 tokens
opened over T0568, T0573, T0575, T0565, T0569, T0572: beagle lane beside the tau lane: T0568 shares T0567's files, so it cannot run beside it
