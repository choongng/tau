+++
id = "000156-pursuit"
ordinal = 156
kind = "pursuit"
timestamp = "2026-10-03T16:28:36+00:00"
summary = "pursuit open T0051: Audit: untested clauses of T0040, T0041, T0044, T0048 get named tests; check helpers committed"
metric_command = ""
drains = []
hooks = []
+++

criteria: The clauses audit 2 found untested or unnamed have named tests that this check runs: the T0040 not-done count resets on new_route and on a plan (existing tests), the T0048 successor abandon (existing test), a task worker's dispatched brief carries NO_BEAGLE_NOTE (new, through pursuit_step, not the constant), and the T0044 stop gate sends no unfounded follow-up in an interactive session or a founded one (two new). The shared check helpers fix/named_tests.sh and runs/diagnosed.sh are committed (scored.sh already is).
decided by: sh -c 'echo "46ac3feb2124a17aae921b80036ba8c04542c9c924fa06ec282646565f8fb6ad  .beagle/checks/T0051/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0051/check.sh'
budget: 30000 tokens
