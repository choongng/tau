+++
id = "000050-pursuit"
ordinal = 50
kind = "pursuit"
timestamp = "2026-10-03T12:24:08+00:00"
summary = "pursuit open T0027: R02 fix: references fetched at founding and carried in every worker brief"
metric_command = ""
drains = []
hooks = []
+++

criteria: After pursuit_found writes the goal, every http(s) URL in the user's original prompt is fetched once into references/ in the project as text (PDF via pdftotext -layout, HTML stripped to text); a failed fetch is noted, not fatal. Every pursuit_step worker brief names the reference files ('read first; outranks the driver's notes'), carries the user's original request verbatim, and heads the driver's notes 'From the driver (who has not read the reference)'.
decided by: sh -c 'echo "733f2b2c36f0e99f7630d239b332ec5ec7b1676ee7a0f1be5d7fa48d8562a9d1  .beagle/checks/T0027/named_tests.sh" | sha256sum -c --quiet && bash .beagle/checks/T0027/named_tests.sh tests/test_beagle_example_extension.py 3 test_found_fetches_references test_step_brief_carries_references_and_prompt test_found_reference_fetch_failure_is_noted'
budget: 150000 tokens
