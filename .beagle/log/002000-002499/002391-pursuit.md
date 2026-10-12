+++
id = "002391-pursuit"
ordinal = 2391
kind = "pursuit"
timestamp = "2026-10-12T14:25:56+00:00"
summary = "pursuit open T0468: The reasoning loop cut catches a sentence group repeated within one line (R58)"
metric_command = ""
drains = []
hooks = []
+++

criteria: The reasoning loop detector cuts a sentence group repeated past the threshold within one line (R58: 193 repeats on one 67,301-char line), and long non-repeating prose is not cut. Named test test_sentences_repeated_within_one_line_are_cut passes; the session tests and ruff pass.
decided by: sh -c 'echo "65fb4304de318643623e45894a936a0cb8cacbde43ab0c093b20c6f82d5921a6  .beagle/checks/T0468/T0468.sh" | sha256sum -c --quiet && bash .beagle/checks/T0468/T0468.sh'
budget: 150000 tokens
