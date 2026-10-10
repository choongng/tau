+++
id = "001679-pursuit"
ordinal = 1679
kind = "pursuit"
timestamp = "2026-10-10T23:38:10+00:00"
summary = "pursuit open T0391: R44 fix: the step cap keeps a passing check, and the stop gate accepts the stop it offered"
metric_command = ""
drains = []
hooks = []
+++

criteria: Once a later run of a step's bound check passes, the earlier failed-check record is cleared, so the routes keyed on a passing check (e.g. the notes-only source rerun) are offered. The three-step cap does not ask for a new done_when when the bound check passes; it keeps that check. When the driver takes a stop the last step result offered, the stop gate accepts it instead of refusing. Structural, no domain words. Tests test_source_judge_escalation_after_an_early_failed_check, test_step_cap_keeps_a_passing_bound_check, test_stop_gate_accepts_a_stop_the_step_cap_offered; whole file passes, ruff clean.
decided by: sh -c 'echo "175fcf109ca4e9fbddddac9ae6bbb9a869c75b26d94229702a082e31a280b017  .beagle/checks/T0391/T0391.sh" | sha256sum -c --quiet && bash .beagle/checks/T0391/T0391.sh'
budget: 120000 tokens
