+++
id = "001141-pursuit"
ordinal = 1141
kind = "pursuit"
timestamp = "2026-10-05T15:53:21+00:00"
summary = "pursuit open T0275: Breaker quotes the sentence of a refusal that holds its call"
metric_command = ""
drains = []
hooks = []
+++

criteria: When the repeated refusal's head is cut before a call to one of the session's tools, _repeated_call quotes instead the result's sentence that names that call (bounded), so the breaker never shows text cut mid-call; a refusal whose head already holds the call is quoted as before.
decided by: sh -c 'echo "8029c80afeee665050867bee0474a6d1bb123b124018ebb6c9dc9a2968f181da  .beagle/checks/T0275/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0275/check.sh'
budget: 30000 tokens
