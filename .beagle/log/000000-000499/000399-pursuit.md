+++
id = "000399-pursuit"
ordinal = 399
kind = "pursuit"
timestamp = "2026-10-04T00:38:38+00:00"
summary = "pursuit prove T0091: WITNESSED — refuses when scored.sh's `assert m.get(\"tau_dirty_files\") == 0,` is put back as `assert True,`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "cb4c093f0b8ca5555598fafd60652abfe6d272a516e3968736dbe2554bf98bf8  .beagle/checks/T0091/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0091/check.sh'
refutes: refuses when scored.sh's `assert m.get("tau_dirty_files") == 0,` is put back as `assert True,` (proven 2026-10-04T00:37:52+00:00; refused at FAIL dirty tau: wanted refuse, got pass)
refused after 1s of a 0s check at: FAIL dirty tau: wanted refuse, got pass
refused with: selftest: 1 failed
