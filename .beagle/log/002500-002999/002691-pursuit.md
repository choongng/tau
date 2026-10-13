+++
id = "002691-pursuit"
ordinal = 2691
kind = "pursuit"
timestamp = "2026-10-13T08:15:35+00:00"
summary = "pursuit open T0526: Compare two extractions of one reference by its lines, not its name"
metric_command = ""
drains = []
hooks = []
+++

criteria: Span overlap treats a path source and a command source with the same text as one document (experiments still by command); R90's two extractions diff with nothing only in the second
decided by: sh -c 'echo "9e100dd5258ff15fb85814eecb8f1ae49c861f44479fab470a61143808b85477  .beagle/checks/T0526/T0526.sh" | sha256sum -c --quiet && bash .beagle/checks/T0526/T0526.sh'
budget: 60000 tokens
opened over T0493, T0517: 65954d169c0981e38f1fbba070223d3a6eb31e98
