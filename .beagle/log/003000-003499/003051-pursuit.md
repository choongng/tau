+++
id = "003051-pursuit"
ordinal = 3051
kind = "pursuit"
timestamp = "2026-10-14T06:01:55+00:00"
summary = "pursuit open T0583: beagle: a limits slice where the sources are silent on malformed input holds a gap with an assumption, and seal refuses a limits slice with neither a limit/invalid entry nor a gap (R84)"
metric_command = ""
drains = []
hooks = []
+++

criteria: beagle: the limits-and-invalid slice brief asks, where the sources say nothing about an operation's malformed input, for a gap with "operation": "X" and an assumption (one short sentence); seal refuses a slice whose name marks it as X's limits slice when it holds neither a limit/invalid entry of X nor such a gap, naming both ways out; a bare-goal fixture (no references) passes with a gap. Tests matching *silent_source_gap*; ci green; README count updated.
decided by: sh -c 'echo "7c7058443c0d8680f66fd719f8d4f8fd0197e3a9685c2614222449d178edef93  .beagle/checks/T0583/T0583.sh" | sha256sum -c --quiet && bash .beagle/checks/T0583/T0583.sh'
budget: 80000 tokens
