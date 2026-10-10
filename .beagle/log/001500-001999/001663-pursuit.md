+++
id = "001663-pursuit"
ordinal = 1663
kind = "pursuit"
timestamp = "2026-10-10T23:07:23+00:00"
summary = "pursuit open T0389: R44 fix: the unwritten-import hint applies to a directory scope"
metric_command = ""
drains = []
hooks = []
+++

criteria: _scope_has_data counts a cases data file under a directory scope entry (e.g. ['tests/']), so a step whose scope is a directory holding the cases data gets the same unwritten-import result (_data_test_unwritten_import: names the import, notes-only Next) as one listing the files. A directory with no data file is unchanged. Structural, no domain words. Tests test_data_test_unwritten_import_on_a_directory_scope, test_scope_has_data_counts_a_data_file_under_a_directory_entry; whole file passes, ruff clean.
decided by: sh -c 'echo "7e5d9d7ed0d32e2561dae0c9bf0dc6cbf4a3083ec6a874a74588d84d356c32f0  .beagle/checks/T0389/T0389.sh" | sha256sum -c --quiet && bash .beagle/checks/T0389/T0389.sh'
budget: 60000 tokens
