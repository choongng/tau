+++
id = "003136-pursuit"
ordinal = 3136
kind = "pursuit"
timestamp = "2026-10-14T21:50:39+00:00"
summary = "pursuit open T0603: hand back policy text 0.48 carries (T0586, scoped): delete tau's copies, file what beagle lacks as upstream asks"
metric_command = ""
drains = []
hooks = []
+++

criteria: On branch beagle-0.48: dev-notes/beagle-0.48/decide-carry.md audits the extension's policy text (prompts, notes, refusal wording, Next: lines) against what beagle 0.48's brief, rules, refusals and next: lines carry, one row each: deleted (beagle carries it; tau's copy is gone), kept (a host's to carry, with why), or ask (beagle lacks it; filed in upstream-asks.md). The cases dispatch role is filed as an ask. The extension's suites pass.
decided by: sh -c 'echo "abc63bac1db337c7b5f58d0c980458569d56e959c298397d8f7db5b4ee4f2a19  .beagle/checks/T0603/T0603.sh" | sha256sum -c --quiet && bash .beagle/checks/T0603/T0603.sh'
budget: 300000 tokens
