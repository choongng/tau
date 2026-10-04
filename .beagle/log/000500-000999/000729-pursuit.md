+++
id = "000729-pursuit"
ordinal = 729
kind = "pursuit"
timestamp = "2026-10-04T16:14:59+00:00"
summary = "pursuit open T0170: Known-answers close checks the cases test against the data before locking"
metric_command = ""
drains = []
hooks = []
+++

criteria: Before the known-answers close locks the cases data and its test, it refuses (the task stays open, nothing is locked) when the test looks up a case name the data file does not hold, never reads the cases' expected values, or uses one attribute both as a method call and as a value, naming which; a cases test like R20's is refused and a well-formed one still locks.
decided by: sh -c 'echo "9f6a51941be00a82ef4a4f81cb7755b9bcd170ed5e0abbab8e74ea6c96b80b90  .beagle/checks/T0170/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0170/check.sh'
budget: 40000 tokens
