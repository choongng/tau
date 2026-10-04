+++
id = "000759-pursuit"
ordinal = 759
kind = "pursuit"
timestamp = "2026-10-04T17:05:16+00:00"
summary = "pursuit open T0102: summary across R11-R20"
metric_command = ""
drains = []
hooks = []
+++

criteria: dev-notes/itc-runs/summary-R11-R20.md summarises R11-R20: a row per run with its grade as recorded in that run's notes, the recurring failure classes, what changed in tau, what is still open, and a comparison with R01-R10; summary.md points to it.
decided by: sh -c 'echo "e323864559912e8b84511e587a38b1f66e1c9a66e91d418377286b8d0038e245  .beagle/checks/T0102/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0102/check.sh'
budget: 60000 tokens
