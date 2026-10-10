+++
id = "001420-pursuit"
ordinal = 1420
kind = "pursuit"
timestamp = "2026-10-10T02:20:37+00:00"
summary = "pursuit open T0336: Audit 12: T0331's tau-subagents twin test runs instead of skipping"
metric_command = ""
drains = []
hooks = []
+++

criteria: tau-subagents' two runtime_provider_config tests (the child holds the config; the child builds the thinking-off twin) run and pass against the choong-dev tau, in a check that refuses a skip; R38.md says where that coverage runs and that T0331's diagnostics.py edit fell outside its scope.
decided by: sh -c 'echo "1f496e64c7f0ef3712f1b79366ec31c0d4d71f1b62db01f324cfdc2c94ed3461  .beagle/checks/T0336/T0336.sh" | sha256sum -c --quiet && bash .beagle/checks/T0336/T0336.sh'
budget: 8000 tokens
