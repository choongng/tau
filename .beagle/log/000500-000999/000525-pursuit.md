+++
id = "000525-pursuit"
ordinal = 525
kind = "pursuit"
timestamp = "2026-10-04T04:53:48+00:00"
summary = "pursuit open T0129: _changed_files drops the first character of the first path"
metric_command = ""
drains = []
hooks = []
+++

criteria: _changed_files returns every changed or new path whole, including a first line that is an unstaged modification (' M path'), a rename, and a path with spaces; beagle's record and caches are still left out.
decided by: sh -c 'echo "bd597bf3871f69b5b94ff5ae789290c1f56c651d74a999d8db1c01c6f3fbc3ba  .beagle/checks/T0129/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0129/check.sh'
budget: 40000 tokens
