+++
id = "001925-pursuit"
ordinal = 1925
kind = "pursuit"
timestamp = "2026-10-12T04:24:15+00:00"
summary = "pursuit open T0449: Own-copy refusal names only the functions computed on a case input, never a data loader"
metric_command = ""
drains = []
hooks = []
+++

criteria: The own-copy refusal of a cases test names only the functions the test gives a case's input (the computed ones), never a loader such as _load_cases; a named test shows a test with _load_cases and fork gets a message naming fork and not _load_cases; full suite and ruff pass.
decided by: sh -c 'echo "52859f9c2eff7ec8a70ac814dc32b4b109e8d14b2f5a0e6abbb96e58ae155c10  .beagle/checks/T0449/T0449.sh" | sha256sum -c --quiet && bash .beagle/checks/T0449/T0449.sh'
budget: 150000 tokens
opened over T0419: R0002
