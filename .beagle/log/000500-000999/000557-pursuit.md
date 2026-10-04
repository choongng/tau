+++
id = "000557-pursuit"
ordinal = 557
kind = "pursuit"
timestamp = "2026-10-04T07:10:57+00:00"
summary = "pursuit prove T0134: WITNESSED — refuses when beagle.py's `if len(parts) != 1 or len(lines) < 2:` is put back as `if True:`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "b0a6fea68adec4aef5fab135bd06fc26df6a59fb9279bb272f0f4476f20cf3ad  .beagle/checks/T0134/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0134/check.sh'
refutes: refuses when beagle.py's `if len(parts) != 1 or len(lines) < 2:` is put back as `if True:` (proven 2026-10-04T07:10:10+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_plan_of_one_part_with_three_lines_is_split_into_parts)
refused after 1s of a 38s check at: FAILED tests/test_beagle_example_extension.py::test_plan_of_one_part_with_three_lines_is_split_into_parts
refused with: 1 failed in 0.75s
