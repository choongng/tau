+++
id = "000794-pursuit"
ordinal = 794
kind = "pursuit"
timestamp = "2026-10-05T00:24:19+00:00"
summary = "pursuit open T0204: R22 diagnose"
metric_command = ""
drains = []
hooks = []
+++

criteria: R22.md holds a trace analysis of the driver and every worker: failure classes each with Evidence from the trace, tau Actions each with a Prompt-independent line, model classes and upstream (beagle) notes; it says whether the R21 fixes T0200-T0202 fired and how, and names the cause of the OOM kill.
decided by: sh -c 'echo "9b5101bb8d8cea253e7d169d6db33b86b8f3dee174026f778d2a9af6d92acb61  .beagle/checks/T0204/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0204/check.sh'
budget: 60000 tokens
