+++
id = "002619-pursuit"
ordinal = 2619
kind = "pursuit"
timestamp = "2026-10-13T03:05:07+00:00"
summary = "pursuit prove T0515: WITNESSED — refuses when eval.md's `| R84 | q35 | cobs | contract-first a80193c (ad…` is put back as `| R84 | q35 | cobs | contract-first a80193c (ad…`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "0c217f497607fae37f1c187db4e5bd5c64954f6b8ae494026f8101437f7098ad  .beagle/checks/T0515/T0515.sh" | sha256sum -c --quiet && bash .beagle/checks/T0515/T0515.sh'
refutes: refuses when eval.md's `| R84 | q35 | cobs | contract-first a80193c (ad…` is put back as `| R84 | q35 | cobs | contract-first a80193c (ad…` (proven 2026-10-13T03:04:09+00:00; refused at Traceback (most recent call last):)
refused after 0s of a 0s check at: Traceback (most recent call last):
refused with: AssertionError: ('R84', '39/44', 'not in eval.md')
