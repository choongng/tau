+++
id = "000490-pursuit"
ordinal = 490
kind = "pursuit"
timestamp = "2026-10-04T03:26:56+00:00"
summary = "pursuit open T0123: Locked cases test must read the cases file"
metric_command = ""
drains = []
hooks = []
+++

criteria: When a task's locks include a cases data file and a cases test, the close keeps it open and locks nothing unless the cases test reads the data file: the test's code (not a docstring or comment) names the data file's basename and opens or loads it. _locked_test_imports skips a locked test that does not read its cases file, so the cases-first gate does not steer toward it.
decided by: sh -c 'echo "11104116742d96fd2c1444f35d7f4081b62975262c13760f8a719673d48b4685  .beagle/checks/T0123/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0123/check.sh'
budget: 120000 tokens
