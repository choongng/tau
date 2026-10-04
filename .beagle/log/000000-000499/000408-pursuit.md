+++
id = "000408-pursuit"
ordinal = 408
kind = "pursuit"
timestamp = "2026-10-04T00:44:30+00:00"
summary = "pursuit spawn T0106: another route to T0104"
metric_command = ""
drains = []
hooks = []
+++

superseded: [T0104] R11 diagnose
because: the second [tau] class had a Disposition and no Action naming a file, which diagnosed.sh rightly refuses
delta: merge the repeat-breaker observation into the first [tau] class's Evidence instead of keeping it as a separate [tau] class with only a Disposition
