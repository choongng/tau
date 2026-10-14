+++
id = "002988-pursuit"
ordinal = 2988
kind = "pursuit"
timestamp = "2026-10-14T04:04:08+00:00"
summary = "pursuit open T0569: beagle: contract status 'ready' agrees with check --draft (S01 #3)"
metric_command = ""
drains = []
hooks = []
+++

criteria: contract status never says 'ready' (or 'the draft checks') for a draft that contract check --draft refuses: both use one judgement (status calls what check --draft calls, including the acceptance run), so an acceptance printing FAIL with exit 0 makes status name the refusal; test(s) *status_ready_agrees_with_check_draft* pass (a draft whose accept.sh prints FAIL and exits 0: status not ready, names check --draft's refusal; a sound draft: both ready); ci/check.sh green.
decided by: sh -c 'echo "79f11d581ac7167f50986035a2b99009ba1d51332f6fbf5099126540e0598c60  .beagle/checks/T0569/T0569.sh" | sha256sum -c --quiet && bash .beagle/checks/T0569/T0569.sh'
budget: 60000 tokens
opened over T0577, T0565: beagle lane beside the tau lane's T0573
