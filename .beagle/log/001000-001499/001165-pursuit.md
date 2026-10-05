+++
id = "001165-pursuit"
ordinal = 1165
kind = "pursuit"
timestamp = "2026-10-05T17:24:08+00:00"
summary = "pursuit open T0278: Close judge counts path.open and with-as handles as reads; refuses a cases test with nothing to collect or a name it never imports"
metric_command = ""
drains = []
hooks = []
+++

criteria: _cases_test_reads counts a data file opened as <path>.open(...) or read via read_text/read_bytes on a path, and json.load/load on a handle bound by with ... as; _cases_test_problem names a cases test that defines no test function pytest collects, and one that calls a module name it never imports.
decided by: sh -c 'echo "6ca44cd765747735cea69bbcf2935a52864992f0e335207ab39d0b22b27c8889  .beagle/checks/T0278/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0278/check.sh'
budget: 70000 tokens
