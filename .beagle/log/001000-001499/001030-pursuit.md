+++
id = "001030-pursuit"
ordinal = 1030
kind = "pursuit"
timestamp = "2026-10-05T09:57:48+00:00"
summary = "pursuit open T0251: R28 run and score"
metric_command = ""
drains = []
hooks = []
+++

criteria: R28 ran qwen on itc_prompt.txt from a clean ~/itc under the 1h cap with tau at HEAD; dev-notes/itc-runs/R28.md names model, prompt, tau sha, a grader line and a scorecard.
decided by: sh -c 'echo "7b925ac71100b4eed52e03dc3f8f705d0870ebe16c3c7aa0b73bea66e6c40f6f  .beagle/checks/T0251/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0251/check.sh'
budget: 40000 tokens
