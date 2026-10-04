+++
id = "000484-pursuit"
ordinal = 484
kind = "pursuit"
timestamp = "2026-10-04T03:15:34+00:00"
summary = "pursuit open T0122: R14 diagnose"
metric_command = ""
drains = []
hooks = []
+++

criteria: R14.md diagnosed: each failure class has Evidence and an Action naming a file or a Disposition; upstream recorded or 'upstream: none'
decided by: sh -c 'echo "9fbfa60244bfd79635f7fe81227f85ddf0ebbc0e31d9759e64346fc503824ad8  .beagle/checks/T0122/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0122/check.sh'
budget: 80000 tokens
