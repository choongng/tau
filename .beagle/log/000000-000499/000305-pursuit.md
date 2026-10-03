+++
id = "000305-pursuit"
ordinal = 305
kind = "pursuit"
timestamp = "2026-10-03T20:16:05+00:00"
summary = "pursuit prove T0072: WITNESSED — refuses when beagle.py's `if intent and _BARE_LABEL.fullmatch(title):` is put back as `if False and intent and _BARE_LABEL.fullmatch(t…`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "1176926bca2c74510ff4c2ef05e291223decae471a8f68c35e65a93b6eb99616  .beagle/checks/T0072/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0072/check.sh'
refutes: refuses when beagle.py's `if intent and _BARE_LABEL.fullmatch(title):` is put back as `if False and intent and _BARE_LABEL.fullmatch(t…` (proven 2026-10-03T20:15:30+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_founding_milestone_with_a_bare_label_takes_its_title_from_the_int
refused after 1s of a 1s check at: FAILED tests/test_beagle_example_extension.py::test_founding_milestone_with_a_bare_label_takes_its_title_from_the_intent
refused with: 2 failed, 1 passed, 275 deselected in 0.67s
