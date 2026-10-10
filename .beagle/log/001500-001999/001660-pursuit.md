+++
id = "001660-pursuit"
ordinal = 1660
kind = "pursuit"
timestamp = "2026-10-10T22:54:25+00:00"
summary = "pursuit open T0388: R44 diagnose"
metric_command = ""
drains = []
hooks = []
+++

criteria: dev-notes/itc-runs/R44.md holds a trace analysis of R44 (mimo, itc, driver and worker thinking medium): a ### Timeline, ### The questions, and failure classes tagged [tau]/[beagle]/[model]/[harness], each with Evidence, an Action (tau classes name the file/function and regression test names) or Disposition, a 'Prompt- and model-independent:' line, and a 'Seen in:' line naming earlier runs and models (or 'first seen'). It says what R43's fixes T0382-T0385 did in this run, and in particular: why T0002's own cases test failed (it imports an unwritten module), why the source hold kept 3-5 of 12 cases, why the three-step limit led to four 'not run' refusals and a plain stop turn, why T0004's check exited 1 on clean data and the open did not catch it, and W5's raw tool-call reply. Beagle-side problems go in upstream.md under '## R44' or the note says 'upstream: none'.
decided by: sh -c 'echo "9ecef1794ad27351218a538941cf9f48f085eb0375247ace544b089fe775b79f  .beagle/checks/T0388/T0388.sh" | sha256sum -c --quiet && bash .beagle/checks/T0388/T0388.sh'
budget: 140000 tokens
