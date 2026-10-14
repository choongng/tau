+++
id = "002941-pursuit"
ordinal = 2941
kind = "pursuit"
timestamp = "2026-10-14T03:04:59+00:00"
summary = "pursuit open T0571: tau: a slice's seal is committed so the tree stays clean (S01 #6)"
metric_command = ""
drains = []
hooks = []
+++

criteria: When a Slice: task's done close seals its draft, tau commits the seal (contract/slices/NN-* added, contract/draft removals staged, nothing else) with a message naming the slice and the task, so git status over the project is clean after it and the workspace-clean gate stays green; a refused seal commits nothing. Test slice_seal_is_committed and the whole extension suite pass outside beagle's venv.
decided by: sh -c 'echo "e4a5f0c9d966fe17edf402a97ffaed551e1cd4cdfed045fb532238cfa4772a4a  .beagle/checks/T0571/T0571.sh" | sha256sum -c --quiet && bash .beagle/checks/T0571/T0571.sh'
budget: 100000 tokens
opened over T0565, T0575, T0569, T0572, T0573: S01's red workspace gate stalls every run after the first seal; T0567/T0568 follow on the same file
