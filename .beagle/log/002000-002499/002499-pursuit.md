+++
id = "002499-pursuit"
ordinal = 2499
kind = "pursuit"
timestamp = "2026-10-12T16:48:57+00:00"
summary = "pursuit open T0495: beagle: a [contract] files entry may be a directory"
metric_command = ""
drains = []
hooks = []
+++

criteria: A [contract] files entry naming a directory seals every file under it (git's view, tracked or untracked and not ignored, else every file), less build leavings such as __pycache__; a file added under it since the seal reads as altered; contract-guard refuses edits under it outside contract work; the acceptance check refuses a directory holding no test besides the extractions. Both named tests pass, as does the whole of test_contract.py.
decided by: sh -c 'echo "91b033d39860d69a2f75bca5911beb97cda4718e952cca8d7c84ffcd48ec091a  .beagle/checks/T0495/T0495.sh" | sha256sum -c --quiet && bash .beagle/checks/T0495/T0495.sh'
budget: 60000 tokens
