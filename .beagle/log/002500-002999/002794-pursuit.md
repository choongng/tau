+++
id = "002794-pursuit"
ordinal = 2794
kind = "pursuit"
timestamp = "2026-10-13T20:39:24+00:00"
summary = "pursuit open T0546: beagle: contract dispute verb, recorded verdicts, re-seal with a reason"
metric_command = ""
drains = []
hooks = []
+++

criteria: beagle's contract brief tells a worker who finds a sealed test contradicting its cited source to end its report with 'DISPUTE <entry-id>'; 'pursuit contract dispute <id> --brief' prints a judge brief holding only the entry, the source lines it cites and the acceptance lines that test it (no code, no worker prose) and asks for 'TEST WRONG: <value>' or 'TEST RIGHT'; 'pursuit contract dispute <id> --record --verdict wrong|right --reason R' appends the verdict to the record, and refuses an id the last acceptance run did not report FAIL; 'pursuit contract seal --reason R' on an altered contract keeps R beside the seal count. Tests *dispute_brief_holds_the_entry_its_cite_and_its_test, *dispute_refuses_an_entry_that_did_not_fail, *reseal_keeps_its_reason pass; ci/check.sh green on rotation-fixes
decided by: sh -c 'echo "f9a9f4aa344d1cef4e4774a0587afddc4f1325859a91a40453ae1ba806532edb  .beagle/checks/T0546/T0546.sh" | sha256sum -c --quiet && bash .beagle/checks/T0546/T0546.sh'
budget: 150000 tokens
