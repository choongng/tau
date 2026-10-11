+++
id = "001758-pursuit"
ordinal = 1758
kind = "pursuit"
timestamp = "2026-10-11T01:56:20+00:00"
summary = "pursuit open T0407: A done-by close opens past the rank gate with a recorded reason"
metric_command = ""
drains = []
hooks = []
+++

criteria: The beagle open that _done_by runs for a done-by close passes --over with a reason naming the done task whose work it confirms, so beagle's rank gate (T ranks below N ready task) does not refuse closing work already done, as it did in R28 (T0029 behind T0027/T0031/T0032). A test with a tree where the task ranks below another ready task shows the done-by close goes through (real beagle, or a fake that refuses an open lacking --over when ranked below). No other open gains --over. Tests named in the check; whole file passes; ruff clean.
decided by: sh -c 'echo "d79707660917e2d1c209ade16df378fe244fb212b76dc30ff6871fa3ce20de24  .beagle/checks/T0407/T0407.sh" | sha256sum -c --quiet && bash .beagle/checks/T0407/T0407.sh'
budget: 40000 tokens
