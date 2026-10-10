+++
id = "001483-pursuit"
ordinal = 1483
kind = "pursuit"
timestamp = "2026-10-10T03:45:40+00:00"
summary = "pursuit open T0347: Known-answers verdict: say to replace a case the references give no result for"
metric_command = ""
drains = []
hooks = []
+++

criteria: When the known-answers close finds a case whose result no line of references/*.txt gives (the unquoted[4] branch), its verdict says the case must be replaced with one whose input and result the reference both gives, and names candidate reference lines that carry a concrete result (a new _result_lines(root) beside _value_lines), without naming the project or its domain. Regression tests test_known_answers_unsourced_result_says_replace_the_case and test_known_answers_unsourced_result_names_reference_result_lines in tests/test_beagle_example_extension.py; the whole file passes and ruff is clean.
decided by: sh -c 'echo "c814e27259f5b887d37f5d85332120b8c406e8931fb57b958027f1108db10149  .beagle/checks/T0347/T0347.sh" | sha256sum -c --quiet && bash .beagle/checks/T0347/T0347.sh'
budget: 80000 tokens
