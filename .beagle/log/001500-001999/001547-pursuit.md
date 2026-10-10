+++
id = "001547-pursuit"
ordinal = 1547
kind = "pursuit"
timestamp = "2026-10-10T14:42:31+00:00"
summary = "pursuit open T0364: Worked example in the known-answers brief"
metric_command = ""
drains = []
hooks = []
+++

criteria: The known-answers (data task) brief, _references_brief(root, context_only=True) with references fetched, carries one worked example after QUOTED_SOURCE_NOTE: a made-up, domain-free reference line; a cases.json entry whose input and expected value are copied from that line and whose source quotes it verbatim; and one counter-example entry, marked wrong, whose source quotes a rule line that does not give its expected value. The example lines and both entries are module data the brief renders, not prose copies. A test writes the made-up lines to references/*.txt and each entry to tests/cases.json: _unquoted_cases returns None for the example and flags the counter-example by result (fifth element True). Neither the plain brief (context_only False) nor a brief without fetched references carries it. Tests test_known_answers_brief_has_worked_example, test_worked_example_agrees_with_the_source_judge; whole file passes, ruff clean.
decided by: sh -c 'echo "e32d95097254fb49a82a85cc49621883c55a3f70b8a439726d19f12084127d5a  .beagle/checks/T0364/T0364.sh" | sha256sum -c --quiet && bash .beagle/checks/T0364/T0364.sh'
budget: 80000 tokens
