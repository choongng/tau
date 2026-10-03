+++
id = "000148-pursuit"
ordinal = 148
kind = "pursuit"
timestamp = "2026-10-03T16:21:44+00:00"
summary = "pursuit open T0050: Audit: R04.md scorecard regenerated, and scored.sh compares the md with the json"
metric_command = ""
drains = []
hooks = []
+++

criteria: R04.md's Scorecard block is regenerated from R04's session and the run's repo (~/itc.r04) and agrees with runs/R04/scorecard.json on tasks_total, tasks_done, commits, founded and uncommitted_files; R05 and R06 still agree; runs/scored.sh (the template later run tasks copy) makes the same comparison.
decided by: sh -c 'echo "08ba37919e13580ce025aca960602b8ec7a48e1becd0ba714791efb43e28a4f9  .beagle/checks/T0050/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0050/check.sh'
budget: 15000 tokens
