+++
id = "002899-pursuit"
ordinal = 2899
kind = "pursuit"
timestamp = "2026-10-14T01:39:53+00:00"
summary = "pursuit prove T0493: WITNESSED — refuses when beagle.py's `TEST_DATA_SUFFIXES = frozenset({\".json\", \".toml…` is put back as `CASES_DATA_SUFFIXES = TEST_DATA_SUFFIXES = froz…`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "ac6351f861b897d930bd8f4dc2b7080871486fbff5515fef96a94946c431b69e  .beagle/checks/T0493/T0493.v2.sh" | sha256sum -c --quiet && bash .beagle/checks/T0493/T0493.v2.sh'
refutes: refuses when beagle.py's `TEST_DATA_SUFFIXES = frozenset({".json", ".toml…` is put back as `CASES_DATA_SUFFIXES = TEST_DATA_SUFFIXES = froz…` (proven 2026-10-14T01:39:52+00:00; refused at forbidden text present)
refused after 0s of a 2m45s check at: forbidden text present
refused with: forbidden text present
