+++
id = "000536-pursuit"
ordinal = 536
kind = "pursuit"
timestamp = "2026-10-04T05:24:27+00:00"
summary = "pursuit prove T0128: WITNESSED — refuses when scored.sh's `assert model == os.environ[\"WANT_MODEL\"], f\"met…` is put back as `pass`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "c713a4d05b3ad5d5c8f8cfa79a11e161e9dfdd4a2afdacaa5b28429899c16994  .beagle/checks/T0128/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0128/check.sh'
refutes: refuses when scored.sh's `assert model == os.environ["WANT_MODEL"], f"met…` is put back as `pass` (proven 2026-10-04T05:23:29+00:00; refused at FAIL wrong model: wanted refuse, got pass)
refused after 1s of a 1s check at: FAIL wrong model: wanted refuse, got pass
refused with: selftest: 1 failed
