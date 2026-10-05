+++
id = "000969-pursuit"
ordinal = 969
kind = "pursuit"
timestamp = "2026-10-05T07:44:17+00:00"
summary = "pursuit open T0238: The data test rebind and proof see the data test as it is run"
metric_command = ""
drains = []
hooks = []
+++

criteria: The data-test rebind never proposes the bound check itself: when the test it would pick is the one importing the unwritten module, tau runs the step with a note to drop that import instead of refusing; a check that runs a test file as python/python3 <file> counts as running that file for every helper that asks whether the check runs a test.
decided by: sh -c 'echo "3fb0dc72db81355dd814d8eea68b647e022208caeeaecf07064f5d52c8023562  .beagle/checks/T0238/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0238/check.sh'
budget: 70000 tokens
