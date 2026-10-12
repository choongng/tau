+++
id = "002376-pursuit"
ordinal = 2376
kind = "pursuit"
timestamp = "2026-10-12T14:16:10+00:00"
summary = "pursuit open T0465: Under lean, the ruff-over-root refusal names no locked tests (R57)"
metric_command = ""
drains = []
hooks = []
+++

criteria: Under BEAGLE_TAU_LEAN the worker ruff-over-root refusal names no locked tests; lean-off text unchanged (R57). Named test test_ruff_over_root_refusal_names_no_locked_tests_when_none_are_locked passes; suite and ruff pass.
decided by: sh -c 'echo "9228d8667209dc7df234a917c6eb1eb7ed3274a15d9bd1d9f0d54a82b330b21e  .beagle/checks/T0465/T0465.sh" | sha256sum -c --quiet && bash .beagle/checks/T0465/T0465.sh'
budget: 150000 tokens
