+++
id = "001542-pursuit"
ordinal = 1542
kind = "pursuit"
timestamp = "2026-10-10T05:22:26+00:00"
summary = "pursuit open T0363: Reference lookup through tilth"
metric_command = ""
drains = []
hooks = []
+++

criteria: A worker or driver can search references/*.txt for words and get numbered lines back: tilth "<words>" --scope references when tilth is on PATH, else grep -n. The references brief (QUOTED_SOURCE_NOTE / _references_brief) gives that command; the reread refusal on a references file offers the search instead of paging; _unanswered_case_note says how to search for the result lines. Domain-free. Tests test_references_brief_says_how_to_search_references, test_reread_refusal_on_reference_offers_search, test_unanswered_case_note_says_how_to_search; whole file passes, ruff clean.
decided by: sh -c 'echo "a4268e5f3f91e98a08ab0769601d84a087d8a47ebf43a68b75ca1658dc027cb4  .beagle/checks/T0363/T0363.sh" | sha256sum -c --quiet && bash .beagle/checks/T0363/T0363.sh'
budget: 80000 tokens
