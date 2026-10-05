+++
id = "001215-pursuit"
ordinal = 1215
kind = "pursuit"
timestamp = "2026-10-05T20:46:22+00:00"
summary = "pursuit open T0288: R35 fix: the not-done verdict reaches the rerun with its file and defect"
metric_command = ""
drains = []
hooks = []
+++

criteria: When a close keeps a task open for a specific defect in a named file, the next brief and stays-open reason carry that file and defect verbatim, not only generic advice; when the bound check fails at collection or import, the not-done lead names the failing import and file before any runner message; the known-answers brief no longer says the check fails with ImportError until the code exists, and says an ImportError from the bound data check is a defect to fix. Regression tests for each.
decided by: sh -c 'echo "6da4a1193d59bc7e30d2afc3ca94be5389e6d5f4452c950c36085ec5308a35f8  .beagle/checks/T0288/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0288/check.sh'
budget: 150000 tokens
