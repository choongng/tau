+++
id = "000039-pursuit"
ordinal = 39
kind = "pursuit"
timestamp = "2026-10-03T11:13:27+00:00"
summary = "pursuit open T0024: R01 fix: an over-long milestone title is split or refused before founding writes anything"
metric_command = ""
drains = []
hooks = []
+++

criteria: pursuit_found checks every milestone title against MAX_TASK_TITLE before writing pursuit.toml or adding any task; an over-long title is refused with a message naming which milestone and its length and asking for a shorter title (the detail goes in the intent after '::'), and nothing is written. A title of exactly MAX_TASK_TITLE founds normally.
decided by: sh -c 'echo "733f2b2c36f0e99f7630d239b332ec5ec7b1676ee7a0f1be5d7fa48d8562a9d1  .beagle/checks/T0024/named_tests.sh" | sha256sum -c --quiet && bash .beagle/checks/T0024/named_tests.sh tests/test_beagle_example_extension.py 2 test_found_refuses_long_milestone_before_writing test_found_accepts_max_length_milestone'
budget: 80000 tokens
