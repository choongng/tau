+++
id = "001115-pursuit"
ordinal = 1115
kind = "pursuit"
timestamp = "2026-10-05T14:13:12+00:00"
summary = "pursuit open T0270: Repeat breaker ignores duplicate list entries"
metric_command = ""
drains = []
hooks = []
+++

criteria: _call_key treats two calls whose list arguments differ only by duplicate entries as the same call (a list of strings is de-duplicated, order kept), so the repeat breaker counts them as repeats; other argument differences still make distinct keys.
decided by: sh -c 'echo "a4da49f54db675f0c92a1aef0c053306b82f7b9e24bb35fc3af5b5aeb4abcab9  .beagle/checks/T0270/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0270/check.sh'
budget: 25000 tokens
