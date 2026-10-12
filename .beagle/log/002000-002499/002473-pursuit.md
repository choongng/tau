+++
id = "002473-pursuit"
ordinal = 2473
kind = "pursuit"
timestamp = "2026-10-12T16:19:29+00:00"
summary = "pursuit open T0483: beagle: contract briefs"
metric_command = ""
drains = []
hooks = []
+++

criteria: beagle contract-first: with [contract] declared, 'pursuit brief' for a task scoped within the contract's files and references/ carries the inventory wording (worked examples, limits, invalid inputs, operations; quote the source; gaps asked or assumed, never guessed) and the file's shape, says to use 'contract check' and not to seal; for the second extraction's file it says not to open the primary; for other work, before the seal it says the task is reconnaissance and to report sources, after it that the sealed contract is what done means and its files are not edited (ALTERED named); without [contract] it says nothing of one. 4 named tests; the file passes.
decided by: sh -c 'echo "6badde3e281f576dc9e42cc49ef13311e9c16d127675c260a00facc61109a021  .beagle/checks/T0483/T0483.sh" | sha256sum -c --quiet && bash .beagle/checks/T0483/T0483.sh'
budget: 200000 tokens
