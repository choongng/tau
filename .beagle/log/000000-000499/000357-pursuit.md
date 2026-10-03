+++
id = "000357-pursuit"
ordinal = 357
kind = "pursuit"
timestamp = "2026-10-03T20:53:12+00:00"
summary = "pursuit open T0082: driver may not hand-edit beagle config, and non-pursuit streaks stay counted after founding"
metric_command = ""
drains = []
hooks = []
+++

criteria: In the driver session (the started session; sub-agents unaffected): (a) a write/edit tool call whose path is under .beagle/, or a bash call that writes a .beagle/ file (redirection, tee, sed -i, cp/mv into it, a python -c/heredoc writing it), is refused, the reason saying the pursuit tools own .beagle and naming pursuit_step; reading .beagle (cat, ls, read) still runs. (b) After the goal exists, more than DRIVER_OFF_PURSUIT_CALLS (a module constant, 8) consecutive non-pursuit_ calls are refused with a reason naming pursuit_step and the streak; any pursuit_ call resets it; the count resets per session start like _SETUP_CALLS. Four named tests pin these, one modelled on R10's gates.toml edit.
decided by: sh -c 'echo "918f9492fa2da16334d0ba72eec1f0075b6881e74b62240324f44b9e6f588551  .beagle/checks/T0082/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0082/check.sh'
budget: 30000 tokens
