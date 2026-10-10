+++
id = "001543-pursuit"
ordinal = 1543
kind = "pursuit"
timestamp = "2026-10-10T14:39:30+00:00"
summary = "pursuit prove T0363: WITNESSED — refuses when beagle.py's `parts.append(f\"{QUOTED_SOURCE_NOTE} {_reference…` is put back as `parts.append(QUOTED_SOURCE_NOTE or _reference_s…` and beagle.py's `f\"{note} To find {'more ' if candidates else ''…` is put back as `f\"{note}\" if note else f\"{note} To find li"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "a4268e5f3f91e98a08ab0769601d84a087d8a47ebf43a68b75ca1658dc027cb4  .beagle/checks/T0363/T0363.sh" | sha256sum -c --quiet && bash .beagle/checks/T0363/T0363.sh'
refutes: refuses when beagle.py's `parts.append(f"{QUOTED_SOURCE_NOTE} {_reference…` is put back as `parts.append(QUOTED_SOURCE_NOTE or _reference_s…` and beagle.py's `f"{note} To find {'more ' if candidates else ''…` is put back as `f"{note}" if note else f"{note} To find lines t…` and beagle.py's `if root 
refused after 2s of a 1m46s check at: FAILED tests/test_beagle_example_extension.py::test_references_brief_says_how_to_search_references
refused with: 3 failed, 689 deselected in 1.22s
