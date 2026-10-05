+++
id = "000945-pursuit"
ordinal = 945
kind = "pursuit"
timestamp = "2026-10-05T07:19:50+00:00"
summary = "pursuit open T0235: R26 diagnose"
metric_command = ""
drains = []
hooks = []
+++

criteria: R26.md holds a trace analysis of the driver and the workers: failure classes each with Evidence from the trace, tau Actions each with a Prompt-independent line, model classes and upstream notes; it says whether the R25 fixes T0229-T0233 fired and how, why no task closed, what the 22 guard refusals and 7 compactions were, and whether one structural cause runs through R23-R26 (four zero-done runs).
decided by: sh -c 'echo "0628001a8ddf32bf7f074613132b0b0c43812ac44f17c2da3a2feed15b9caf48  .beagle/checks/T0235/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0235/check.sh'
budget: 70000 tokens
