+++
id = "000384-pursuit"
ordinal = 384
kind = "pursuit"
timestamp = "2026-10-03T21:21:20+00:00"
summary = "pursuit open T0089: directory scope walk skips cache directories"
metric_command = ""
drains = []
hooks = []
+++

criteria: _scope_dir_files skips .pytest_cache, .ruff_cache, .mypy_cache (and any directory whose name ends in _cache or is .tox/.nox), so a file in one under a scope directory does not count as unlocked data in _oracle_with_code_problem. One named test: a scope dir holding src/x.py and .pytest_cache/v/cache/lastfailed lists only src/x.py.
decided by: sh -c 'echo "01b7531aebef9b4d276e4a09d115cf12323afdf64dd482c21c65d25f0eb6829b  .beagle/checks/T0089/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0089/check.sh'
budget: 10000 tokens
