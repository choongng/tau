+++
id = "001377-pursuit"
ordinal = 1377
kind = "pursuit"
timestamp = "2026-10-10T00:31:14+00:00"
summary = "pursuit open T0326: R38 diagnose"
metric_command = ""
drains = []
hooks = []
+++

criteria: dev-notes/itc-runs/R38.md holds a trace analysis of R38 (mimo, itc, driver thinking medium): a timeline, the questions, and failure classes tagged [tau]/[beagle]/[model]/[harness], each with Evidence, an Action (tau classes name the file/function and regression test names) or Disposition, prompt- and model-independence, and a 'Seen in:' line naming the earlier runs and models it also appeared in (or 'first seen'). It says what R37's fixes (T0322-T0324) did in this run and how driver thinking showed in the trace. Beagle-side problems go in upstream.md under '## R38' or the note says 'upstream: none'.
decided by: sh -c 'echo "b815618e0ecbedd342e419f1ae813b79a362ee4be48ede9a10336c8756d393b0  .beagle/checks/T0326/T0326.sh" | sha256sum -c --quiet && bash .beagle/checks/T0326/T0326.sh'
budget: 30000 tokens
