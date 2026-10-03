+++
id = "000078-pursuit"
ordinal = 78
kind = "pursuit"
timestamp = "2026-10-03T13:02:50+00:00"
summary = "pursuit amend T0036"
metric_command = ""
drains = []
hooks = []
+++

catalog walk read model ids from the wrong key (model_metadata is keyed by model name)
was: sh -c 'echo "d9ed3d4ad4b3a8f8cb4e6834f001e7f41f1bb8cb3581e9886c15c8094270e5e7  .beagle/checks/T0036/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0036/check.sh'
  d9ed3d4ad4b3a8f8cb4e6834f001e7f41f1bb8cb3581e9886c15c8094270e5e7  .beagle/checks/T0036/check.sh
now: sh -c 'echo "61f8d2b6d07d1b3d90d30bc15d13dda5edeee787b714ebe416c88c2465804856  .beagle/checks/T0036/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0036/check.sh'
