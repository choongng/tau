+++
id = "000293-pursuit"
ordinal = 293
kind = "pursuit"
timestamp = "2026-10-03T20:10:01+00:00"
summary = "pursuit prove T0071: WITNESSED — refuses when beagle.py's `text = _fetch_reference(url, timeout=REFERENCE_…` is put back as `text = _fetch_reference(url)`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "94aee8578df906438ae0480c9878034305d17d51e740e0162583edd886ac041c  .beagle/checks/T0071/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0071/check.sh'
refutes: refuses when beagle.py's `text = _fetch_reference(url, timeout=REFERENCE_…` is put back as `text = _fetch_reference(url)` (proven 2026-10-03T20:09:27+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_reference_fetch_retries_a_timeout_with_a_longer_timeout)
refused after 1s of a 1s check at: FAILED tests/test_beagle_example_extension.py::test_reference_fetch_retries_a_timeout_with_a_longer_timeout
refused with: 1 failed, 1 passed, 271 deselected in 0.42s
