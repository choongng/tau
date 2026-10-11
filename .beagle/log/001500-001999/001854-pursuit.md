+++
id = "001854-pursuit"
ordinal = 1854
kind = "pursuit"
timestamp = "2026-10-11T23:21:29+00:00"
summary = "pursuit open T0417: R51 q35 itc"
metric_command = ""
drains = []
hooks = []
+++

criteria: R51 (q35 qwen3.6-35b-q6-mtp-thinking-coding on krang, itc_prompt.txt, driver and worker thinking medium) ran from a clean ~/itc under the one-hour cap with tau's T0437-T0442 fixes in; dev-notes/itc-runs/R51.md holds the scorecard, the hidden-grader result, a 'Wall:' line (wall time, driver and worker output tokens, tasks spawned per task done), an 'Against B04:' comparison with the q35 baseline, and a trace analysis (timeline, questions, failure classes tagged [tau]/[beagle]/[model]/[harness] with Evidence, Action or Disposition, independence and Seen in) that says what each of T0437-T0442 did in this run.
decided by: sh -c 'echo "f1220ff34feb578b3e296dfd26cef325eb498e14439108efb97ab7f4c1e1950a  .beagle/checks/T0417/T0417.sh" | sha256sum -c --quiet && bash .beagle/checks/T0417/T0417.sh'
budget: 300000 tokens
