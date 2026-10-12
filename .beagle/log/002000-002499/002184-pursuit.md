+++
id = "002184-pursuit"
ordinal = 2184
kind = "pursuit"
timestamp = "2026-10-12T09:37:16+00:00"
summary = "pursuit prove T0459: WITNESSED — refuses when beagle.py's `if re.search(rf\"(?<![\\w.]){re.escape(module)}(?…` is put back as `if False:`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "08bad4268f729b454bd51a8cb04815dd25a190b852ba98836cd1db93a37c2a67  .beagle/checks/T0459/T0459.sh" | sha256sum -c --quiet && bash .beagle/checks/T0459/T0459.sh'
refutes: refuses when beagle.py's `if re.search(rf"(?<![\w.]){re.escape(module)}(?…` is put back as `if False:` (proven 2026-10-12T09:37:15+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_drop_import_brief_skips_a_task_whose_criteria_name_the_import)
refused after 4s of a 2m43s check at: FAILED tests/test_beagle_example_extension.py::test_drop_import_brief_skips_a_task_whose_criteria_name_the_import
refused with: 1 failed, 807 deselected in 3.94s
