+++
id = "001583-pursuit"
ordinal = 1583
kind = "pursuit"
timestamp = "2026-10-10T16:51:19+00:00"
summary = "pursuit open T0367: R41 diagnose"
metric_command = ""
drains = []
hooks = []
+++

criteria: dev-notes/itc-runs/R41.md holds a trace analysis of R41 (mimo, cobs, driver and worker thinking medium): a timeline, the questions, and failure classes tagged [tau]/[beagle]/[model]/[harness], each with Evidence, an Action (tau classes name the file/function and regression test names) or Disposition, prompt- and model-independence, and a 'Seen in:' line naming earlier runs and models (or 'first seen'). It says what R40's fixes (T0347-T0351, T0359, T0360) and the assists T0362-T0365 did in this run, in particular why 7 of 9 workers hit the wall timeout with empty reports and whether worker thinking caused it, and why known-answers never closed in the hour. Beagle-side problems go in upstream.md under '## R41' or the note says 'upstream: none'.
decided by: sh -c 'echo "196c6c4c47cd04c4d0cc78f6806f0607fad43ec664169524816ba54b0d48c760  .beagle/checks/T0367/T0367.sh" | sha256sum -c --quiet && bash .beagle/checks/T0367/T0367.sh'
budget: 100000 tokens
