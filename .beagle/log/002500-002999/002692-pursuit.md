+++
id = "002692-pursuit"
ordinal = 2692
kind = "pursuit"
timestamp = "2026-10-13T08:16:44+00:00"
summary = "pursuit prove T0526: WITNESSED — refuses when contract.py's `files = not self.ident.startswith(\"$ \") or not …` is put back as `files = False`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "9e100dd5258ff15fb85814eecb8f1ae49c861f44479fab470a61143808b85477  .beagle/checks/T0526/T0526.sh" | sha256sum -c --quiet && bash .beagle/checks/T0526/T0526.sh'
refutes: refuses when contract.py's `files = not self.ident.startswith("$ ") or not …` is put back as `files = False` (proven 2026-10-13T08:15:44+00:00; refused at 1 failed, 1 passed, 53 deselected in 0.42s)
refused after 1s of a 1s check at: 1 failed, 1 passed, 53 deselected in 0.42s
refused with: 1 failed, 1 passed, 53 deselected in 0.42s
