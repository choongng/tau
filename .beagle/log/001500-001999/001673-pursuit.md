+++
id = "001673-pursuit"
ordinal = 1673
kind = "pursuit"
timestamp = "2026-10-10T23:18:45+00:00"
summary = "pursuit open T0390: R44 fix: the source rule judges a structured result whole, and a bare bool is not judged"
metric_command = ""
drains = []
hooks = []
+++

criteria: The known-answers source rule judges a case's structured (nested) expected result whole: a source that matches only one scalar of it (e.g. a counter 0) does not count as quoting the result. A bare bool or None result has nothing searchable, so it is neither held as unquoted on that ground nor listed as 'Already sourced, keep unchanged'. Cases whose whole result is quoted pass as before. Structural, no domain words. Tests test_result_unquoted_requires_a_nested_result_not_one_scalar, test_keep_sourced_omits_a_case_with_no_searchable_result; whole file passes, ruff clean.
decided by: sh -c 'echo "9e9230d8c1000ecc676ef3ac9b547926accfb4ddc709e105d2ffe489900e1857  .beagle/checks/T0390/T0390.sh" | sha256sum -c --quiet && bash .beagle/checks/T0390/T0390.sh'
budget: 60000 tokens
