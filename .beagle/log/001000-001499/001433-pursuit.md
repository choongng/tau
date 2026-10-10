+++
id = "001433-pursuit"
ordinal = 1433
kind = "pursuit"
timestamp = "2026-10-10T02:32:04+00:00"
summary = "pursuit prove T0319: WITNESSED — refuses when T0054.sh's `if grep -q \"def test_founding_refuses_when_ever…` is put back as `! grep -q \"def test_founding_refuses_when_every…`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "559a1b62b9bd06ff4d92ff1cfe4c9339a03575679c8f9db00f338ff5b7ef1af4  .beagle/checks/T0319/T0319.sh" | sha256sum -c --quiet && bash .beagle/checks/T0319/T0319.sh'
refutes: refuses when T0054.sh's `if grep -q "def test_founding_refuses_when_ever…` is put back as `! grep -q "def test_founding_refuses_when_every…` (proven 2026-10-10T02:32:04+00:00; refused at Traceback (most recent call last):)
refused after 0s of a 1m43s check at: Traceback (most recent call last):
refused with: AssertionError: bound checks with a '! cmd' line: .beagle/checks/T0054/T0054.sh
