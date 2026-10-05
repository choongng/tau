+++
id = "000868-pursuit"
ordinal = 868
kind = "pursuit"
timestamp = "2026-10-05T03:45:28+00:00"
summary = "pursuit open T0220: R24 diagnose"
metric_command = ""
drains = []
hooks = []
+++

criteria: R24.md holds a trace analysis of the driver and the workers: failure classes each with Evidence from the trace, tau Actions each with a Prompt-independent line, model classes and upstream notes; it says whether the R23 fixes T0215-T0218 fired and how, why 11 steps stayed open with 17 workers capped and none committed, and why the implementation landed under tests/.
decided by: sh -c 'echo "d739c328750fa0ea6d01cb32c0f355cb69f7b244d531d46cb75b6e06a93676a8  .beagle/checks/T0220/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0220/check.sh'
budget: 70000 tokens
