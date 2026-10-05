+++
id = "000897-pursuit"
ordinal = 897
kind = "pursuit"
timestamp = "2026-10-05T04:37:07+00:00"
summary = "pursuit open T0225: A known-answers open whose check names a test not yet on disk binds the data test"
metric_command = ""
drains = []
hooks = []
+++

criteria: A known-answers open (data file in scope) whose done_when runs a test file that is in scope but not yet on disk, beside a data test that is on disk or also named, is bound to run the data test only, as the import-based rebind does when the cases test imports an unwritten module; the result says so; an open whose named test is the only test is unchanged.
decided by: sh -c 'echo "6162c01b661603eea4fc2a31a4083621778787742be58a7fbb2444b870dae567  .beagle/checks/T0225/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0225/check.sh'
budget: 60000 tokens
