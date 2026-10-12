+++
id = "002044-pursuit"
ordinal = 2044
kind = "pursuit"
timestamp = "2026-10-12T07:02:03+00:00"
summary = "pursuit open T0421: R55 q35 itc"
metric_command = ""
drains = []
hooks = []
+++

criteria: R55: q35 itc run, lean arm (BEAGLE_TAU_LEAN=1), on frozen tau code (3d07bc9f), graded and scorecarded; note dev-notes/itc-runs/R55.md has Arm: lean, Against R53, Against B04, Wall, a ## Mechanisms section (>=3 Mnn lines), the v8 failure-class sections, Timeline and The questions, and says what T0447 did. (R55 was launched before this open, because T0420 had no --scope; the check dd9071a2 predates the launch.)
decided by: sh -c 'echo "d6fe54a9240b2b320774b49fdcf3a70e0494ee64d55a60b750ecf3bd8d2cbbda  .beagle/checks/T0421/T0421.sh" | sha256sum -c --quiet && bash .beagle/checks/T0421/T0421.sh'
budget: 150000 tokens
