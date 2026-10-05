+++
id = "000909-pursuit"
ordinal = 909
kind = "pursuit"
timestamp = "2026-10-05T05:55:10+00:00"
summary = "pursuit open T0228: R25 diagnose"
metric_command = ""
drains = []
hooks = []
+++

criteria: R25.md holds a trace analysis of the driver and the workers: failure classes each with Evidence from the trace, tau Actions each with a Prompt-independent line, model classes and upstream notes; it says whether the R24 fixes T0221-T0226 fired and how, why no task closed in 52 minutes across 13 workers, and compares with R23/R24, the other zero-done runs.
decided by: sh -c 'echo "346f1507d981a265eab3beb9e688bdb44f11d579269309db78df437080794a5e  .beagle/checks/T0228/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0228/check.sh'
budget: 70000 tokens
