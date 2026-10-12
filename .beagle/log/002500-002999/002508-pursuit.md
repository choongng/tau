+++
id = "002508-pursuit"
ordinal = 2508
kind = "pursuit"
timestamp = "2026-10-12T17:05:30+00:00"
summary = "pursuit retire T0135 by T0488 (moved)"
metric_command = ""
drains = []
hooks = []
+++

T0135 pinned R15's repair: a read-and-design founding milestone retitled 'Known answers from the reference', and FOUND_FIRST_NOTE naming the known answers as the first milestone. R0003 moved that on purpose: founding now seeds the contract (Contract, Second extraction) ahead of the milestones, so read/design-only milestones fold into the work and FOUND_FIRST_NOTE names the contract. The two tests were renamed (..._names_the_contract_not_read_and_design, ..._is_folded_into_the_work) and still guard that reading and design are not milestones; T0488's check runs them in the full suite.
