+++
id = "003120-pursuit"
ordinal = 3120
kind = "pursuit"
timestamp = "2026-10-14T20:38:16+00:00"
summary = "pursuit prove T0600: WITNESSED — refuses when beagle.py's `changed = list(dict.fromkeys([*changed, *commit…` is put back as `changed = list(dict.fromkeys([*changed, *carrie…`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "703ad4835298af00caab69e25cd28ae73788285fd146d18d75e7aca193e71d66  .beagle/checks/T0600/T0600.sh" | sha256sum -c --quiet && bash .beagle/checks/T0600/T0600.sh'
refutes: refuses when beagle.py's `changed = list(dict.fromkeys([*changed, *commit…` is put back as `changed = list(dict.fromkeys([*changed, *carrie…` (proven 2026-10-14T20:38:15+00:00)
refused after 25s of a 3m01s check
