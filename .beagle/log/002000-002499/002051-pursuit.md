+++
id = "002051-pursuit"
ordinal = 2051
kind = "pursuit"
timestamp = "2026-10-12T08:02:39+00:00"
summary = "pursuit open T0422: R56 q35 cobs"
metric_command = ""
drains = []
hooks = []
+++

criteria: R56: q35 cobs run, lean arm (BEAGLE_TAU_LEAN=1), on frozen tau code (3d07bc9f), graded and scorecarded; note dev-notes/itc-runs/R56.md has Arm: lean, Against R54, Against B05, Wall, a ## Mechanisms section (>=3 Mnn lines), the v8 failure-class sections, Timeline and The questions. (R56 was launched at 00:55, before this open, because T0421 was still open with no scope; the check dd9071a2 predates the launch.)
decided by: sh -c 'echo "cafe34b56d16d2ea10256e77d7afb467d9d7704e7b6bdfcc90f9f5eeb5464bdb  .beagle/checks/T0422/T0422.sh" | sha256sum -c --quiet && bash .beagle/checks/T0422/T0422.sh'
budget: 150000 tokens
