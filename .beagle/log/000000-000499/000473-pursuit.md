+++
id = "000473-pursuit"
ordinal = 473
kind = "pursuit"
timestamp = "2026-10-04T02:52:38+00:00"
summary = "pursuit open T0120: Refuse deliverables scoped under references/"
metric_command = ""
drains = []
hooks = []
+++

criteria: pursuit_step refuses a scope path under references/ (REFERENCES_DIR, which tau git-ignores at founding), naming the path and pointing to docs/ (e.g. docs/NOTES.md); the same task scoped to docs/NOTES.md opens.
decided by: sh -c 'echo "87143fc88d31d4e0df3c47b4118eba7d974a022b83d33796ded1c82f34b8ba6f  .beagle/checks/T0120/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0120/check.sh'
budget: 80000 tokens
