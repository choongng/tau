+++
id = "002801-pursuit"
ordinal = 2801
kind = "pursuit"
timestamp = "2026-10-13T20:53:53+00:00"
summary = "pursuit open T0547: tau ext: pursuit_step judges a DISPUTE at a sub-agent boundary and routes an upheld one to a contract amend"
metric_command = ""
drains = []
hooks = []
+++

criteria: When a pursuit_step worker's report ends 'DISPUTE <entry-id>' and the task's check failed with that entry FAIL, the extension runs a fresh judge sub-agent (as _audit does, no tools beyond reading) on 'beagle pursuit contract dispute <id> --brief', records its verdict with --record; on TEST WRONG it adds a contract amend task (contract scope, brief carrying the entry, the cited words and the judge's line) whose check is the contract check plus that entry's acceptance run against the judge's value, and the disputing task waits on it; on TEST RIGHT the worker's next brief says the test stands. _seal_when_ready re-seals an altered contract when an upheld dispute's amend closes, passing its reason. A DISPUTE with no matching FAIL is not judged. No change to the driver's system prompt or tool list mid-session. Tests *dispute_is_judged_and_an_upheld_one_amends_the_contract, *dispute_without_a_failing_entry_is_not_judged, *reseals_an_altered_contract_with_the_dispute_reason pass
decided by: sh -c 'echo "131c26a167ac7272b90640186c30b0982344ccf67dbf5a495739855fe50ddc87  .beagle/checks/T0547/T0547.sh" | sha256sum -c --quiet && bash .beagle/checks/T0547/T0547.sh'
budget: 180000 tokens
