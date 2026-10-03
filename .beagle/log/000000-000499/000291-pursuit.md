+++
id = "000291-pursuit"
ordinal = 291
kind = "pursuit"
timestamp = "2026-10-03T20:06:25+00:00"
summary = "pursuit open T0071: reference fetch retries a timed-out URL with a longer timeout"
metric_command = ""
drains = []
hooks = []
+++

criteria: _fetch_references retries a URL whose first fetch timed out (socket/TimeoutError, or URLError whose reason is a timeout) once, with REFERENCE_FETCH_RETRY_TIMEOUT = 90 s; a failure that is not a timeout (HTTP error, refused, too large, no text) is recorded at once with no retry. A URL that fails twice is recorded with both attempts' reasons. R09: itc2008.pdf timed out at 30 s at founding and every worker re-downloaded it to /tmp.
decided by: sh -c 'echo "94aee8578df906438ae0480c9878034305d17d51e740e0162583edd886ac041c  .beagle/checks/T0071/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0071/check.sh'
budget: 25000 tokens
