+++
id = "002387-pursuit"
ordinal = 2387
kind = "pursuit"
timestamp = "2026-10-12T14:25:28+00:00"
summary = "pursuit prove T0467: WITNESSED — refuses when beagle.py's `and not _judge_kept_open(task, root):` is put back as `:`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "710605bb253c14579d62c74d30178b3592f3395f82fb3071674ce1e91c32880b  .beagle/checks/T0467/T0467.sh" | sha256sum -c --quiet && bash .beagle/checks/T0467/T0467.sh'
refutes: refuses when beagle.py's `and not _judge_kept_open(task, root):` is put back as `:` (proven 2026-10-12T14:25:27+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_new_route_held_at_close_sends_its_notes_to_a_worker)
refused after 4s of a 2m45s check at: FAILED tests/test_beagle_example_extension.py::test_new_route_held_at_close_sends_its_notes_to_a_worker
refused with: 1 failed, 816 deselected in 3.21s
