+++
id = "002756-pursuit"
ordinal = 2756
kind = "pursuit"
timestamp = "2026-10-13T20:10:20+00:00"
summary = "pursuit open T0537: beagle: acceptance names a missing operation; contract run names a shared failure"
metric_command = ""
drains = []
hooks = []
+++

criteria: beagle's contract brief asks the acceptance to load each operation on its own, by the name the goal's own criteria import it under (from the project root, so a module or a package both serve) and never by a file path, and to report FAIL for each entry of an operation it could not load, with the exception it caught; 'pursuit contract run' says, when every failing entry fails for one and the same reason, that the acceptance cannot reach the code, and names that reason. Tests test_contract.py::*asks_for_one_import_per_operation (asserting the import-by-name wording too) and *names_one_reason_every_entry_fails_for pass; ci/check.sh green on rotation-fixes
decided by: sh -c 'echo "6801e71928eeddabec2fb2b0d1d07a69f99df915e64ec0ac4018e4bfcb99f70c  .beagle/checks/T0537/T0537.sh" | sha256sum -c --quiet && bash .beagle/checks/T0537/T0537.sh'
budget: 150000 tokens
