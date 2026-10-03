+++
id = "000217-pursuit"
ordinal = 217
kind = "pursuit"
timestamp = "2026-10-03T18:31:18+00:00"
summary = "pursuit open T0062: founding commits beagle init config and .gitignore"
metric_command = ""
drains = []
hooks = []
+++

criteria: After a successful pursuit_found (goal written, root and milestones added), tau commits beagle's setup as one commit: every untracked or changed path under .beagle/ that git does not ignore, plus .gitignore — and nothing else (other untracked or modified project files stay as they were, and the index holds nothing else afterwards). In a fresh directory where beagle init ran, git status --porcelain is empty after founding (R08: workspace-clean was red from T0002 because .beagle/*.toml, memory-rubric.md and .gitignore stayed untracked). With no git identity, or when the commit fails, founding still succeeds and the result says the setup is uncommitted.
decided by: sh -c 'echo "7a6f6fe81562630de3e2484a36bdafdd8a74dd2f1fd753c408b8f73d44f93a59  .beagle/checks/T0062/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0062/check.sh'
budget: 50000 tokens
