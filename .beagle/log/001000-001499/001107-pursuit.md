+++
id = "001107-pursuit"
ordinal = 1107
kind = "pursuit"
timestamp = "2026-10-05T14:12:44+00:00"
summary = "pursuit prove T0267: WITNESSED — refuses when R31.md's `## Trace analysis` is put back as `## Trace notes`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "8eb8512779a5c09020ccdd75cb17593a0ca64faea9faddba5fe846e713436f3e  .beagle/checks/T0267/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0267/check.sh'
refutes: refuses when R31.md's `## Trace analysis` is put back as `## Trace notes` (proven 2026-10-05T14:11:47+00:00)
refused after 0s of a 0s check
