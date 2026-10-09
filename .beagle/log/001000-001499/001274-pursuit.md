+++
id = "001274-pursuit"
ordinal = 1274
kind = "pursuit"
timestamp = "2026-10-09T20:58:50+00:00"
summary = "pursuit open T0307: R36 diagnose"
metric_command = ""
drains = []
hooks = []
+++

criteria: dev-notes/itc-runs/R36.md holds a trace analysis of R36 (gemma4-12b-q4, itc, driver thinking medium): a timeline, the questions, and failure classes tagged [tau]/[beagle]/[model]/[harness], each with Evidence, an Action (tau classes name the file/function and regression test names) or Disposition, prompt- and model-independence, and a 'Seen in:' line naming the earlier runs and models it also appeared in (or 'first seen'). It says what R35's fixes (T0290-T0294) did in this run and how driver thinking showed in the trace. Beagle-side problems go in upstream.md under '## R36' or the note says 'upstream: none'.
decided by: sh -c 'echo "d8e811a70f2225e2885d40cc367f7398c49efa831ef27f66bf3d0c0b588b67b6  .beagle/checks/T0307/T0307.sh" | sha256sum -c --quiet && bash .beagle/checks/T0307/T0307.sh'
budget: 120000 tokens
