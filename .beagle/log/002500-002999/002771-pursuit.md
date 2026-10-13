+++
id = "002771-pursuit"
ordinal = 2771
kind = "pursuit"
timestamp = "2026-10-13T20:19:41+00:00"
summary = "pursuit open T0541: beagle seal: a codeless entry that fails for another reason is the acceptance's own defect"
metric_command = ""
drains = []
hooks = []
+++

criteria: 'pursuit contract seal', in its codeless run (the sealed files and references/ copied without the code), reads each entry's FAIL reason; when most failing entries share one reason (the code cannot be loaded, as T0537's shared_failure reads it) and some entries fail for a different reason, seal refuses, naming each such entry and its reason as the acceptance's own defect (it never reached the code: an input it cannot parse, a name it never defined). Test test_contract.py::*seal_names_an_entry_failing_codeless_for_another_reason covers R96's shape (prose input -> 'invalid syntax' beside 'No module named'), and that a contract whose every entry fails for the one load reason still seals; ci/check.sh green on rotation-fixes
decided by: sh -c 'echo "afc053d9f2f60479eaff83f4bfadf136c9f087172871d91b68d61d6de7a30aa7  .beagle/checks/T0541/T0541.sh" | sha256sum -c --quiet && bash .beagle/checks/T0541/T0541.sh'
budget: 120000 tokens
opened over T0534, T0540: T0534 waits on B07 (running till ~14:05); T0540 should carry this fix into R97
