+++
id = "001022-pursuit"
ordinal = 1022
kind = "pursuit"
timestamp = "2026-10-05T09:45:33+00:00"
summary = "pursuit open T0249: A worker's cut-off calls and silent end reach the driver"
metric_command = ""
drains = []
hooks = []
+++

criteria: A call cut off at the output limit is refused with a budget in characters (not lines) and a script hint; the 2nd cut-off in one worker says the same size will be cut again; a worker turn whose tool result is the cut-off refusal counts as a length stop so a later timeout names the output limit, not the turn cap; a step result after several worker runs names each earlier run that ended without a report, with what it changed and its last words.
decided by: sh -c 'echo "b8ccd49b995c6a42a5027614593f5472b747c813e58a0bb204adc7aaa7d6e246  .beagle/checks/T0249/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0249/check.sh'
budget: 60000 tokens
