+++
id = "002618-pursuit"
ordinal = 2618
kind = "pursuit"
timestamp = "2026-10-13T03:04:07+00:00"
summary = "pursuit open T0515: eval: q35 itc + cobs on contract add, the anchor listing and bare-name operations (R83, R84)"
metric_command = ""
drains = []
hooks = []
+++

criteria: R83 (q35 itc) and R84 (q35 cobs) ran on contract-first beagle at or after a80193c and tau at or after 96b9beb9 with no dirty code, each has a scorecard, and the grade on file is the grader's re-run over the run's adapter, listed by progress.py and in dev-notes/contract-first/eval.md. (Runs launched before this open; the check was written after.)
decided by: sh -c 'echo "0c217f497607fae37f1c187db4e5bd5c64954f6b8ae494026f8101437f7098ad  .beagle/checks/T0515/T0515.sh" | sha256sum -c --quiet && bash .beagle/checks/T0515/T0515.sh'
budget: 60000 tokens
opened over T0493: the owner asked for the q35 trials after ideas 1 and 2, 10-12
