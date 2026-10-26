# PROVINCE.md round-37 drop-in (draft for L1; not applied)

Insert at EOF, after `PROVINCE.md:257` (the round-36 `**Reported out:**` line). Body words: 139
(`len(body.split())`), the same count as the landed round-36 paragraph (`:244-255` → 139). Nothing above
`:258` is edited.

```markdown
## Round37 partial frontier admission (2026-10-26)

**Core addition:** offline execution of a third pinned Terminal-Bench 2.0 grader of a class the lane had
not run — `configure-git-webserver/tests/test_outputs.py` and `tests/verify.sh` at terminal-bench-2
`2fd12b88`, a stdout-substring verdict over a helper script probing a live HTTP service — over 22 frozen
synthetic service states, each in a private-network bubblewrap sandbox, via
`corpus/knowledge/tb2-git-webserver-grader.md` (S111–S113), `plans/git_webserver_probe.py` and receipt
`corpus/evidence/round37/git-webserver-probe.txt` (`cases=22 observed_pass=9 observed_fail=13
mismatches=0`). It records what that verdict depends on for lane-built states only: it never runs
Terminal-Bench, the task image, the oracle path or a real git push; validate or certify a task; own
nginx, git or ssh administration; or measure agent performance. Adjacent: fixture craft (tameshi),
research method (chousa), prompt craft (kotoba) and seat arrangement (kumitate) stay theirs. The round36
paragraph above stays as written; this one narrows only its "any other TB2 task" clause for this task.
```

Word-cut options if the L1 wants slack under the 140 ceiling (139 now): drop "frozen" in "22 frozen
synthetic service states" (−1) and "of a class the lane had not run" (−8) → 130.
