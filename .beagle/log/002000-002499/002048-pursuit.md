+++
id = "002048-pursuit"
ordinal = 2048
kind = "pursuit"
timestamp = "2026-10-12T08:02:10+00:00"
summary = "pursuit retry T0421 (1 of 3)"
metric_command = ""
drains = []
hooks = []
+++

The note had bare 'Action:' and 'Evidence:' label lines, which diagnosed.sh's regexes don't read. The analysis agent reported a pass it hadn't got. Fixed in e839b434 and ace59aab; the check now exits 0, and prove --absent witnessed it.
