+++
id = "003362-pursuit"
ordinal = 3362
kind = "pursuit"
timestamp = "2026-10-15T21:51:27+00:00"
summary = "pursuit open T0654: pursuit_found: a source naming a reference by a near-miss spelling resolves to that file"
metric_command = ""
drains = []
hooks = []
+++

criteria: In pursuit_found and pursuit_plan, a milestone source whose token matches a references/ file's name or stem with case and the separators _ - . and space ignored resolves to that file, and the source is rewritten with the file's real name; a source naming only part of a name still joins its intent with the note.
decided by: .venv/bin/python -m pytest -q -p no:cacheprovider tests/test_beagle_example_extension.py -k 'milestone_source or placeholder'
budget: 80000 tokens
opened over T0632: T0651's bench runs ~3h in the harness checkout; this edits only the dev tau
