+++
id = "002161-pursuit"
ordinal = 2161
kind = "pursuit"
timestamp = "2026-10-12T09:34:27+00:00"
summary = "pursuit open T0459: Drop-import brief skips a task whose criteria name the import (R55)"
metric_command = ""
drains = []
hooks = []
+++

criteria: The drop-import brief is skipped when the task's title or criteria name the module (R55). Named test test_drop_import_brief_skips_a_task_whose_criteria_name_the_import passes; suite and ruff pass.
decided by: sh -c 'echo "08bad4268f729b454bd51a8cb04815dd25a190b852ba98836cd1db93a37c2a67  .beagle/checks/T0459/T0459.sh" | sha256sum -c --quiet && bash .beagle/checks/T0459/T0459.sh'
budget: 150000 tokens
