+++
id = "001177-pursuit"
ordinal = 1177
kind = "pursuit"
timestamp = "2026-10-05T17:48:34+00:00"
summary = "pursuit open T0281: R34 run and score"
metric_command = ""
drains = []
hooks = []
+++

criteria: R34 ran qwen on cobs_prompt.txt from a clean ~/cobs under the 1h cap with tau at HEAD; dev-notes/itc-runs/R34.md names model, prompt, tau sha, a grader line and a scorecard.
decided by: sh -c 'echo "a1e83ccf609ca56fd439992457cb1801f182f1e7abb97b64d30646039b15458d  .beagle/checks/T0281/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0281/check.sh'
budget: 40000 tokens
