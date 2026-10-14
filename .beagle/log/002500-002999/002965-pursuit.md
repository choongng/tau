+++
id = "002965-pursuit"
ordinal = 2965
kind = "pursuit"
timestamp = "2026-10-14T03:38:25+00:00"
summary = "pursuit open T0568: tau: workers may run read-only beagle contract verbs and --help (S01 #2)"
metric_command = ""
drains = []
hooks = []
+++

criteria: A worker's bash command guard lets through any beagle command ending in or containing --help/-h, beagle doctor, and the read-only contract verbs (status, refs, check, run, show/view if they exist) — the set read from beagle's CLI, not guessed — while mutating verbs (pursuit open/close/amend/prove, contract seal/retire, gate changes) stay refused with the existing note; contract add stays allowed where it is today. Tests worker_runs_help_and_read_only_verbs and worker_mutating_beagle_refused pass; suite green outside beagle's venv.
decided by: sh -c 'echo "974ca3bcd698ecadc71f0421d87883550ec4b452e06ca97eba93fc611e658885  .beagle/checks/T0568/T0568.sh" | sha256sum -c --quiet && bash .beagle/checks/T0568/T0568.sh'
budget: 70000 tokens
