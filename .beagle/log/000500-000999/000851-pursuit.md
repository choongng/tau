+++
id = "000851-pursuit"
ordinal = 851
kind = "pursuit"
timestamp = "2026-10-05T02:19:29+00:00"
summary = "pursuit open T0216: An amended or new-route check is proved as itself and binds && the same way open does"
metric_command = ""
drains = []
hooks = []
+++

criteria: After pursuit_step amends an open task's check, the old check's unproven mark and exit are forgotten, so the new check is judged on its own run; the result names the bound check and scope; refusals that ran no worker do not count toward the escalation step count; new_route binds a bare && through bash -c as open and amend do.
decided by: sh -c 'echo "5c0adbda9a69997a2cd12ebd5d7eb4b467a98acde33e894b3d69ecd2711a6338  .beagle/checks/T0216/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0216/check.sh'
budget: 80000 tokens
