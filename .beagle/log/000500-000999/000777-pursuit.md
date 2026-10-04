+++
id = "000777-pursuit"
ordinal = 777
kind = "pursuit"
timestamp = "2026-10-04T23:05:43+00:00"
summary = "pursuit open T0200: Escalation after an unproven pass keeps the passing check and adds the data file; no placeholder calls"
metric_command = ""
drains = []
hooks = []
+++

criteria: After a passing check is found unproven, the escalation refusal and its offered call keep the bound check (no new check required) and name adding the data file the test reads to the scope; no offered call contains a <placeholder>; the proof note for a data test scoped without its data names that data file. Prompt-independent: decided from the tree, the check's AST and data suffixes.
decided by: sh -c 'echo "fd33b528309957f934a8d6a456d13ec354a49007ac45be2dc1180d7afafc770a  .beagle/checks/T0200/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0200/check.sh'
budget: 150000 tokens
