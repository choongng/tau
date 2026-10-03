+++
id = "000275-pursuit"
ordinal = 275
kind = "pursuit"
timestamp = "2026-10-03T19:59:27+00:00"
summary = "pursuit open T0067: T0059 guard expands directory scopes against disk"
metric_command = ""
drains = []
hooks = []
+++

criteria: _oracle_with_code_problem also judges directory scope entries against disk: a test-path directory (tests/) that holds an unlocked non-.py file (tests/cases.json) counts as data; a non-test directory (src/) that holds .py files counts as source. R09: scope ['src/', 'tests/'] with tests/cases.json on disk and unlocked is refused before any worker runs, naming tests/cases.json; ['src/'] alone, or with the cases locked, is accepted.
decided by: sh -c 'echo "bba7aecda4842179c7e3411ad74de0da4026921a0a59f453db30bff6f1567fb5  .beagle/checks/T0067/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0067/check.sh'
budget: 40000 tokens
