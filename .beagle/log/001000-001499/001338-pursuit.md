+++
id = "001338-pursuit"
ordinal = 1338
kind = "pursuit"
timestamp = "2026-10-09T22:25:38+00:00"
summary = "pursuit open T0317: Audit 11: the no-source-quoting verdict names each flagged case's source, not only the first"
metric_command = ""
drains = []
hooks = []
+++

criteria: The 'no source quoting' verdict names, for each case it names as flagged (up to the three it lists), the source string it searched, or that the case has no source string; the first case keeps the full explanation of what was searched, the others say their source in a short sentence. _unquoted_cases returns the (name, source) pairs for the named cases. Existing verdict tests still pass.
decided by: sh -c 'echo "1a132151a94eb213635e5414830ab7b428707a7bed8f54eefdd2af5af3e931e6  .beagle/checks/T0317/T0317.sh" | sha256sum -c --quiet && bash .beagle/checks/T0317/T0317.sh'
budget: 40000 tokens
