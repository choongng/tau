+++
id = "002718-pursuit"
ordinal = 2718
kind = "pursuit"
timestamp = "2026-10-13T19:14:22+00:00"
summary = "pursuit open T0533: bare-goal prompt, hidden grader and launch.sh task"
metric_command = ""
drains = []
hooks = []
+++

criteria: A bare-goal task 'semver' exists: ~/tautest/semver_prompt.txt asks, in the other prompts' form but with no spec or link, for a modern Python library that parses, validates and compares semantic versions; grade_semver.py (hidden, >=40 cases against Semantic Versioning 2.0.0: parse, validity, precedence incl. prerelease and build) passes adapters/semver_reference.py and fails each SEMVER_TRAP of adapters/semver_broken.py; launch.sh takes 'semver' for pursuit and baseline runs
decided by: sh -c 'echo "d54b9081f18886fc91c313d4c9b9bdb749a1cc214d4a95ae4d4f369cacb1690f  .beagle/checks/T0533/T0533.sh" | sha256sum -c --quiet && bash .beagle/checks/T0533/T0533.sh'
budget: 150000 tokens
