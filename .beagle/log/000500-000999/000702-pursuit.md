+++
id = "000702-pursuit"
ordinal = 702
kind = "pursuit"
timestamp = "2026-10-04T14:05:02+00:00"
summary = "pursuit open T0165: Founding drops a Found-the-pursuit milestone"
metric_command = ""
drains = []
hooks = []
+++

criteria: pursuit_found drops a milestone whose title names the pursuit or beagle with a founding verb (found, founding, founded, start, create), e.g. R19's 'Found the pursuit: implement interval tree clocks…', with the setup-milestone note; real work milestones are kept.
decided by: sh -c 'echo "b191e9d45013854e710b5a92635942c4b9a04da252393bd2e4a0839f3adf91a8  .beagle/checks/T0165/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0165/check.sh'
budget: 25000 tokens
