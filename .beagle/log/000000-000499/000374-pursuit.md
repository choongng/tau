+++
id = "000374-pursuit"
ordinal = 374
kind = "pursuit"
timestamp = "2026-10-03T21:16:12+00:00"
summary = "pursuit open T0086: setup commit failure unstages only what founding staged"
metric_command = ""
drains = []
hooks = []
+++

criteria: _commit_setup records the index's cached paths (git diff --cached --name-only) before its git add, and on a failed commit resets only the paths it newly staged; a path the user had staged before founding (e.g. a .gitignore change) stays staged. The existing empty-index test still passes; one named test pins the pre-staged case.
decided by: sh -c 'echo "bba9d5ef5049333297e51238e0b366313867a3720454c34bb73d4c42b216c5f3  .beagle/checks/T0086/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0086/check.sh'
budget: 15000 tokens
