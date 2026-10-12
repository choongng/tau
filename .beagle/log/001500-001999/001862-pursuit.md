+++
id = "001862-pursuit"
ordinal = 1862
kind = "pursuit"
timestamp = "2026-10-12T00:44:07+00:00"
summary = "pursuit prove T0446: WITNESSED — refuses when beagle.py's `KILLED_WORDS_CHARS = 600` is put back as `KILLED_WORDS_CHARS = 2000`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "06d0b702cc0d5a57b21d9826b10792eb4057c7fd542655f58847db7e3e75c018  .beagle/checks/T0446/T0446.sh" | sha256sum -c --quiet && bash .beagle/checks/T0446/T0446.sh'
refutes: refuses when beagle.py's `KILLED_WORDS_CHARS = 600` is put back as `KILLED_WORDS_CHARS = 2000` (proven 2026-10-12T00:44:06+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_wall_kill_step_result_shows_the_killed_workers_last_words)
refused after 10s of a 2m47s check at: FAILED tests/test_beagle_example_extension.py::test_wall_kill_step_result_shows_the_killed_workers_last_words
refused with: 1 failed, 1 passed, 777 deselected in 9.56s
