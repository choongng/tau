+++
id = "000104-pursuit"
ordinal = 104
kind = "pursuit"
timestamp = "2026-10-03T14:26:57+00:00"
summary = "pursuit open T0039: R04 fix: a cases-first (data-only) task can close: prove by absence of the data file, locks from scope, no implementation in test files"
metric_command = ""
drains = []
hooks = []
+++

criteria: A known-answers task whose changes are only data and test files can close done: when no non-test source changed, _prove falls back to --absent on the changed data files in scope (beagle accepts that as PROVEN when the task wrote them). A done close of such a task locks its scope files when the driver gave no locks. The unproven Next text for a tests-only scope never tells the driver to import the code. A done close is refused, the task kept open with the file named, when a changed test file defines a class or a non-test top-level function.
decided by: sh -c 'echo "a031e46e87ddab5f2f223b45af9b47d9e908adb5702c834ee367d25b000a3f08  .beagle/checks/T0039/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0039/check.sh'
budget: 120000 tokens
