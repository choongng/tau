+++
id = "003103-pursuit"
ordinal = 3103
kind = "pursuit"
timestamp = "2026-10-14T19:49:14+00:00"
summary = "pursuit open T0598: harness: pin beagle to ~/beagle-wt/0.48 (detached 08e642c) as launch.sh's default BEAGLE_ROOT; record R99 in eval.md"
metric_command = ""
drains = []
hooks = []
+++

criteria: launch.sh's default BEAGLE_ROOT is ~/beagle-wt/0.48, a detached worktree at 0.48.0 (08e642c) or a pinned successor, and a dry run resolves beagle there; dev-notes/contract-first/eval.md has an R99 row at 75/76
decided by: sh -c 'echo "4462166c68099b74108dc731e7c96371ef02def2aebaac1dd90f7684926870ec  .beagle/checks/T0598/T0598.sh" | sha256sum -c --quiet && bash .beagle/checks/T0598/T0598.sh'
budget: 20000 tokens
