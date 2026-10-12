+++
id = "001996-pursuit"
ordinal = 1996
kind = "pursuit"
timestamp = "2026-10-12T07:00:42+00:00"
summary = "pursuit prove T0420: WITNESSED — refuses when R54.md is absent"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "cc196144c5006da97c6be6cda98915c1ca22cd50170e903a806e9cd0550b9301  .beagle/checks/T0420/T0420.sh" | sha256sum -c --quiet && bash .beagle/checks/T0420/T0420.sh'
refutes: refuses when R54.md is absent (proven 2026-10-12T06:59:41+00:00)
refused after 0s of a 0s check
standing checks red: T0335, T0336, T0360, T0368, T0386
