+++
id = "001569-pursuit"
ordinal = 1569
kind = "pursuit"
timestamp = "2026-10-10T15:25:22+00:00"
summary = "pursuit open T0358: Baseline comparison"
metric_command = ""
drains = []
hooks = []
+++

criteria: dev-notes/itc-runs/baselines.md: a '## Comparison' table with a row for each of B01-B03 and every pursuit run of the same model and prompt (qwen cobs, mimo itc, gemma cobs), columns grade (as each run's grade.json says), stage reached (progress.py's stages), wall time and how it ended; '## What it implies' on pursuit workflow vs model capability per model, citing the rows; '## Recommendation for R41-R50' saying what to change or keep for the remaining runs, as a recommendation for the owner, not a decision.
decided by: sh -c 'echo "adf2670b532d595059a9cac79594a9a2a0bc39e96d04de44fa60c8337d0e8328  .beagle/checks/T0358/T0358.sh" | sha256sum -c --quiet && bash .beagle/checks/T0358/T0358.sh'
budget: 60000 tokens
