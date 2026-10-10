+++
id = "001628-pursuit"
ordinal = 1628
kind = "pursuit"
timestamp = "2026-10-10T20:12:37+00:00"
summary = "pursuit open T0381: R43 diagnose"
metric_command = ""
drains = []
hooks = []
+++

criteria: dev-notes/itc-runs/R43.md holds a trace analysis of R43 (qwen, cobs, driver and worker thinking medium): a timeline, the questions, and failure classes tagged [tau]/[beagle]/[model]/[harness], each with Evidence, an Action (tau classes name the file/function and regression test names) or Disposition, prompt- and model-independence, and a 'Seen in:' line naming earlier runs and models (or 'first seen'). It says what R42's fixes T0375-T0378 and T0372 did in this run, in particular: why the thinking-off retry W13 was still killed (text cut-offs at 8192), why T0003 sat behind 9 'not opened' refusals and 13 refused driver writes from t=36.4, why its check selected no tests, why known answers took 36 min and 8 workers, and why the graded code stayed uncommitted. Beagle-side problems go in upstream.md under '## R43' or the note says 'upstream: none'.
decided by: sh -c 'echo "f532aac342fa64e6fc0f879c0090b3c8444ff10395816c9c45862febb3d30910  .beagle/checks/T0381/T0381.sh" | sha256sum -c --quiet && bash .beagle/checks/T0381/T0381.sh'
budget: 140000 tokens
