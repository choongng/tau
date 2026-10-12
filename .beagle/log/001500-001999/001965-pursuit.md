+++
id = "001965-pursuit"
ordinal = 1965
kind = "pursuit"
timestamp = "2026-10-12T05:55:29+00:00"
summary = "pursuit open T0420: R54 q35 cobs"
metric_command = ""
drains = []
hooks = []
+++

criteria: R54: q35 cobs run, full arm, on frozen tau code (3d07bc9f), graded and scorecarded; note dev-notes/itc-runs/R54.md has Arm: full, Against B05, Wall, a ## Mechanisms section (>=3 Mnn lines), the v8 failure-class sections, Timeline and The questions, and says what T0445 T0446 T0448 T0452 did. (R54 was launched at 22:50, before this open, because T0419 had no --scope and an open is refused while another unscoped task is open; this check, dd9071a2, predates the launch.)
decided by: sh -c 'echo "cc196144c5006da97c6be6cda98915c1ca22cd50170e903a806e9cd0550b9301  .beagle/checks/T0420/T0420.sh" | sha256sum -c --quiet && bash .beagle/checks/T0420/T0420.sh'
budget: 150000 tokens
