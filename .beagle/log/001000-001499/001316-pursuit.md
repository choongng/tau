+++
id = "001316-pursuit"
ordinal = 1316
kind = "pursuit"
timestamp = "2026-10-09T21:47:09+00:00"
summary = "pursuit open T0314: R36 fix: a case's known-answer check requires each changed result field, not any one"
metric_command = ""
drains = []
hooks = []
+++

criteria: _case_results compares a case's expected results with its inputs flattened at any depth, and drops a result field equal to any input field (so a nested input id echoed in the result is not counted as a result). _result_unquoted then flags a case unless each remaining result renders in the quoted context, not just any one of them; T0293's narrow/wide handling is kept. R36's four wrong final cases (a fixture with their quoted reference lines) are flagged; a case whose every changed field is in its quoted line passes (negative test). Keyed on JSON structure and the comparison rule; no prompt words.
decided by: sh -c 'echo "3923bd3b915ee476e6bf36df8f3565455dff8748757bc211b5a24e7fce83e729  .beagle/checks/T0314/T0314.sh" | sha256sum -c --quiet && bash .beagle/checks/T0314/T0314.sh'
budget: 120000 tokens
