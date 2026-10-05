+++
id = "001102-pursuit"
ordinal = 1102
kind = "pursuit"
timestamp = "2026-10-05T13:37:08+00:00"
summary = "pursuit open T0266: R31 run and score"
metric_command = ""
drains = []
hooks = []
+++

criteria: R31 ran mimo on cobs_prompt.txt from a clean ~/cobs under the 1h cap with tau at HEAD; dev-notes/itc-runs/R31.md names model, prompt, tau sha, a grader line and a scorecard.
decided by: sh -c 'echo "bd5f2bf0192f2c226d54690f51e0489a761c97cc4b489981f1ca6d2edf14c522  .beagle/checks/T0266/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0266/check.sh'
budget: 40000 tokens
