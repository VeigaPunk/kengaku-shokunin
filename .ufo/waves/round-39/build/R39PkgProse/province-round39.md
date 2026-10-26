## Round39 partial frontier admission (2026-10-26)

*Paste target: `PROVINCE.md`, inserted after the round-38 section (after the `**Reported out (round 38) —
sandboxed-probe prior art …**` block and before `## Province map`'s later sections), as the lane's newest
`## RoundNN partial frontier admission` paragraph. Nothing above it changes; the round-35/36/37/38 paragraphs
stay byte-identical (this paragraph narrows only their "remaining TB2 tasks" clause).*

**Core addition:** offline execution of one more pinned Terminal-Bench 2.0 grader —
`git-leak-recovery/tests/test_outputs.py` at terminal-bench-2 `2fd12b88` — over 25 frozen synthetic end states,
via `corpus/knowledge/tb2-git-leak-recovery-grader.md` (S117 `tests/test_outputs.py`, S118 `instruction.md`),
`plans/git_leak_probe.py` and receipt `corpus/evidence/round39/git-leak-probe.txt` (`cases=25 observed_pass=13
observed_fail=12 mismatches=0`; a second run is byte-equal). The graded state is a class new to this lane: a git
repository's object store and refs plus one flag file, scored by five assertions — a `strip()`ed literal equality
read of `/app/secret.txt`, two `git log --all` greps (commit messages with `--grep`, then added/removed content
with `-p -S`), a `git log --oneline --all` substring on the init message, a `git fsck --lost-found` sweep that
`cat-file -p`s every `dangling` line, and a work-tree `sha256sum` that skips dot paths
(`test_outputs.py:11-113`). Each case first runs the task's own `challenge-setup.sh` (the state the Dockerfile
builds at image time, `Dockerfile:12-15`), then a frozen recipe under `bash -euo pipefail`, in a per-case
bubblewrap sandbox: private network/pid/ipc namespaces, `/usr` and `/etc` read-only, private `/tmp`, a fresh
`/app`, `/cap` holding only the three executed captures, `GIT_CONFIG_NOSYSTEM=1` and
`GIT_CONFIG_GLOBAL=/dev/null`; it then imports the captured module and calls its five test functions in file
order (`plans/git_leak_probe.py:1-35`). Observed: the untouched initial repository fails only the flag test
(`untouched`, receipt:6); writing the literal alone passes 5/5 while the secret commit stays in the
reflog/object store (`echo-only`, receipt:8), and so do `echo-gc-only` and `echo-reflog-expire`
(receipt:10,9); a non-branch ref pinning the secret blob, an annotated tag message, a stash, a dot file in the
work tree and the secret in
`.git/config` all pass 5/5 (receipt:15,16,19,20,22); a dangling blob or an unreferenced commit whose message
carries the secret fails exactly test 4 (receipt:12,13); a rewritten tip message and a rebuilt one-commit
history pass (receipt:24,25). It records how that captured grader answers those synthetic states only: it does
not run Terminal-Bench or the task image (the image is never pulled; `tests/test.sh`'s `uvx`/pytest path and its
`/logs/verifier/reward.txt` write are read, not run), does not validate or certify the task, measure difficulty,
gameability or contamination, judge whether these five assertions are the right ones, or speak for the remaining
84 TB2 task graders (89 carry `tests/test.sh`; 5 are read). The task's own `solve.sh` is executed as one case
(`oracle-solve-sh`, receipt:7) and observed 5/5; host git 2.56.0 and host bash stand in for the image's Ubuntu
24.04 git and dash (the checksum runs `sh -c`), the setup runs unprivileged, and commit object ids differ per run
and are never printed. Disclosed ordering: before the freeze the probe ran only `--dry` and `--stage-check`
(`stagecheck cases=25 failed=0`, the grader never imported in stage mode); the receipt is the first recorded run.
Adjacent: sandboxed child execution stays fleet prior art (the round-38 prior-art block above — kumitate's
runner, tameshi's method); capture and citation method stay chousa's; prompt and skill wording stays kotoba's;
deployment configuration and runtime task validity are refused. What git actually stores, and how a given
history was rewritten, is read here only through this grader's assertions — no claim is made about git's storage
semantics or about any real repository or agent, and any such finding routes rather than being absorbed. The
round35/36/37/38 paragraphs above stay as written; this paragraph narrows only their "remaining TB2 tasks"
clause for this one task.

**Reported out (round 39):** nothing absorbed — `plans/pkg_gate.py` stays this lane's own gate, the C1 harness's
scope stays `plans/pkg_gate.py` and `plans/battery39/`, and the round-38 sandboxed-probe split (runner → kumitate,
method → tameshi) is cited, not renegotiated.
