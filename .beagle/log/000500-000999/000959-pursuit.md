+++
id = "000959-pursuit"
ordinal = 959
kind = "pursuit"
timestamp = "2026-10-05T07:32:59+00:00"
summary = "pursuit open T0237: A passing, proven known-answers task closes done"
metric_command = ""
drains = []
hooks = []
+++

criteria: An open task whose scope holds only data files and tests, whose check passes and whose proof is witnessed by the data file's absence closes done through pursuit_step; the misplaced-implementation close gate counts only files the bound check runs or that they import, so a def in a test the check never runs holds no close.
decided by: sh -c 'echo "e2d60758beecb3e176a05f415e1d8af48e894f9418db7e2ea10728ac59a90d19  .beagle/checks/T0237/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0237/check.sh'
budget: 80000 tokens
