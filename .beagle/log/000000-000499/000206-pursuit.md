+++
id = "000206-pursuit"
ordinal = 206
kind = "pursuit"
timestamp = "2026-10-03T18:27:19+00:00"
summary = "pursuit open T0060: read: list def/class lines when a file is cut at the head"
metric_command = ""
drains = []
hooks = []
+++

criteria: When buffer_tool_result cuts a read result to the head window, the marker is followed by an outline of the file's def/class (incl. async def and methods) lines with their line numbers in the file, so the model can jump with read offset/limit (R08: workers spent 56% of turns paging a 548-line file 60 lines at a time). Line numbers are the file's, also when the read had an offset or prints line-number prefixes. The outline is bounded (entries and chars) so it cannot itself blow the inline budget; a non-read tool and a text with no definitions get no outline.
decided by: sh -c 'echo "0c801f9020570e56e945e1548a0599deb721235031abfcf4d0d812b959615ab2  .beagle/checks/T0060/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0060/check.sh'
budget: 50000 tokens
