+++
id = "001128-pursuit"
ordinal = 1128
kind = "pursuit"
timestamp = "2026-10-05T14:31:40+00:00"
summary = "pursuit open T0271: R32 run and score"
metric_command = ""
drains = []
hooks = []
+++

criteria: R32 ran qwen on itc_prompt.txt from a clean ~/itc under the 1h cap with tau at HEAD; dev-notes/itc-runs/R32.md names model, prompt, tau sha, a grader line and a scorecard.
decided by: sh -c 'echo "48f35e24c7fd304232eb82d560ab855e9b2b144502de73b88b5362fb946ff76d  .beagle/checks/T0271/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0271/check.sh'
budget: 40000 tokens
