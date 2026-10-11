+++
id = "001731-pursuit"
ordinal = 1731
kind = "pursuit"
timestamp = "2026-10-11T00:51:50+00:00"
summary = "pursuit open T0399: Write dev-notes/itc-runs/mining.md and file the live findings as fix tasks"
metric_command = ""
drains = []
hooks = []
+++

criteria: itc-harness/mine/findings.py turns refusals.py, contradictions.py and indicators.py output into ranked findings (class, title, count, runs, models, trace lines, live) by fixed rules: every offered-then-refused kind pair seen 2+ times, the most repeated and alternating kinds, kinds with many unrecovered rows, non-reported worker outcomes, abnormal stops, driver-side implementation work, the longest non-dispatch time sinks. A refusal-backed finding is live only if today's code still writes its kinds. mine/dispositions.json gives each finding fixed (commit+test), task (a filed fix task), deferred, not_live or not_a_bug, with a reason. mining.md says how to rerun every script, carries the generated table verbatim, ranks and explains the findings, and has a Known answers section on where runs stalled (9/13 that closed that task passed any test, 3/31 that did not), split worker-side vs driver-side, with the stronger-model opportunity and its caveats.
decided by: sh -c 'echo "19f39c0bcb16f8719f4442a26e393d3dbbf75ef9fa4d45fc27b92f9f2baf78fd  .beagle/checks/T0399/T0399.sh" | sha256sum -c --quiet && bash .beagle/checks/T0399/T0399.sh'
budget: 160000 tokens
