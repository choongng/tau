+++
id = "003374-pursuit"
ordinal = 3374
kind = "pursuit"
timestamp = "2026-10-15T22:22:42+00:00"
summary = "pursuit open T0655: pursuit_found: a request link or references/ name written inside a milestone's part becomes its Source"
metric_command = ""
drains = []
hooks = []
+++

criteria: In pursuit_found and pursuit_plan, a milestone given no source whose part (string or dict) carries a link, or under a project names a references/ file by name or stem, gets that as its Source: — a link is taken out of the words with a leading 'based on/from/per/see' and trailing punctuation; a part with no title::intent split keeps its words as the title; a milestone given a source keeps its part's words as they are.
decided by: .venv/bin/python -m pytest -q -p no:cacheprovider tests/test_beagle_example_extension.py -k 'milestone_source or placeholder or milestone_part'
budget: 80000 tokens
opened over T0632: R132 (g26) is two rounds away and this is g26's linked founding defect (F011/F012 → R123 path); T0632 is test-pinning with no run waiting on it
