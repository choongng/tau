+++
id = "002488-pursuit"
ordinal = 2488
kind = "pursuit"
timestamp = "2026-10-12T16:37:56+00:00"
summary = "pursuit open T0486: beagle: refuse whole-tree git-status checks at open"
metric_command = ""
drains = []
hooks = []
+++

criteria: beagle contract-first: wherever a check is bound (open --check-file script, open/bind --done-when, amend), a check that reads a clean-or-not answer over the whole working tree (git status --porcelain/-s/--short with no pathspec; git diff/diff-index/diff-files --quiet/--exit-code/--name-only/--name-status with no path, not a revision pair, range or --cached) is refused, naming the pathspec fix incl. ':!.beagle'. Pathspec'd, revision-only, --cached and commented forms stand. 8 named tests (1 + 7 params); test_pursuit.py passes; CI green.
decided by: sh -c 'echo "3bc32e40573f9e2a3beae2a59691e3d9546c11fa43668ded3d089d2b09e2342f  .beagle/checks/T0486/T0486.sh" | sha256sum -c --quiet && bash .beagle/checks/T0486/T0486.sh'
budget: 150000 tokens
