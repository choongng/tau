+++
id = "003126-pursuit"
ordinal = 3126
kind = "pursuit"
timestamp = "2026-10-14T21:05:33+00:00"
summary = "pursuit prove T0602: WITNESSED — refuses when beagle.py's `argv.append(\"--isolated\")` is put back as `pass`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "dbc7bb693facefd3c29c17d809b45fb5e9c21160f3495b392cc019de8d90b7c4  .beagle/checks/T0602/T0602.sh" | sha256sum -c --quiet && bash .beagle/checks/T0602/T0602.sh'
refutes: refuses when beagle.py's `argv.append("--isolated")` is put back as `pass` (proven 2026-10-14T21:05:32+00:00; refused at tests/test_beagle_example_extension.py -k json_out and next -> 1 passed, 702 deselected in 0.55s)
refused after 2s of a 2m59s check at: tests/test_beagle_example_extension.py -k json_out and next -> 1 passed, 702 deselected in 0.55s
refused with: tests/test_beagle_example_extension.py -k json_out and next -> 1 passed, 702 deselected in 0.55s
