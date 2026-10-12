+++
id = "002201-pursuit"
ordinal = 2201
kind = "pursuit"
timestamp = "2026-10-12T09:50:52+00:00"
summary = "pursuit open T0423: R57 q35 itc"
metric_command = ""
drains = []
hooks = []
+++

criteria: R57: q35 itc run, lean arm (BEAGLE_TAU_LEAN=1), on the R57-R60 freeze (frozen-sha.txt, 56dda5a9, with T0453-T0462 landed), graded and scorecarded. Note dev-notes/itc-runs/R57.md has Arm: lean, Against B04, Wall, a ## Mechanisms section (>=3 Mnn lines), the v8 failure-class sections, Timeline and The questions. Every [tau] class's cited test exists, or the class says Deferred: or Filed as:. Its pair, R59 (full), comes after it.
decided by: sh -c 'echo "f57e98e96349c67c3a950f3f0e718337ca1b7cc8f646fa8ee6b6d6c0b82fce6c  .beagle/checks/T0423/T0423.sh" | sha256sum -c --quiet && bash .beagle/checks/T0423/T0423.sh'
budget: 150000 tokens
