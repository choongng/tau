+++
id = "000712-pursuit"
ordinal = 712
kind = "pursuit"
timestamp = "2026-10-04T14:18:50+00:00"
summary = "pursuit prove T0167: WITNESSED — refuses when beagle.py's `kept, fold_notes = _fold_design_milestones(kept)` is put back as `fold_notes = []`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "2cedd2c99bc400c549aeaeb75e87ea5f1bc4f3059380a6453358ab4a88a9eb1e  .beagle/checks/T0167/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0167/check.sh'
refutes: refuses when beagle.py's `kept, fold_notes = _fold_design_milestones(kept)` is put back as `fold_notes = []` (proven 2026-10-04T14:18:22+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_founding_folds_a_design_milestone_into_the_next_when_known_answers_…)
refused after 2s of a 1m00s check at: FAILED tests/test_beagle_example_extension.py::test_founding_folds_a_design_milestone_into_the_next_when_known_answers_…
refused with: 1 failed in 1.54s
