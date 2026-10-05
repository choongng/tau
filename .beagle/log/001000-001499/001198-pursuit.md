+++
id = "001198-pursuit"
ordinal = 1198
kind = "pursuit"
timestamp = "2026-10-05T19:25:36+00:00"
summary = "pursuit open T0285: R34 fix: worker bash timeout and no-write guard over paging and runs"
metric_command = ""
drains = []
hooks = []
+++

criteria: A worker's bash calls default to a short timeout that beagle sets (tau core gains a per-session override of DEFAULT_BASH_TIMEOUT_SECONDS, e.g. an env var, with the 600 s default unchanged otherwise); the worker no-write guard also counts repeated reads of in-scope files past what a file needs once, and bash runs that change no file, so a worker that has written nothing is steered to write before its cap. Regression tests for each.
decided by: sh -c 'echo "5e4aaf375ad8d3a87253ceb820fb5d89e2f724a808b5f5174b6dd3da7c4b5992  .beagle/checks/T0285/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0285/check.sh'
budget: 150000 tokens
