# Item 3 — `corpus/README.md` §Coverage map bullet (eleventh task)

**Surface:** `corpus/README.md` `## Coverage map` (`:268`), the one-bullet-per-covered-grader list.

**Anchor (byte-exact):**

```
file: corpus/README.md
line: 303 (length 411 bytes; sha256 105b0cd2f83d0e8ce0401020c39874b34d6ece5ac0b516e98a70ea2d63895e79)
      - **Terminal-Bench 2.0 task grader (tenth task, constant-compare-of-a-file class)**: covered at
        source-code depth and executed offline (round 44, 2026-10-26) — knowledge/tb2-feal-linear-cryptanalysis-grader.md;
        S138–S146; probe `plans/feal_linear_probe.py`, receipt `evidence/round44/feal-linear-probe.txt`.
        A tenth instance of the same ground (10 of the 89 TB2 task graders; not breadth, and no quality claim).
line: 304  - **Terminal-Bench 2.0 task grader (ninth task, in-process module-import class)**: … (round 43 …)
```

**Edit:** insert one bullet after `:303` (the tenth-task bullet) and before `:304` (the ninth-task bullet), so
the two most recent rounds stay adjacent. Nothing else changes.

```diff
@@ corpus/README.md:303-304 @@
 - **Terminal-Bench 2.0 task grader (tenth task, constant-compare-of-a-file class)**: … (10 of the 89 TB2 task graders; not breadth, and no quality claim).
+- **Terminal-Bench 2.0 task grader (eleventh task, exact-line-membership class)**: covered at source-code depth and executed offline (round 45, 2026-10-26) — knowledge/tb2-password-recovery-grader.md; S149–S156; probe `plans/password_recovery_probe.py`, receipt `evidence/round45/password-recovery-probe.txt`. An eleventh instance of the same ground (11 of the 89 TB2 task graders; not breadth, and no quality claim), on `password-recovery` only: the whole score is two test functions over `/app/recovered_passwords.txt` — existence (`test_outputs.py:8-10`) and whole-line membership of one embedded 23-character constant (`:18`) — with the guess list's length, order and duplicate lines never read, a 1001-line decoy list accepted (`decoys-1000`), the constant published by the task's own `README.md:31` and seeded by `setup.sh:25`, and the `len(guesses) > 0` assert at `:16` unreachable on every input.
 - **Terminal-Bench 2.0 task grader (ninth task, in-process module-import class)**: … (round 43 …)
```

**Why this wording (gate P8, `plans/pkg_gate.py:245-247`):** the coverage bullet must be a line that
**starts with `- `** and contains both `tb2-password-recovery-grader.md` and the receipt path relative to
`corpus/` — i.e. the literal `evidence/round45/password-recovery-probe.txt`, not
`corpus/evidence/…` (`receipt_rel = spec["receipt"].split("/", 1)[1]`, `plans/pkg-spec-r45.json`). The bullet
above contains both. "not breadth, and no quality claim" is the frozen round-44 tail phrasing, kept so the
coverage map does not silently upgrade the claim.

**Count discipline:** the frozen claims fix the wording as *eleventh* task and *11 of 89*; the same 11 appears
in item 2's §Frontier bullet, so the two must be pasted together or not at all.

**Paste precondition:** the bullet names one outcome, `decoys-1000` accepted (frozen prediction,
`corpus/evidence/round45/password-recovery-dry-cases-freeze.txt:22`). Paste only when the probe receipt reports
`mismatches=0`; otherwise state the observed verdict for that case instead.
