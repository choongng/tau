+++
id = "001409-pursuit"
ordinal = 1409
kind = "pursuit"
timestamp = "2026-10-10T02:16:47+00:00"
summary = "pursuit open T0333: R39 diagnose"
metric_command = ""
drains = []
hooks = []
+++

criteria: dev-notes/itc-runs/R39.md holds a trace analysis of R39 (gemma, cobs, driver thinking medium): a timeline, the questions, and failure classes tagged [tau]/[beagle]/[model]/[harness], each with Evidence, an Action (tau classes name the file/function and regression test names) or Disposition, prompt- and model-independence, and a 'Seen in:' line naming the earlier runs and models it also appeared in (or 'first seen'). It says what R38's fixes (T0328-T0331) did in this run and how driver thinking showed in the trace. Beagle-side problems go in upstream.md under '## R39' or the note says 'upstream: none'.
decided by: sh -c 'echo "87bab758d1afdcfaa059714577bf737ba256a8c03006cae437a2419dcda369a2  .beagle/checks/T0333/T0333.sh" | sha256sum -c --quiet && bash .beagle/checks/T0333/T0333.sh'
budget: 30000 tokens
