+++
id = "001474-pursuit"
ordinal = 1474
kind = "pursuit"
timestamp = "2026-10-10T03:33:48+00:00"
summary = "pursuit open T0346: R40 diagnose"
metric_command = ""
drains = []
hooks = []
+++

criteria: dev-notes/itc-runs/R40.md holds a trace analysis of R40 (qwen, itc, driver thinking medium): a timeline, the questions, and failure classes tagged [tau]/[beagle]/[model]/[harness], each with Evidence, an Action (tau classes name the file/function and regression test names) or Disposition, prompt- and model-independence, and a 'Seen in:' line naming the earlier runs and models it also appeared in (or 'first seen'). It says what R39's fixes (T0338-T0344) did in this run and how driver thinking showed in the trace. Beagle-side problems go in upstream.md under '## R40' or the note says 'upstream: none'.
decided by: sh -c 'echo "3eb73ff0510e5b8c5a3e8ebe06127756e751d1c971111b29d87126d1989f858e  .beagle/checks/T0346/T0346.sh" | sha256sum -c --quiet && bash .beagle/checks/T0346/T0346.sh'
budget: 100000 tokens
