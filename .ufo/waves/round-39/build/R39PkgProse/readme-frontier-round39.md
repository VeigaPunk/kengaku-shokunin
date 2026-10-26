### (b) `corpus/README.md` §Frontier — TB2 sub-bullet, narrowed by one task

*Paste target: `corpus/README.md` §Frontier, the bullet **Agentic benchmark task-spec audits**, as a new child
sub-bullet inserted directly after the existing `*Partly discharged round 38 (2026-10-26):*` sub-bullet and
before the bullet **Contamination transparency cards**. The round-38 sub-bullet's own text
("4 of 89 read", "remaining TB2 task graders") is left byte-identical; this sub-bullet narrows that clause.*

```markdown
  - *Partly discharged round 39 (2026-10-26):* `knowledge/tb2-git-leak-recovery-grader.md` reads and executes a
    fifth Terminal-Bench 2.0 task's scoring code (`git-leak-recovery/tests/test_outputs.py` @ `2fd12b88`; S117,
    S118) against its `instruction.md`, probe `plans/git_leak_probe.py`, receipt
    `corpus/evidence/round39/git-leak-probe.txt`. The graded state is a class the lane had not executed before:
    a git repository's object store and refs plus one flag file at `/app/secret.txt`, scored by a `strip()`ed
    literal equality, two `git log --all` greps (messages, then `-p -S` contents), a `git log --oneline --all`
    substring on the init message, a `git fsck --lost-found` sweep over `dangling` objects and a work-tree
    `sha256sum` that skips dot paths — so the untouched initial repo fails only the flag test, writing the
    literal alone passes 5/5 while the secret commit stays in the reflog, a non-branch ref pinning the secret
    blob, an annotated tag message, a stash, a dot file and `.git/config` all pass 5/5, and a dangling blob or
    an unreferenced commit whose message carries the secret fails test 4 (`cases=25 observed_pass=13
    observed_fail=12 mismatches=0`). The "Terminal-Bench 2.0's" clause is **narrowed for that one task only**;
    it stays open for the remaining TB2 task graders (5 of 89 read), for any SWE-bench Pro V2 grader beyond the
    round-31 one, and for runtime task validity (which `PROVINCE.md` refuses to this lane). Not the task image
    or a harness run (the task's own `solve.sh` is executed as one case and observed pass), not contamination,
    not model or agent behaviour.
```

**Count audit for the "5 of 89" cell.** The four prior graders are `protein-assembly` (round 35),
`regex-log` (round 36), `configure-git-webserver` (round 37) and `build-pmars` (round 38) — their
`corpus/README.md` rows each say "N of 89 TB2 task graders" with N = 1,2,3,4; the round-38 sub-bullet says
"4 of 89 read". This round's task is the fifth, so the cell reads `5 of 89 read`, and the PROVINCE paragraph's
"remaining 84" is `89 − 5`. The denominator `89` is the round-35 census (`89 carry tests/test.sh`) restated in
`plans/round-39-claims.md` §C2 and `PROVINCE.md`'s round-37 paragraph; this draft does not re-derive it.

**Not in this draft (other seats' bytes):** the §What's here index row for the new entry, the §Coverage map
bullet, `corpus/SOURCES.md` rows S117/S118, and the knowledge entry itself. The C2 counter's V6 (census) and
V3 (anchor cells) read those; V7 reads the entry's `## Requirement map`.
