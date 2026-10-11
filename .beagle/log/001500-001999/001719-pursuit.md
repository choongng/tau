+++
id = "001719-pursuit"
ordinal = 1719
kind = "pursuit"
timestamp = "2026-10-11T00:21:58+00:00"
summary = "pursuit open T0401: Audit 14 fix: every _scope_has_data caller sees data under a directory scope"
metric_command = ""
drains = []
hooks = []
+++

criteria: Every _scope_has_data caller in beagle.py that has the project root in reach passes it, so a directory scope entry such as ['tests/'] that holds cases data on disk reads as holding data on every route that asks (audit 14: ten callers near 7778, 7951, 8027, 8111, 8896, 9569, 9617, 13458, 13559, 13590 passed no root). A caller with no root in reach is unchanged. Tests test_directory_scope_data_reaches_every_scope_has_data_route (through at least one of those routes) and the existing test_data_test_unwritten_import_on_a_directory_scope; whole file passes, ruff clean.
decided by: sh -c 'echo "99725eb7ae8820ec278d7383e9ed4e35ab2cdb4ce1d89a758e8f963864a07dcf  .beagle/checks/T0401/T0401.sh" | sha256sum -c --quiet && bash .beagle/checks/T0401/T0401.sh'
budget: 70000 tokens
