+++
id = "001843-pursuit"
ordinal = 1843
kind = "pursuit"
timestamp = "2026-10-11T23:07:37+00:00"
summary = "pursuit open T0437: Data-only known-answers tasks get a sound witness"
metric_command = ""
drains = []
hooks = []
+++

criteria: A known-answers task whose scope holds only tests and data can be proven soundly. In beagle.py's _prove: a WITNESS naming the cases data file (_is_cases_data, e.g. tests/cases.json) is a site, not refused as 'in a test file', when that data is what the check reads; the absence fallback never takes away a file the bound done_when names (its own script), and a witness whose only failure comes from removing such a file is refused as vacuous (q38fn 10-11 T0011: the check failed only because tests/check_known_answers.py was gone). Tests named in the check; whole file passes; ruff clean.
decided by: sh -c 'echo "9871846cb348a4ab3804bdd269daa87f6be769497e4c80d1a2785c504bd1f672  .beagle/checks/T0437/T0437.sh" | sha256sum -c --quiet && bash .beagle/checks/T0437/T0437.sh'
budget: 300000 tokens
