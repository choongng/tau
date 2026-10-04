+++
id = "000507-pursuit"
ordinal = 507
kind = "pursuit"
timestamp = "2026-10-04T04:08:26+00:00"
summary = "pursuit open T0115: cases.json sources must quote references/ (R12 class 2c)"
metric_command = ""
drains = []
hooks = []
+++

criteria: Where the goal names references/, the known-answers guidance asks that each case's source quote a line of references/*.txt verbatim. At a done close of a task whose scope writes the locked cases file, tau counts the cases with no source text of at least 4 words found (whitespace-normalised) in references/*.txt, and keeps the task open, naming up to 3 such cases, when more than half have none. A bare file:line or URL source counts as not found. A cases file whose cases mostly quote references/ closes as before.
decided by: sh -c 'echo "0dfc8d7bd5efdc4c1293479402008663e8f852740b8b16dbce04ac8ba880e48f  .beagle/checks/T0115/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0115/check.sh'
budget: 100000 tokens
