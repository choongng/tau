+++
id = "002908-pursuit"
ordinal = 2908
kind = "pursuit"
timestamp = "2026-10-14T01:51:52+00:00"
summary = "pursuit amend T0564"
metric_command = ""
drains = []
hooks = []
+++

v2's pattern still missed pytest's '10 passed, 2593 deselected in' (the comma); v3 accepts that and still rejects any line led by failures; run directly: exits 0
was: sh -c 'echo "ed209ec05bf9aa5c35c1381ddafbc092c32103b8f0d158a2fc71690526de6707  .beagle/checks/T0564/T0564.v2.sh" | sha256sum -c --quiet && bash .beagle/checks/T0564/T0564.v2.sh'
  ed209ec05bf9aa5c35c1381ddafbc092c32103b8f0d158a2fc71690526de6707  .beagle/checks/T0564/T0564.v2.sh
now: sh -c 'echo "536762806de7cff2cb95d361c9340fcca80e6b9c3e46a9320d47a206d57682fa  .beagle/checks/T0564/T0564.v3.sh" | sha256sum -c --quiet && bash .beagle/checks/T0564/T0564.v3.sh'
