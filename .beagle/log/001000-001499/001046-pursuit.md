+++
id = "001046-pursuit"
ordinal = 1046
kind = "pursuit"
timestamp = "2026-10-05T10:58:57+00:00"
summary = "pursuit open T0254: Locked files stay as locked; known-answers note only when true"
metric_command = ""
drains = []
hooks = []
+++

criteria: The split's WIP commit, done-by's check and each driver step see locked files as locked (put back, said in one line); the known-answers brief says a test imports none of the code only when its AST imports no project module, says to keep an import of a module that exists, and is not added to a fix task whose check runs a test importing code.
decided by: sh -c 'echo "10c8de4f8eae49a1bf4604bf6161c909dffb3c3c5d6bd9b47f199350734868f2  .beagle/checks/T0254/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0254/check.sh'
budget: 60000 tokens
