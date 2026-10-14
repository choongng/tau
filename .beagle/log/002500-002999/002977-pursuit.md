+++
id = "002977-pursuit"
ordinal = 2977
kind = "pursuit"
timestamp = "2026-10-14T03:51:38+00:00"
summary = "pursuit open T0578: tau: drop T0493's leftover cases-first brief text (QUOTED_SOURCE_NOTE, the cases.json worked example)"
metric_command = ""
drains = []
hooks = []
+++

criteria: QUOTED_SOURCE_NOTE, _worked_example_note and every other brief text describing a cases file or its close-time source judge are gone from examples/extensions/beagle.py (grep for QUOTED_SOURCE_NOTE, _worked_example_note, cases.json, 'cases file' finds nothing); a data-file worker's brief still says what T0493 kept (references, how to cite); tests at :3371/:3397 updated to assert the absence; test data_task_brief_has_no_cases_first_text passes; suite green outside beagle's venv.
decided by: sh -c 'echo "5e2bf708dc444ba08294523cd890292acd9c0bc7df66b8ce1ca4fb7e09c42154  .beagle/checks/T0578/T0578.sh" | sha256sum -c --quiet && bash .beagle/checks/T0578/T0578.sh'
budget: 50000 tokens
opened over T0575, T0577, T0565, T0573: tau lane beside the beagle lane (T0569); audit defect, filed before more opens
