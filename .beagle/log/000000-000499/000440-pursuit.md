+++
id = "000440-pursuit"
ordinal = 440
kind = "pursuit"
timestamp = "2026-10-04T02:01:13+00:00"
summary = "pursuit prove T0112: WITNESSED — refuses when beagle.py's `uncommitted_note = _commit_before_split(root, t…` is put back as `uncommitted_note = _uncommitted_note(task, unco…`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "3638c570b54cf98a900ba28940d82cc10736a04b9dfd35747f2aec17b8edcfe6  .beagle/checks/T0112/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0112/check.sh'
refutes: refuses when beagle.py's `uncommitted_note = _commit_before_split(root, t…` is put back as `uncommitted_note = _uncommitted_note(task, unco…` (proven 2026-10-04T02:00:25+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_split_commits_passing_uncommitted_work_before_the_parts)
refused after 1s of a 30s check at: FAILED tests/test_beagle_example_extension.py::test_split_commits_passing_uncommitted_work_before_the_parts
refused with: 1 failed in 0.56s
replaces: refuses when beagle.py's `uncommitted_note = _commit_before_split(root, t…` is put back as `uncommitted_note = _uncommitted_note(uncommitte…` (proven 2026-10-04T01:59:02+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_split_commits_passing_uncommitted_work_before_the_parts)
