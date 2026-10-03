+++
id = "000363-pursuit"
ordinal = 363
kind = "pursuit"
timestamp = "2026-10-03T21:06:25+00:00"
summary = "pursuit open T0084: after compaction the driver is given the last pursuit_step result; bash 'pursuit next' is steered"
metric_command = ""
drains = []
hooks = []
+++

criteria: (a) pursuit_step's execute keeps its last result text per task in a module global (bounded, e.g. last 2000 chars); make_state_after_compaction appends 'Last pursuit_step on TNNNN said: …' verbatim for a task that is ready or open, and adds nothing when there is none. (b) 'next' is in _STEERED_VERBS, steering to pursuit_step with no arguments; the driver's bash 'beagle pursuit next' is blocked with that reason. Three named tests pin these; the compaction test uses a refused step like R10's T0002.
decided by: sh -c 'echo "ff6b00093ce07764e9fc6f7922be7152985805f4dbc22ebb54fccbf66c060ff2  .beagle/checks/T0084/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0084/check.sh'
budget: 25000 tokens
