+++
id = "000530-pursuit"
ordinal = 530
kind = "pursuit"
timestamp = "2026-10-04T04:57:58+00:00"
summary = "pursuit open T0127: Tests for unguarded clauses of T0118, T0123, T0124"
metric_command = ""
drains = []
hooks = []
+++

criteria: Tests pin: _check_broke refusing exit 127 (missing command) and exit 2 with a usage: line at open; _locked_test_imports skipping a test that imports the module but reads no locked data, with an earlier lock present so the store is not empty; _cases_test_reads requiring the open/Path/read_text call to take the cases file name (a bare Path(__file__) plus a message string naming cases.json does not count); the part-abandon refusal offering abandon="done by Tnnnn" and never saying it closes done at once; a done-by close on a pending milestone. The code changes only where a pinned behaviour is wrong.
decided by: sh -c 'echo "e86c4262f98309838477b3d6a26e8671ddae650fe188d2127df27183819f33fd  .beagle/checks/T0127/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0127/check.sh'
budget: 60000 tokens
