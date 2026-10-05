+++
id = "000808-pursuit"
ordinal = 808
kind = "pursuit"
timestamp = "2026-10-05T01:06:22+00:00"
summary = "pursuit open T0207: Driver edit guard sees through NAME=val and wrappers; refusals stop naming the env var; _locked trusts only the manifest"
metric_command = ""
drains = []
hooks = []
+++

criteria: The driver write guard reads a bash -c / sh -c script behind leading NAME=value words, env and the other wrappers; driver refusal texts no longer name the override environment variable; _locked returns only paths in the lock manifest.
decided by: sh -c 'echo "6c1078f35022f34b987fc6a8fb366e9c3b3a14f60459cc13f4c7d33b57475e3f  .beagle/checks/T0207/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0207/check.sh'
budget: 100000 tokens
