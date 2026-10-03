+++
id = "000026-pursuit"
ordinal = 26
kind = "pursuit"
timestamp = "2026-10-03T11:00:12+00:00"
summary = "pursuit amend T0019"
metric_command = ""
drains = []
hooks = []
+++

dry-run used R01/R02, which real runs now occupy, so the launcher rightly refuses; dry-run ids moved to R98/R99 that no run will use
was: sh -c 'echo "3a28c8d0249cdabe922453391482fb6628dd51634f770ff284cd8d552dcbfac4  .beagle/checks/T0019/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0019/check.sh'
  3a28c8d0249cdabe922453391482fb6628dd51634f770ff284cd8d552dcbfac4  .beagle/checks/T0019/check.sh
now: sh -c 'echo "0662620b8fe7f816dd1ebf2931bf6b14bb4a80a9c92e29453b48577616efb8de  .beagle/checks/T0019/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0019/check.sh'
