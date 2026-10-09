+++
id = "001333-pursuit"
ordinal = 1333
kind = "pursuit"
timestamp = "2026-10-09T22:14:15+00:00"
summary = "pursuit open T0318: Audit 11: a narrow result is not found by coincidence in the line after the quote"
metric_command = ""
drains = []
hooks = []
+++

criteria: A narrow result (T0293's sense) is only found in its quoted context as a whole value, not as a fragment of a larger token such as the 2 in '{0,2}' or in '(1,2)' on the line after the quote; how the line after is used stays T0293's rule otherwise. All four of R36's wrong final cases in the test fixture are flagged by _unquoted_cases (test asserts ['#1','#2','#3','#4']), while R35's and R36's correctly quoted fixture cases and the existing narrow-result tests still pass. Keyed on token boundaries and JSON structure; no prompt words.
decided by: sh -c 'echo "c0eebbedcd2c039acd1f640fe1978453038f9b630a989ba608858f353619e37a  .beagle/checks/T0318/T0318.sh" | sha256sum -c --quiet && bash .beagle/checks/T0318/T0318.sh'
budget: 100000 tokens
