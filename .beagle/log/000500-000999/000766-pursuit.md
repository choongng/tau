+++
id = "000766-pursuit"
ordinal = 766
kind = "pursuit"
timestamp = "2026-10-04T21:53:21+00:00"
summary = "pursuit prove T0177: WITNESSED — refuses when scored.sh's `assert task == os.environ[\"WANT_TASK\"]` is put back as `assert True or task == os.environ[\"WANT_TASK\"]`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "0700f47f7309612bd7c2fc14ecd0f6eced3eb99770a50834abc1dfc16407e13c  .beagle/checks/T0177/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0177/check.sh'
refutes: refuses when scored.sh's `assert task == os.environ["WANT_TASK"]` is put back as `assert True or task == os.environ["WANT_TASK"]` (proven 2026-10-04T21:52:24+00:00; refused at FAIL wrong task: wanted refuse, got pass)
refused after 1s of a 1s check at: FAIL wrong task: wanted refuse, got pass
refused with: selftest: 2 failed
