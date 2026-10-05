+++
id = "001148-pursuit"
ordinal = 1148
kind = "pursuit"
timestamp = "2026-10-05T16:05:29+00:00"
summary = "pursuit open T0274: A rerun after a stays-open close carries the reason; known-answers brief names the right check file and the cases test's close requirement"
metric_command = ""
drains = []
hooks = []
+++

criteria: After a done close that stays open, the reason is kept on the task and the next worker's brief states it (beside _last_failure_note); the not-workable answer names the call with notes; _known_answers_note names the check's test file when the check names one that is not yet on disk (never falls back to another .py in scope), and the brief says the cases test must load the data file and run every case.
decided by: sh -c 'echo "655b5da655bebfca944ce58b9023800585ac6c3e4ed773261108fa4b79d9ca04  .beagle/checks/T0274/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0274/check.sh'
budget: 70000 tokens
