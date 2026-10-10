+++
id = "001492-pursuit"
ordinal = 1492
kind = "pursuit"
timestamp = "2026-10-10T04:05:59+00:00"
summary = "pursuit open T0353: Stage tracking in progress.py"
metric_command = ""
drains = []
hooks = []
+++

criteria: progress.py prints, besides the per-cell grade table, the furthest stage each run R21 onward reached (none, founded, known-answers, implementation, any-pass, complete) in a per-run line starting with the run id, and the best stage per model/prompt cell. Founded comes from the scorecard; known-answers closed from a done known-answers task in the run's repo .beagle/tree (repo: the next same-task run's moved_previous_to, else meta cwd); implementation from a graded case not Missing. Baseline runs (B01...) are listed separately without pursuit stages.
decided by: sh -c 'echo "d488d5c0099c1153594ca9c593fe843f06ebc9c533e563cf31573b139c20dad2  .beagle/checks/T0353/T0353.sh" | sha256sum -c --quiet && bash .beagle/checks/T0353/T0353.sh'
budget: 60000 tokens
opened over T0349, T0350, T0351, T0360: T0353 runs beside T0359 on a disjoint scope (the harness repo)
