+++
id = "001242-pursuit"
ordinal = 1242
kind = "pursuit"
timestamp = "2026-10-09T18:31:43+00:00"
summary = "pursuit open T0291: R35 fix: a data test importing unwritten code through a sibling test is seen"
metric_command = ""
drains = []
hooks = []
+++

criteria: _imports_unwritten resolves a test_* import to a sibling test file in the project (same dir or a tests package), recurses into it with a visited set, and reports the chain (data test -> sibling -> unwritten module) when the sibling imports code no path in scope creates; _self_import_note names that chain and says a data test imports no other test (copy what it needs or read the data file directly); _kept_data_check does not keep a bound check that _imports_unwritten flags, and instead says neither test can pass and gives the self-import fix. No prompt-specific names. Regression tests for each.
decided by: sh -c 'echo "0f247735d47d3349591234aea45ce4a1ac6905ed28a79fdbc022ef9100f63809  .beagle/checks/T0291/T0291.sh" | sha256sum -c --quiet && bash .beagle/checks/T0291/T0291.sh'
budget: 150000 tokens
