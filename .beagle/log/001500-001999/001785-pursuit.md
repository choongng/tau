+++
id = "001785-pursuit"
ordinal = 1785
kind = "pursuit"
timestamp = "2026-10-11T03:07:17+00:00"
summary = "pursuit prove T0211: WITNESSED — refuses when summary-R21-R44.md's `| R34 | qwen | cobs | off | off | 515feb3 | 60.…` is put back as `| R34 | qwen | cobs | off | off | 515feb3 | 60.…`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "c71866026d54c4ad6d7ac88c1bc90416c96f72ab26b957f468d5c10ce5982df9  .beagle/checks/T0211/T0211.sh" | sha256sum -c --quiet && bash .beagle/checks/T0211/T0211.sh'
refutes: refuses when summary-R21-R44.md's `| R34 | qwen | cobs | off | off | 515feb3 | 60.…` is put back as `| R34 | qwen | cobs | off | off | 515feb3 | 60.…` (proven 2026-10-11T03:06:18+00:00; refused at Traceback (most recent call last):)
refused after 0s of a 0s check at: Traceback (most recent call last):
refused with: AssertionError: R34: row ['R34', 'qwen', 'cobs', 'off', 'off', '515feb3', '60.0', '6/44', "Cap. 1 of 12 done (known answers); locked files kept in the code task's scope; cobs.py uncommitted"] lacks '7/44'
replaces: refuses when summary-R21-R44.md's `| R34 | qwen | cobs | off | off | 515feb3 | 60.…` is put back as `| R34 | qwen | cobs | off | off | 515feb3 | 60.…` (proven 2026-10-11T03:05:14+00:00; refused at Traceback (most recent call last):)
standing checks red: T0368
