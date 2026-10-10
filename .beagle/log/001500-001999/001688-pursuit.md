+++
id = "001688-pursuit"
ordinal = 1688
kind = "pursuit"
timestamp = "2026-10-10T23:44:15+00:00"
summary = "pursuit open T0395: Extract a normalized event table from every R01-R44 and B01-B03 session"
metric_command = ""
drains = []
hooks = []
+++

criteria: itc-harness/mine/events.py (--runs DIR --out FILE) reads every run's meta.json and each driver and worker session it lists, and writes one JSONL row per tool call, tool result and tau-level event: thinking-level change, assistant stop (with stopReason: length, aborted, error, toolUse, stop), compaction, custom/follow-up message, model change. Every row has run, model, task (prompt), role (driver|worker), session, line, t (seconds since the run's start), kind; tool rows add tool, call id, an argument digest and the argument text head; result rows add blocked (tau's 'Tool call blocked' refusal), is_error and the result text head. Counts of calls, results and blocked results per session match an independent recount. Tests in mine/test_events.py; ruff clean.
decided by: sh -c 'echo "13242627fc8b347d14e486b94fad8e0604af68afcb58e9dec36f80989e4ea57d  .beagle/checks/T0395/T0395.sh" | sha256sum -c --quiet && bash .beagle/checks/T0395/T0395.sh'
budget: 120000 tokens
