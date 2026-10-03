+++
id = "000352-pursuit"
ordinal = 352
kind = "pursuit"
timestamp = "2026-10-03T20:49:47+00:00"
summary = "pursuit open T0083: a never-opened setup milestone can be abandoned, and the .beagle refusal says how"
metric_command = ""
drains = []
hooks = []
+++

criteria: _abandon_problem accepts abandoning a milestone that was never opened (no open/close events, no children worked) when the milestone is setup by _setup_milestone's rule; any other milestone, or a setup one that was opened, is still refused as before. The refusal tau gives when a step names a .beagle path in scope (R10's T0002) names that abandon as the way out, with the exact call. Three named tests pin these.
decided by: sh -c 'echo "9b118bb3445602e1ba0e4f948e15b16d2396cf42a8769865446a0125d488c59e  .beagle/checks/T0083/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0083/check.sh'
budget: 25000 tokens
