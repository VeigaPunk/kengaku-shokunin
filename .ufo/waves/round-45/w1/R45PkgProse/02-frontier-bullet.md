# Item 2 — `corpus/README.md` §Frontier narrowing bullet (11 of 89)

**Surface:** `corpus/README.md` `## Frontier` → the `**Agentic benchmark task-spec audits**` bullet and its
`*Partly discharged round NN*` sub-bullets.

**Exact current wording (found, not assumed).** The TB2-count clause currently reads, in the newest
sub-bullet:

```
file: corpus/README.md
line: 425 (length 1235 bytes; one long line, sha256 b31d77b2fe84d29bef223a149d070e74221a85e43d412f4897682829133ce3e5)
      … `cases=14 observed_pass=8 observed_fail=6 mismatches=0`, `regrade cases=14 differ=0`. The
      "Terminal-Bench 2.0's" clause is **narrowed for that one task only**; it stays open for the remaining
      TB2 task graders (10 of 89 read), for any SWE-bench Pro V2 grader beyond the round-31 one, and for
      runtime task validity (which `PROVINCE.md` refuses to this lane). Not the task image (never pulled) or a
      harness run, not contamination, not model or agent behaviour.
line: 426 `    refuses to this lane). Not the task image (never pulled) or a harness run, not contamination, not model or agent`
line: 427 `    behaviour.`   (sha256 b699489674439c98a06deb1fbe5987ad16c192e5b80b7e626c3f26c35ac978b6)
```

So the count to move is the parenthetical `(10 of 89 read)`; the new bullet states `(11 of 89 read)`. The
round-44 bullet is **not** rewritten (each round's bullet records the count it stood at, and round 44's was 10).

**Edit:** insert a new sibling sub-bullet after `:427` (`    behaviour.`), before `- **Contamination
transparency cards**` at `:428`.

```diff
@@ corpus/README.md:427-428 @@
     behaviour.
+  - *Partly discharged round 45 (2026-10-26):* `knowledge/tb2-password-recovery-grader.md` reads and
+    executes an eleventh Terminal-Bench 2.0 task's scoring code (`password-recovery/tests/test_outputs.py` @
+    `2fd12b88`; S149–S156) against its `instruction.md`, probe `plans/password_recovery_probe.py`, receipt
+    `corpus/evidence/round45/password-recovery-probe.txt`. The graded artefact is an agent-written guess list
+    the grader splits on newlines (`:14`) and tests for whole-line membership of one embedded 23-character
+    constant (`:18`) — a class distinct from round 44's 100-substring scan: line order, guess count,
+    duplicates, CRLF endings and decoy padding are invisible, while a guess concatenated with decoys on one
+    line (`constant-joined`) and the `PASSWORD=` form `instruction.md:4` quotes (`password-eq`) both fail; the
+    constant is published in the task's own `README.md:31` and written into the image by `setup.sh:25`, so
+    four of the five predicted passes need no recovery at all (`constant`, `constant-crlf`, `crlf-line`,
+    `decoys-1000`) and the fifth is the task oracle (`oracle-solve-sh`), and the `len(guesses) > 0` assert at
+    `:16` cannot fire on any input. `cases=16 observed_pass=<<P>> observed_fail=<<F>> mismatches=0`, `regrade
+    cases=16 differ=0`. The "Terminal-Bench 2.0's" clause is **narrowed for that one task only**; it stays open
+    for the remaining TB2 task graders (11 of 89 read), for any SWE-bench Pro V2 grader beyond the round-31
+    one, and for runtime task validity (which `PROVINCE.md` refuses to this lane). Not the task image (never
+    pulled) or a harness run, not contamination, not model or agent behaviour.
 - **Contamination transparency cards**: why — `knowledge/contamination-detection-and-transparency.md` …
```

**The one substitution — `<<P>>` / `<<F>>`.** Take them verbatim from the summary line of
`corpus/evidence/round45/password-recovery-probe.txt` (printed by `plans/password_recovery_probe.py:358`):

```
cases=16 observed_pass=P observed_fail=F mismatches=0
```

Do **not** guess 5/11 from the frozen dry table: `predicted_pass=5 predicted_fail=11`
(`corpus/evidence/round45/password-recovery-dry-cases-freeze.txt:26`) is a prediction, and per the frozen kill
rule a mismatch is a defect in the receipt, not a number to paste. If `mismatches=` is not `0`, this bullet
must not be pasted at all.

**Why this placement satisfies V9:** `plans/round45_c2_verify.py:328-330` requires the literal `password-recovery`
inside `## Frontier`; the bullet names it in the first clause and again in the code path.
