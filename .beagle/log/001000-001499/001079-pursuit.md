+++
id = "001079-pursuit"
ordinal = 1079
kind = "pursuit"
timestamp = "2026-10-05T12:04:02+00:00"
summary = "pursuit open T0259: Done-by ImportError-only branch tested"
metric_command = ""
drains = []
hooks = []
+++

criteria: A done-by witness whose refusal is only an ImportError/ModuleNotFoundError (collection error) is not taken as proof: _done_by releases rather than closes, with the 'taken away only on importing' text; a test drives that branch in _done_by, separate from the _prove one.
decided by: sh -c 'echo "3f1f60d3904ddfa94eec7e50868efc3460c8dcfc999abd4ad0197c5a21420445  .beagle/checks/T0259/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0259/check.sh'
budget: 30000 tokens
