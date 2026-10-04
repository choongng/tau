+++
id = "000571-pursuit"
ordinal = 571
kind = "pursuit"
timestamp = "2026-10-04T07:37:03+00:00"
summary = "pursuit open T0137: Workers do not read .beagle/ or re-read references from scratch"
metric_command = ""
drains = []
hooks = []
+++

criteria: The worker scope guard refuses reading anything under .beagle/ (read tool, cat/grep/sed/head/tail over a .beagle path, and git show of a .beagle path) with a line saying the brief already holds what the task needs; bash write-target detection sees the directory uv init creates; a retry brief carries the previous attempt's report so the worker does not re-read references to rediscover it.
decided by: sh -c 'echo "a740f698bb8f97421c970d85a4a9d8c08d7256c6901aaf864838b321afa388cd  .beagle/checks/T0137/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0137/check.sh'
budget: 60000 tokens
