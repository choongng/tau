+++
id = "002730-pursuit"
ordinal = 2730
kind = "pursuit"
timestamp = "2026-10-13T19:26:00+00:00"
summary = "pursuit open T0538: beagle: prove credits a change an earlier, killed attempt at the task made"
metric_command = ""
drains = []
hooks = []
+++

criteria: In tau's beagle extension (not beagle itself), when a worker gives no WITNESS, the automatic prove also tries each file in the task's scope that was modified since the task opened, putting back its content at the open (--mutate with the reversion edit, as _reversion_edit makes), before reporting 'no WITNESS'. A task whose check an earlier attempt made pass is then proven, not superseded. Tests test_auto_prove_reverts_a_scope_file_changed_since_open and test_auto_prove_reports_no_witness_and_no_change pass.
decided by: sh -c 'echo "18bd0836f8439f8c95638d9eef13ed2c813a3f041fc350cf5e5cbddc26de920a  .beagle/checks/T0538/T0538.sh" | sha256sum -c --quiet && bash .beagle/checks/T0538/T0538.sh'
budget: 150000 tokens
