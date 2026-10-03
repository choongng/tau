+++
id = "000086-pursuit"
ordinal = 86
kind = "pursuit"
timestamp = "2026-10-03T13:03:53+00:00"
summary = "pursuit open T0033: R03 fix: pursuit_found repairs mechanical problems instead of refusing, and the repeat breaker quotes the earlier result"
metric_command = ""
drains = []
hooks = []
+++

criteria: pursuit_found no longer refuses for mechanical problems it can fix itself: a setup::/scaffolding first milestone is dropped and an over-long milestone title is shortened, and the result says what was changed. The repeat breaker's refusal quotes the head of the earlier result (what to change) instead of only 'use the result you already have'.
decided by: sh -c 'echo "947dfeb8456476d5f44c36903af4bb7be8c426738b0a313a02506889867be002  .beagle/checks/T0033/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0033/check.sh'
budget: 120000 tokens
