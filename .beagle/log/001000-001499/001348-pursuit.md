+++
id = "001348-pursuit"
ordinal = 1348
kind = "pursuit"
timestamp = "2026-10-09T22:56:50+00:00"
summary = "pursuit open T0321: R37 diagnose"
metric_command = ""
drains = []
hooks = []
+++

criteria: dev-notes/itc-runs/R37.md holds a trace analysis of R37 (qwen, cobs, driver thinking medium): a timeline, the questions, and failure classes tagged [tau]/[beagle]/[model]/[harness], each with Evidence, an Action (tau classes name the file/function and regression test names) or Disposition, prompt- and model-independence, and a 'Seen in:' line naming the earlier runs and models it also appeared in (or 'first seen'). It says what R36's fixes (T0308-T0318) did in this run and how driver thinking showed in the trace. Beagle-side problems go in upstream.md under '## R37' or the note says 'upstream: none'.
decided by: sh -c 'echo "b470cb633d6665b3edc99da5f6b1a74dc8173a3721985ad3c7c66326879f66b8  .beagle/checks/T0321/T0321.sh" | sha256sum -c --quiet && bash .beagle/checks/T0321/T0321.sh'
budget: 40000 tokens
