+++
id = "002136-pursuit"
ordinal = 2136
kind = "pursuit"
timestamp = "2026-10-12T09:17:53+00:00"
summary = "pursuit open T0457: Prove: a witness outside the task's scope does not pre-empt the absence proof of its own file; the retry asks no write the scope refuses (R54)"
metric_command = ""
drains = []
hooks = []
+++

criteria: Prove lets no witness outside the scope pre-empt the absence of the task's own file, and its not-proven retry asks for no test when the scope has none (R54). Its two named tests pass; suite and ruff pass.
decided by: sh -c 'echo "112e8eb6cc5ac03096ba09df8985fc9263afb1e302d52676c3f3b2ad3197f9ac  .beagle/checks/T0457/T0457.sh" | sha256sum -c --quiet && bash .beagle/checks/T0457/T0457.sh'
budget: 150000 tokens
