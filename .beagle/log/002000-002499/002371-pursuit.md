+++
id = "002371-pursuit"
ordinal = 2371
kind = "pursuit"
timestamp = "2026-10-12T14:12:55+00:00"
summary = "pursuit open T0464: The cut-off kill note says 'without acting' only when the worker made no calls; a killed attempt is not said to have reported in any wording (R56)"
metric_command = ""
drains = []
hooks = []
+++

criteria: The cut-off kill note says 'without acting' only when the worker made no calls, and a killed attempt is said to have ended without a report, not to have reported (R56). Named test test_cut_off_kill_note_omits_without_acting_when_the_worker_made_calls passes (plus test_killed_attempt_context_says_the_attempt_before_ended_without_a_report in the suite); suite and ruff pass.
decided by: sh -c 'echo "06a8fa96767ffc996b3cdca1d1406437e92202d32a7c3769f977f186f5e7e1ef  .beagle/checks/T0464/T0464.sh" | sha256sum -c --quiet && bash .beagle/checks/T0464/T0464.sh'
budget: 150000 tokens
