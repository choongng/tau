+++
id = "001286-pursuit"
ordinal = 1286
kind = "pursuit"
timestamp = "2026-10-09T21:09:56+00:00"
summary = "pursuit open T0309: R36 fix: the source-quote check reads a quote in parentheses after a file:line label, and its verdict shows what it searched"
metric_command = ""
drains = []
hooks = []
+++

criteria: A known-answer case's source written as a file:line label followed by a verbatim quote in parentheses or brackets (as R36's W2-W4 wrote them) counts as quoting the reference: _QUOTE_MARKS reads ( ) and [ ] spans, and _quotes_reference strips a leading file:line label before matching; _quoted_context finds the same quote for the narrow-result check. A bare file:line label with no quoted text is still flagged (R36's first verdict on W1's sources stays correct). The 'no source quoting' verdict names, for each flagged case, the source string it searched, so a driver can see why. Keyed on structure, no prompt-domain words; R36's final tests/cases.json sources (copied into the test as a fixture) pass the quote check.
decided by: sh -c 'echo "3dfd10fc0dec3e1ec8345b1d05fdaf913edb25337e991993a250310ee53048c4  .beagle/checks/T0309/T0309.sh" | sha256sum -c --quiet && bash .beagle/checks/T0309/T0309.sh'
budget: 120000 tokens
