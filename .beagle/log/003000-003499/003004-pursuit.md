+++
id = "003004-pursuit"
ordinal = 3004
kind = "pursuit"
timestamp = "2026-10-14T04:20:30+00:00"
summary = "pursuit prove T0533: WITNESSED — refuses when semver_prompt.txt's `implement a modern python library for parsing, …` is put back as `implement a modern python library for parsing, …`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "0966c6b38026d385016ab7a62350de73f633dc6133ec9886f713a08050e6cf8f  .beagle/checks/T0533/T0533.v2.sh" | sha256sum -c --quiet && bash .beagle/checks/T0533/T0533.v2.sh'
refutes: refuses when semver_prompt.txt's `implement a modern python library for parsing, …` is put back as `implement a modern python library for parsing, …` (proven 2026-10-14T04:20:30+00:00; refused at the semver prompt names a link or semver.org)
refused after 0s of a 2s check at: the semver prompt names a link or semver.org
refused with: the semver prompt names a link or semver.org
