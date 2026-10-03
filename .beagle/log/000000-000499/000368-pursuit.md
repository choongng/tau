+++
id = "000368-pursuit"
ordinal = 368
kind = "pursuit"
timestamp = "2026-10-03T21:13:15+00:00"
summary = "pursuit open T0085: stale-report detector needs a non-zero failure count and a narrow error term"
metric_command = ""
drains = []
hooks = []
+++

criteria: _REPORTED_FAILURE (beagle.py ~L1612) requires a non-zero count ('[1-9]\d* failed'), so '0 failed, 12 passed' is not a failure report; it also matches a Python error line ('\b\w*Error:' e.g. 'TypeError: x'), so such a report gets the superseded note. Existing matches (exit code N>0, unfixed, remaining failures, FAILED) unchanged. Two named tests pin these through _report_claims_failure.
decided by: sh -c 'echo "95989605a9fdf6f9c34378143a5e4b9659d01f82fd5815e4f77d641fcb370530  .beagle/checks/T0085/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0085/check.sh'
budget: 15000 tokens
