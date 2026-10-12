+++
id = "002238-pursuit"
ordinal = 2238
kind = "pursuit"
timestamp = "2026-10-12T11:07:17+00:00"
summary = "pursuit open T0424: R58 q35 cobs"
metric_command = ""
drains = []
hooks = []
+++

criteria: R58: q35 cobs run, lean arm (BEAGLE_TAU_LEAN=1), on the R57-R60 freeze 56dda5a9 (T0453-T0462 landed), graded and scorecarded. Note dev-notes/itc-runs/R58.md passes the v8 run-note rules, with Arm: lean, Against B05, Wall, a ## Mechanisms section, Timeline and The questions; every cited [tau] test exists, or the class says Deferred: or Filed as:. (R58 was launched at 03:53, before this open, because T0423 was open with no scope; this check was committed in cb61ad1e, before the launch.)
decided by: sh -c 'echo "b686c087471992ed3f4ac26fc70a2f56ac683bbc397225e5903185588b4e1d4c  .beagle/checks/T0424/T0424.sh" | sha256sum -c --quiet && bash .beagle/checks/T0424/T0424.sh'
budget: 150000 tokens
