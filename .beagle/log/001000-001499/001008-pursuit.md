+++
id = "001008-pursuit"
ordinal = 1008
kind = "pursuit"
timestamp = "2026-10-05T08:25:10+00:00"
summary = "pursuit open T0244: The unproven refusal for a tests-only scope importing nothing gives a pursuit_step call"
metric_command = ""
drains = []
hooks = []
+++

criteria: In _unproven_call, a tests-only scope whose tests import no module gets a concrete pursuit_step call in the first line (not a Code/Tests pursuit_plan). Also (audit-12 follow-up from T0242): the 'check still fails' result does not offer new_route=true for a task whose retry chain is at SPAWN_LIMIT, but the shared _spawn_limit_offer.
decided by: sh -c 'echo "81d5b87f1d25bb6c29c6d16d6841aad2441f02b33062adc3523848cebdfa7e18  .beagle/checks/T0244/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0244/check.sh'
budget: 45000 tokens
