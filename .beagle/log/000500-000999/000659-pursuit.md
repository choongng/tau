+++
id = "000659-pursuit"
ordinal = 659
kind = "pursuit"
timestamp = "2026-10-04T11:39:09+00:00"
summary = "pursuit open T0156: R15 cases fixture covers all 32 cases"
metric_command = ""
drains = []
hooks = []
+++

criteria: A test copies R15's full cases file (all 32 cases from ~/itc.r15/tests/cases.json) and the reference lines it quotes as fixtures, and asserts every case counts as quoting the reference.
decided by: sh -c 'echo "58a69bca34a7c2d6b2a65ed70ff2edb53faf616b49402b66cd7665ed3429b98b  .beagle/checks/T0156/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0156/check.sh'
budget: 30000 tokens
opened over T0099: audit defect: becomes work before more is opened, and it is a small test-only fix ahead of a 1h run
