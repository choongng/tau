+++
id = "002121-pursuit"
ordinal = 2121
kind = "pursuit"
timestamp = "2026-10-12T09:08:04+00:00"
summary = "pursuit open T0454: Retry note never says a killed worker 'reported back' (R53)"
metric_command = ""
drains = []
hooks = []
+++

criteria: The retry note says an attempt 'reported back' only when it did; a killed attempt is not said to have reported (R53). Named test test_retry_note_after_killed_attempt_does_not_say_reported_back passes; suite and ruff pass.
decided by: sh -c 'echo "2b8db83651158cb5b7617ab4d4aa843da8881607d7ea7fcf0a289b97123fd34b  .beagle/checks/T0454/T0454.sh" | sha256sum -c --quiet && bash .beagle/checks/T0454/T0454.sh'
budget: 150000 tokens
