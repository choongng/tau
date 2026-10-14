+++
id = "002876-pursuit"
ordinal = 2876
kind = "pursuit"
timestamp = "2026-10-14T00:46:36+00:00"
summary = "pursuit open T0561: merge rotation-fixes (T0554-T0558) into contract-first, CI green"
metric_command = ""
drains = []
hooks = []
+++

criteria: contract-first contains rotation-fixes through b9efa1d (T0554-T0558), its worktree is on the contract-first branch and clean, and ci/check.sh is green on a clean checkout of its tip.
decided by: sh -c 'echo "974196dccb808ccfdc90c09874436345a92822b0ad9a2deaa41e194f04a16487  .beagle/checks/T0561/T0561.sh" | sha256sum -c --quiet && bash .beagle/checks/T0561/T0561.sh'
budget: 60000 tokens
