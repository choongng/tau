+++
id = "003023-pursuit"
ordinal = 3023
kind = "pursuit"
timestamp = "2026-10-14T04:32:38+00:00"
summary = "pursuit open T0572: beagle: seal refuses an entry whose stand-in failure is the acceptance's own error (S01 #4)"
metric_command = ""
drains = []
hooks = []
+++

criteria: Per dev-notes/contract-first/standin-crash-recon.md's recommendation: the contract worker writes a right-answer stand-in in its own place (proposed <draft>/oracle/, not a numbered standin/ dir) that answers each example with its expect and rejects each invalid input; seal (and check --draft) runs the acceptance under it and refuses, naming each entry and its reason, any example/limit/invalid entry that fails there (properties are not judged by it); a draft with such entries and no oracle is refused with how to write one; the slice brief says so in a sentence; refusal text as the recommendation gives. Tests matching *oracle_standin* pass, including: S01's sealed acceptance (fixture from ~/semver/contract/slices/01-examples, copied) refused for ex-015..017 and nothing else; the r97_semver / wrenfold_r3 / r73_itc fixtures keep their current verdicts or the change is stated. ci/check.sh green.
decided by: sh -c 'echo "4b2b4baf09b6de4612508c09136fa5ecc433ecd716c8484c76dd09185a48eaff  .beagle/checks/T0572/T0572.sh" | sha256sum -c --quiet && bash .beagle/checks/T0572/T0572.sh'
budget: 120000 tokens
opened over T0580: R98 waits on the seal catching tests that can never pass; T0580 is a p3 env leak worked around today
