+++
id = "001083-pursuit"
ordinal = 1083
kind = "pursuit"
timestamp = "2026-10-05T12:08:30+00:00"
summary = "pursuit open T0262: R30 run and score"
metric_command = ""
drains = []
hooks = []
+++

criteria: R30 ran qwen on cobs_prompt.txt from a clean ~/cobs under the 1h cap with tau at HEAD; dev-notes/itc-runs/R30.md names model, prompt, tau sha, a grader line and a scorecard.
decided by: sh -c 'echo "3e704a7bd517aeb78b2d43ba493c3acd72157463560faf2f529df0967baa81a0  .beagle/checks/T0262/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0262/check.sh'
budget: 40000 tokens
