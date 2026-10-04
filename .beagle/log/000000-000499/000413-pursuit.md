+++
id = "000413-pursuit"
ordinal = 413
kind = "pursuit"
timestamp = "2026-10-04T00:44:57+00:00"
summary = "pursuit open T0107: print mode: infer user_delegated for pursuit_found"
metric_command = ""
drains = []
hooks = []
+++

criteria: In print mode (not interactive), pursuit_found founds without user_delegated when the session's prompt delegates (e.g. 'use your judgement', 'without further discussion', 'decide') or when the same goal is re-sent after the print-mode refusal; the founding result says delegation was inferred and why. A print-mode prompt that does not delegate is still refused on the first call; interactive sessions never infer delegation. Named tests pass, extension test file passes, ruff clean.
decided by: sh -c 'echo "d25e9a33433f75f3c29264c708e64f0e22636bf420676a52e9e62fc832e40e35  .beagle/checks/T0107/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0107/check.sh'
budget: 120000 tokens
