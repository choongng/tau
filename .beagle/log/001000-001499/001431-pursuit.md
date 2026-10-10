+++
id = "001431-pursuit"
ordinal = 1431
kind = "pursuit"
timestamp = "2026-10-10T02:30:08+00:00"
summary = "pursuit prove T0128: WITNESSED — refuses when scored.sh's `assert model == os.environ[\"WANT_MODEL\"], f\"met…` is put back as `assert True or model == os.environ[\"WANT_MODEL\"…`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "b9d6e10eb58348c2d54c59f43734c099bba3175900c93317e11318a4ca610bc1  .beagle/checks/T0128/T0128.sh" | sha256sum -c --quiet && bash .beagle/checks/T0128/T0128.sh'
refutes: refuses when scored.sh's `assert model == os.environ["WANT_MODEL"], f"met…` is put back as `assert True or model == os.environ["WANT_MODEL"…` (proven 2026-10-10T02:30:08+00:00; refused at FAIL wrong model: wanted refuse, got pass)
refused after 1s of a 1s check at: FAIL wrong model: wanted refuse, got pass
refused with: selftest: 1 failed
