+++
id = "000014-pursuit"
ordinal = 14
kind = "pursuit"
timestamp = "2026-10-03T09:51:29+00:00"
summary = "pursuit prove T0018: WITNESSED — refuses when fang-ideas.md is absent"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "a8557923adf70c24916edd57c5b093900a7d989f76a447d6335d3eb2fc8e20e8  .beagle/checks/T0018/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0018/check.sh'
refutes: refuses when fang-ideas.md is absent (proven 2026-10-03T09:51:29+00:00)
refused after 0s of a 0s check
