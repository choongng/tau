+++
id = "000608-pursuit"
ordinal = 608
kind = "pursuit"
timestamp = "2026-10-04T09:08:14+00:00"
summary = "pursuit open T0145: Check judge: uv run python, pytest in strings, sys.exit without a comparison"
metric_command = ""
drains = []
hooks = []
+++

criteria: A check run as 'uv run python -c ...' (or python3 -m with -c under any runner prefix: uv run, poetry run, pipenv run) with no assert, no comparison and no raise is refused like 'python -c'; naming pytest or unittest only inside a string literal does not exempt the code; sys.exit of a call or name with no comparison does not count as judging.
decided by: sh -c 'echo "9f972080f3a728ae47ad11e24c94e14a430979ebf2bc1afab1036faa63aa6c29  .beagle/checks/T0145/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0145/check.sh'
budget: 50000 tokens
