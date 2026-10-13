+++
id = "002612-pursuit"
ordinal = 2612
kind = "pursuit"
timestamp = "2026-10-13T01:00:00+00:00"
summary = "pursuit open T0512: beagle contract: an operation is exercised by entries that name it by bare name, and the refusal says what name it matched (R82)"
metric_command = ""
drains = []
hooks = []
+++

criteria: contract check counts an operation exercised when an example, limit, invalid or property names it by bare name (before any argument list or ->, last dotted part), so R82's 'encode(data: bytes) -> bytes' is exercised by examples naming 'encode'; the second extraction and diff compare operations the same way; a truly unexercised operation's refusal names the bare name compared and the names the exercising entries use. beagle CI green. (Work was begun before this open: the check was written after; prove shows it refuses.)
decided by: sh -c 'echo "aad4b0e5ec2c2c48564bcd64d2ccb12637d03bbab49788e1881607772c911bc6  .beagle/checks/T0512/T0512.sh" | sha256sum -c --quiet && bash .beagle/checks/T0512/T0512.sh'
budget: 40000 tokens
opened over T0493: unblocks the 35b trials the owner asked for next (R82 stalled on it), 10-12
