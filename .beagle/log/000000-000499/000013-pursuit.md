+++
id = "000013-pursuit"
ordinal = 13
kind = "pursuit"
timestamp = "2026-10-03T09:47:16+00:00"
summary = "pursuit open T0018: survey fang's 9B-model tuning for ideas tau could adopt"
metric_command = ""
drains = []
hooks = []
+++

criteria: dev-notes/itc-runs/fang-ideas.md lists at least five concrete techniques fang uses to make 9B models work (prompting, tool shapes, guards, decomposition, context management, sampling settings...), each under a ### heading with the fang file(s) it comes from and where it would land in tau (src/tau_*/ path), plus whether tau already has an equivalent. If fang has fewer real techniques, say so rather than padding.
decided by: sh -c 'echo "a8557923adf70c24916edd57c5b093900a7d989f76a447d6335d3eb2fc8e20e8  .beagle/checks/T0018/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0018/check.sh'
budget: 150000 tokens
