+++
id = "001705-pursuit"
ordinal = 1705
kind = "pursuit"
timestamp = "2026-10-11T00:02:56+00:00"
summary = "pursuit open T0396: Catalog refusals and map each kind to its source site and today's code"
metric_command = ""
drains = []
hooks = []
+++

criteria: itc-harness/mine/refusals.py (--events FILE --out JSON --rows JSONL) reads the T0395 event table and writes: refused.jsonl, one row per refused tool result (tau's 'Tool call blocked', tau's breaker 'Not run, and the run is stopped', and beagle's own refusals in pursuit_* result text: not run, not opened, not closed, nothing added, not a task to work now, and the like; a result that did the work is not refused) with session, line, run, model, role, tool, task id and kind id; and refusals.json, the kinds: variable parts masked (task ids, paths, numbers, quoted names), with id, a stable template, count, runs, models, roles, first and last run, an example, and live: true with site (file:line in tau src/, examples/ or ~/beagle/src) and a quote of 15+ chars that is both on that line and in the traced text, or live: false with pieces of the traced text (15+ chars each) that no source file holds now. Tests in mine/test_refusals.py; ruff clean.
decided by: sh -c 'echo "c8497a54c1924614619e45b5b2c7c9a032fdaee31a901184107ea65beb326744  .beagle/checks/T0396/T0396.sh" | sha256sum -c --quiet && bash .beagle/checks/T0396/T0396.sh'
budget: 140000 tokens
