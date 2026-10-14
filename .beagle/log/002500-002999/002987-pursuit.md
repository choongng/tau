+++
id = "002987-pursuit"
ordinal = 2987
kind = "pursuit"
timestamp = "2026-10-14T04:03:51+00:00"
summary = "pursuit open T0573: tau: milestones are checked by contract run --operation (S01 #7)"
metric_command = ""
drains = []
hooks = []
+++

criteria: Under a declared contract with a sealed slice, pursuit_step refuses to open a non-Slice task whose check does not run 'beagle pursuit contract run --operation <op>' for an operation the sealed slices hold, and the refusal gives the exact check line to use (other commands may follow it in the check); the rule holds from the first milestone (consistent from the start, so no mid-session change); a task whose work holds no contract operation (packaging, docs) has a stated way through that the refusal names; with no declared contract nothing changes (bare goal and plain pursuits). Test milestone_check_runs_contract_operation passes; suite green outside beagle's venv.
decided by: sh -c 'echo "1b2cfd1435eb52893c1828fc9c7eaeeee4a687b7c1561c5e5794d4d6982f7771  .beagle/checks/T0573/T0573.sh" | sha256sum -c --quiet && bash .beagle/checks/T0573/T0573.sh'
budget: 80000 tokens
