+++
id = "002978-pursuit"
ordinal = 2978
kind = "pursuit"
timestamp = "2026-10-14T03:51:46+00:00"
summary = "pursuit open T0575: beagle: contract run --operation X prints only X's entries (S01 #8)"
metric_command = ""
drains = []
hooks = []
+++

criteria: contract run --operation X prints the ok/FAIL lines of X's entries only (other operations' lines, even failing ones, are not printed; at most a one-line count of them), then its verdict; the exit status is unchanged (0 iff X's entries all pass); test(s) *run_operation_prints_only_its_entries* pass (an acceptance where X passes and Y fails: no Y line in the output, exit 0; X failing: exit non-zero naming X's failures); ci/check.sh green.
decided by: sh -c 'echo "39cb033b8ed0c6cf9680c4b198d4c8f8abe5ff0288ffbf79c613fbd2ec5aa68d  .beagle/checks/T0575/T0575.sh" | sha256sum -c --quiet && bash .beagle/checks/T0575/T0575.sh'
budget: 60000 tokens
