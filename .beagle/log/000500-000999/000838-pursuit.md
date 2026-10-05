+++
id = "000838-pursuit"
ordinal = 838
kind = "pursuit"
timestamp = "2026-10-05T02:05:40+00:00"
summary = "pursuit open T0214: R23 diagnose"
metric_command = ""
drains = []
hooks = []
+++

criteria: R23.md holds a trace analysis of the driver and both workers: failure classes each with Evidence from the trace, tau Actions each with a Prompt-independent line, model classes and upstream notes; it says whether the R22 fixes T0205-T0210/T0212 fired and how, and names what the 8 refusals in a row were.
decided by: sh -c 'echo "0b000b29b5f271d66e32a74866d5db25d9fe0008ff57ed28a25373d1151f1133  .beagle/checks/T0214/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0214/check.sh'
budget: 70000 tokens
