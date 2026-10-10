+++
id = "001382-pursuit"
ordinal = 1382
kind = "pursuit"
timestamp = "2026-10-10T00:34:48+00:00"
summary = "pursuit open T0328: Found-first gate refuses agent before founding"
metric_command = ""
drains = []
hooks = []
+++

criteria: R38 class 1: the driver's pre-founding agent call ran outside the pursuit with no scope, check or time limit and held 57 of 60 minutes. make_found_first_gate refuses agent while the goal is missing, whatever the setup-call count.
decided by: sh -c 'echo "a814862d385a32c6fb6f671070f83c098c138cf8dc52164241808fc6a7730163  .beagle/checks/T0328/T0328.sh" | sha256sum -c --quiet && bash .beagle/checks/T0328/T0328.sh'
budget: 60000 tokens
