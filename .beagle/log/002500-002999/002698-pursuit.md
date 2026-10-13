+++
id = "002698-pursuit"
ordinal = 2698
kind = "pursuit"
timestamp = "2026-10-13T15:02:56+00:00"
summary = "pursuit open T0529: Brief: write the code and run it before tracing a case by hand"
metric_command = ""
drains = []
hooks = []
+++

criteria: The worker brief's working habits say to write the code and run it before tracing a case by hand
decided by: sh -c 'echo "a29de8f9a25c56b35b44dd4225cf419c5c1f238a311dc508bc17631650f4a1e8  .beagle/checks/T0529/T0529.sh" | sha256sum -c --quiet && bash .beagle/checks/T0529/T0529.sh'
budget: 30000 tokens
opened over T0493, T0517: 2db46f63d586c45fc3208987a75babd73f0d4fde
