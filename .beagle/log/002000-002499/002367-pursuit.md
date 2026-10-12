+++
id = "002367-pursuit"
ordinal = 2367
kind = "pursuit"
timestamp = "2026-10-12T14:12:24+00:00"
summary = "pursuit prove T0463: WITNESSED — refuses when beagle.py's `\"answer\", \"encoded\", \"decoded\")` is put back as `\"answer\")` and beagle.py's `or str(key).lower().startswith(\"input_\"))` is put back as `)`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "60eb3275f8969a1e9dcb670c5e14c97ee2ff4f9c99a65ae9101e149690724f99  .beagle/checks/T0463/T0463.sh" | sha256sum -c --quiet && bash .beagle/checks/T0463/T0463.sh'
refutes: refuses when beagle.py's `"answer", "encoded", "decoded")` is put back as `"answer")` and beagle.py's `or str(key).lower().startswith("input_"))` is put back as `)` (proven 2026-10-12T14:12:23+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_source_judge_judges_results_under_enc
refused after 3s of a 2m43s check at: FAILED tests/test_beagle_example_extension.py::test_source_judge_judges_results_under_encoded_and_decoded_keys
refused with: 1 failed, 811 deselected in 2.87s
