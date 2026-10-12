+++
id = "001920-pursuit"
ordinal = 1920
kind = "pursuit"
timestamp = "2026-10-12T04:20:21+00:00"
summary = "pursuit open T0447: BEAGLE_TAU_LEAN switch: one env setting turns off the zero-catch mechanisms"
metric_command = ""
drains = []
hooks = []
+++

criteria: BEAGLE_TAU_LEAN=1 turns off the zero-catch and low-catch mechanisms named in R0002 (M14 locks, M20 plan guards, M19 abandon/done-by, M18 escalation, M07 audit, M16 own-copy, M09 already-passes, M12 cases-first, M22 read guards), each shown by a named test; every other guard keeps working under lean; with the switch unset nothing changes (full suite passes); ruff clean.
decided by: sh -c 'echo "ce1555fc7a8fdd3eb1ca6ca331a5c126fe0e093630b59ac9daa8e1a0739303e9  .beagle/checks/T0447/T0447.sh" | sha256sum -c --quiet && bash .beagle/checks/T0447/T0447.sh'
budget: 150000 tokens
