+++
id = "002813-pursuit"
ordinal = 2813
kind = "pursuit"
timestamp = "2026-10-13T21:37:28+00:00"
summary = "pursuit open T0549: recon: how sealing can show each entry's test fails once the code loads, in any language (R97)"
metric_command = ""
drains = []
hooks = []
+++

criteria: dev-notes/contract-first/discriminate-recon.md says what R97 sealed (accept.sh lines that print ok unconditionally, examples checked only for not raising), what seal and the contract check test today (codeless_run, codeless_outliers, failure_reasons, with file:line), at least three language-neutral options for showing each entry's test can fail once code loads with their cost and what each would have caught on R96 and R97, and one recommendation; sections '## What R97 sealed', '## What sealing checks now', '## Options', '## Recommendation'
decided by: sh -c 'echo "c29d6f4ba5c6ad6c92d0cfa9b18cc93f90840a3f2e0a9142c0168b577954519e  .beagle/checks/T0549/T0549.sh" | sha256sum -c --quiet && bash .beagle/checks/T0549/T0549.sh'
budget: 80000 tokens
