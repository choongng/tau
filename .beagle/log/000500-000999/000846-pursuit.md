+++
id = "000846-pursuit"
ordinal = 846
kind = "pursuit"
timestamp = "2026-10-05T02:14:35+00:00"
summary = "pursuit open T0215: Scope given as an absolute path matches git's relative paths"
metric_command = ""
drains = []
hooks = []
+++

criteria: A pursuit_step open/amend/new_route given a scope entry as an absolute path under the project root stores and matches it root-relative, so the task's new file is in scope for prove, the guard and commit; an absolute path outside the root is refused with a message naming the root-relative form; a relative scope behaves as before.
decided by: sh -c 'echo "900d6a72355d3dd0e3a058235c8cfd7db86416fe7c68a8289e9764153b947b13  .beagle/checks/T0215/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0215/check.sh'
budget: 70000 tokens
