+++
id = "002381-pursuit"
ordinal = 2381
kind = "pursuit"
timestamp = "2026-10-12T14:19:25+00:00"
summary = "pursuit open T0466: An amended check that passes on disk briefs the witness note, not the old check's close demand (R57)"
metric_command = ""
drains = []
hooks = []
+++

criteria: An amended check that passes on disk sets passed_on_disk and clears the old close demand, so the worker is briefed with the witness note, not the old check's demand (R57). Named test test_amended_check_passing_on_disk_briefs_witness_note_not_old_demand passes; suite and ruff pass.
decided by: sh -c 'echo "01deccfed4f7f7fdf105ba23ad0d3290903958edc6ffe73db9e9ab8e54241cb9  .beagle/checks/T0466/T0466.sh" | sha256sum -c --quiet && bash .beagle/checks/T0466/T0466.sh'
budget: 150000 tokens
