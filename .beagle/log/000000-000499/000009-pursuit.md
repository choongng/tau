+++
id = "000009-pursuit"
ordinal = 9
kind = "pursuit"
timestamp = "2026-10-03T09:46:49+00:00"
summary = "pursuit open T0006: harness: launcher, hidden grader, scorecard extractor"
metric_command = ""
drains = []
hooks = []
+++

criteria: A launcher (~/tautest/itc-harness/launch.sh RNN mimo|qwen) moves the old ~/itc aside, runs itc_prompt.txt unchanged under a 1h cap and MemoryMax with the model explicit and git identity via env; a hidden grader scores an ITC through a per-run adapter against a reference implementation (paper examples, normalisation, random op traces, causality of leq) and refuses a broken join; a scorecard extractor reads a tau session + the run repo into the scorecard fields.
decided by: sh -c 'echo "3a28c8d0249cdabe922453391482fb6628dd51634f770ff284cd8d552dcbfac4  .beagle/checks/T0006/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0006/check.sh'
budget: 200000 tokens
