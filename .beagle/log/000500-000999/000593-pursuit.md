+++
id = "000593-pursuit"
ordinal = 593
kind = "pursuit"
timestamp = "2026-10-04T08:49:29+00:00"
summary = "pursuit open T0142: Case runner wording and capped worker report in not-done results"
metric_command = ""
drains = []
hooks = []
+++

criteria: The implementation-in-tests lead names a long function in a test file as a case runner that belongs in the code (or in a helper the module exports), never as 'implementation' that the task must write; a not-done result keeps the lead and check output in view by cutting the last worker report to a bounded length with a note where the full transcript is.
decided by: sh -c 'echo "fbeac5d140a38b4899d41c863615cce1b73a17896d648e5893ae420448e16db2  .beagle/checks/T0142/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0142/check.sh'
budget: 50000 tokens
