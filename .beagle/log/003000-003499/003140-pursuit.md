+++
id = "003140-pursuit"
ordinal = 3140
kind = "pursuit"
timestamp = "2026-10-14T22:09:23+00:00"
summary = "pursuit prove T0603: WITNESSED — refuses when beagle.py's `TAU_HOST_NOTE = \"\"\"\\` is put back as `TAU_HOST_NOTE = \"\"\"whatever its status \\`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "abc63bac1db337c7b5f58d0c980458569d56e959c298397d8f7db5b4ee4f2a19  .beagle/checks/T0603/T0603.sh" | sha256sum -c --quiet && bash .beagle/checks/T0603/T0603.sh'
refutes: refuses when beagle.py's `TAU_HOST_NOTE = """\` is put back as `TAU_HOST_NOTE = """whatever its status \` (proven 2026-10-14T22:09:23+00:00; refused at deleted, but still in the extension: whatever its status)
refused after 0s of a 3m10s check at: deleted, but still in the extension: whatever its status
refused with: deleted, but still in the extension: whatever its status
