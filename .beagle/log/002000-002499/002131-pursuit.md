+++
id = "002131-pursuit"
ordinal = 2131
kind = "pursuit"
timestamp = "2026-10-12T09:14:37+00:00"
summary = "pursuit open T0456: Locked-test binding refusal's advice never names the call it refused (R54)"
metric_command = ""
drains = []
hooks = []
+++

criteria: The locked-test refusal for a lint check offers a scope without the judged module (R54). Named test passes; suite and ruff pass.
decided by: sh -c 'echo "2a984a64a85225afd666a8f3d1b53197a8a6e4cc058ca013f22f0fd37b188450  .beagle/checks/T0456/T0456.sh" | sha256sum -c --quiet && bash .beagle/checks/T0456/T0456.sh'
budget: 150000 tokens
