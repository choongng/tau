+++
id = "000388-pursuit"
ordinal = 388
kind = "pursuit"
timestamp = "2026-10-03T21:23:32+00:00"
summary = "pursuit open T0088: re-run-only founding milestones are dropped with a note"
metric_command = ""
drains = []
hooks = []
+++

criteria: _repair_milestones applies T0066's _rerun_only_part to founding milestones: a milestone like 'Run all tests and confirm they pass' is dropped (not refused, so founding still succeeds), and the founding result carries a note naming it and why. Other milestones pass on unchanged and in order. One named test pins this.
decided by: sh -c 'echo "6afe023705e7ae4730724b8f530b9dc7f4f5e60e882a64fa6fdaaae31ec8ec45  .beagle/checks/T0088/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0088/check.sh'
budget: 15000 tokens
