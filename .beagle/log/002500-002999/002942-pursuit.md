+++
id = "002942-pursuit"
ordinal = 2942
kind = "pursuit"
timestamp = "2026-10-14T03:04:59+00:00"
summary = "pursuit open T0570: beagle: an acceptance finds the code the same way drafted and sealed (S01 #5)"
metric_command = ""
drains = []
hooks = []
+++

criteria: Beagle runs every acceptance (check, seal's codeless and stand-in runs, contract run) with cwd the project root (or the scratch copy's root) and BEAGLE_PROJECT_ROOT set to it; the slice brief's acceptance instructions name that variable and say not to locate the root relative to the script; seal runs the acceptance from where it will be sealed (contract/slices/NN-*) before accepting, so a draft-relative path is refused at seal. Tests acceptance_runs_from_project_root and seal_runs_acceptance_where_sealed pass; ci/check.sh green.
decided by: sh -c 'echo "7e5fb206997e7431a3532a0f2ebd4f4cc96949b27c988abaa352825395347659  .beagle/checks/T0570/T0570.sh" | sha256sum -c --quiet && bash .beagle/checks/T0570/T0570.sh'
budget: 100000 tokens
opened over T0565, T0575, T0569, T0572, T0573: a sealed acceptance that only finds the code by cwd breaks the first run that calls it elsewhere; T0569 is on the same tree next
