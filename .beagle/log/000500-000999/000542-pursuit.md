+++
id = "000542-pursuit"
ordinal = 542
kind = "pursuit"
timestamp = "2026-10-04T06:02:38+00:00"
summary = "pursuit open T0131: R15 diagnose"
metric_command = ""
drains = []
hooks = []
+++

criteria: dev-notes/itc-runs/R15.md has a trace analysis and failure classes, each with Evidence and an Action or Disposition; every [tau] Action names beagle.py or a tests/ path; upstream.md has ## R15 or R15.md says upstream: none.
decided by: sh -c 'echo "eb60a507c147a226ca4a407f375d7a77bea7b8edde809557d4e50df89836f0eb  .beagle/checks/T0131/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0131/check.sh'
budget: 80000 tokens
