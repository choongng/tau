+++
id = "000744-pursuit"
ordinal = 744
kind = "pursuit"
timestamp = "2026-10-04T16:46:18+00:00"
summary = "pursuit open T0172: Scope refusal of project code does not point to /tmp"
metric_command = ""
drains = []
hooks = []
+++

criteria: A worker's write refused as outside its task's scope no longer says scratch files go in /tmp when the target is project code; it says work outside the scope is lost and to report the file as needed, and when the refused file is the module the task's check imports, it says the check cannot pass without it.
decided by: sh -c 'echo "0256985607393205445e8803d75719bb5ba90c13eb995856342ed54e2303ba8e  .beagle/checks/T0172/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0172/check.sh'
budget: 20000 tokens
