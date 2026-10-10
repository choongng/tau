+++
id = "001601-pursuit"
ordinal = 1601
kind = "pursuit"
timestamp = "2026-10-10T18:30:52+00:00"
summary = "pursuit open T0374: R42 diagnose"
metric_command = ""
drains = []
hooks = []
+++

criteria: dev-notes/itc-runs/R42.md holds a trace analysis of R42 (gemma, itc, driver and worker thinking medium): a timeline, the questions, and failure classes tagged [tau]/[beagle]/[model]/[harness], each with Evidence, an Action (tau classes name the file/function and regression test names) or Disposition, prompt- and model-independence, and a 'Seen in:' line naming earlier runs and models (or 'first seen'). It says what R41's fixes T0370-T0372 did in this run (in particular whether the thinking-off retry W2 helped, and why it was stopped by refusals after 20 s), why the driver kept calling pursuit_step on T0007 from t=48.8 with every call refused, its 10 length stops, and why no implementation was written in the hour. Beagle-side problems go in upstream.md under '## R42' or the note says 'upstream: none'.
decided by: sh -c 'echo "1c819ecc83ff9086e59611cd7b3f6af41dc10aa1b42f88e07be849a8a95eb0c4  .beagle/checks/T0374/T0374.sh" | sha256sum -c --quiet && bash .beagle/checks/T0374/T0374.sh'
budget: 140000 tokens
