+++
id = "000409-pursuit"
ordinal = 409
kind = "pursuit"
timestamp = "2026-10-04T00:44:39+00:00"
summary = "pursuit open T0106: R11 diagnose (breaker class folded in)"
metric_command = ""
drains = []
hooks = []
+++

criteria: R11.md diagnosed: each failure class has Evidence and an Action naming a file or a Disposition; upstream recorded or 'upstream: none'
decided by: sh -c 'echo "341018b03f6000c822f19008a77c996a0bb2cd4a5bea6d486570ec2a1edfa751  .beagle/checks/T0106/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0106/check.sh'
budget: 15000 tokens
