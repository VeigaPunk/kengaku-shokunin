# Item 5 — `LOG.md` round-45 C2 bullet block

**Surface:** `LOG.md` (1372 lines). Round 44's section is the last one: heading
`## Round 44 (hyaku run 9, 2026-10-26) — five advertised behaviours killed with value-attributed kills (5/5)
under fences F1–F6; tenth TB2 grader executed` at `:1337`, and its C2 bullet at `:1351-1357` is the model.

**Anchors (byte-exact):**

```
file: LOG.md  (1372 lines; ends `\n`)
line: 1372 (sha256 dcfb087ac9a61af49100cf48cfdd672f1ba8589a827def4d019be43b36e22a63)
      - Round shape: one v2 wave (68 seats: executor 22, scribe 11, critic 9, scout 7, mutation-tester 5, reviewer 5,
        connector 4, sentinel 2, simplifier 2, revenger 1) + one residual call (8: reviewer 5, critic 3) = 76.
```

Model bullet (round 44, `:1351-1357`), which the block below mirrors in shape — `- C2 (coverage, predicate met):`
then `TB2 <task> @ 2fd12b88, S-rows (A);` then `probe <counts>;` then `V11 <counts>.` then `Observations: …`:

```diff
@@ LOG.md (under the new `## Round 45 …` heading, after the C1 bullet) @@
+- C2 (coverage, predicate met): TB2 `password-recovery` @ `2fd12b88`, S149–S156 (A); probe `cases=16
+  observed_pass=<<P>> observed_fail=<<F>> mismatches=0`, `regrade cases=16 differ=0`; V11 `states=48
+  grader_pass=18 grader_fail=30 disagree=0`. Observations: the whole score is two test functions over
+  `/app/recovered_passwords.txt` — `Path(...).exists()` (`test_outputs.py:8-10`) and whole-line membership of the
+  embedded 23-character constant `8XDP5Q2RT9ZK7VB3BV4WW54` (`:18`) — with the `len(guesses) > 0` assert at `:16`
+  unable to fire on any input, the list's length, order and duplicate lines never read, CRLF accepted through
+  `read_text()`'s universal-newline mode (`crlf-line`, `constant-crlf`), the `PASSWORD=` form `instruction.md:4`
+  quotes refused (`password-eq`), a guess concatenated with decoys on one line refused (`constant-joined`), and a
+  1001-line decoy list accepted (`decoys-1000`). The constant is published by the task's own `README.md:31` and
+  written into the image by `setup.sh:25`, so four of the five predicted passes need no forensic recovery at all
+  and the fifth is the task oracle (`oracle-solve-sh`, whose `OUTPUT_FILE="recovered_passwords.txt"` at
+  `solve.sh:51` is relative — it lands at the graded path only because `Dockerfile:20` sets `WORKDIR /app`; the
+  `under-varsea` case shows the same recovery work failing from another cwd). The environment seeds a 4MB image
+  (`setup.sh:22`), splits the zip at the password's byte offset (`:29-30`) and dd's the halves at the 1MB and 3MB
+  offsets with a noise log between them (`:36-41`). pytest is not run: the harness reproduces each test's verdict,
+  which is the only thing `tests/test.sh:25-28` rewards (`verifier.timeout_sec = 900.0` at `task.toml:22`).
```

**Two bracketed inserts the L1 owns (numbers I will not invent):**

- `- C2 (coverage, `**`predicate met`**`):` — paste `predicate met` only when
  `python3 plans/round45_c2_verify.py --lane .` prints `checks=11 defects=0` / `PREDICATE C2 pass`, exit 0. The
  freeze's before-state is `checks=11 defects=8`, `PREDICATE C2 fail`
  (`.ufo/waves/round-45/claims/control-c2-nothing.txt`), so this line is the claim the counter has to earn.
- A coverage-score sentence, if the round's ledger wants one (round 44 wrote `Coverage held at 7 (L0 cap).`).
  The claims carry coverage 7 "capped by the open L0 question `kengaku | round-33`"; whether round 45 holds 7 or
  moves is not mine to assert.

**V11 numbers are read, not assumed:** `.ufo/waves/round-45/claims/control-c2-predictor.txt` line
`CONTROL predictor=membership V11 ok states=48 grader_pass=18 grader_fail=30 disagree=0` — the 48 states are 16
password-shaped kinds under `random.Random(45)`, so most of them fail the captured grader (18 pass / 30 fail),
unlike round 44's balanced 24/24.

**Substitution `<<P>>` / `<<F>>`:** from `corpus/evidence/round45/password-recovery-probe.txt`'s
`cases=16 observed_pass=P observed_fail=F mismatches=0`. If `mismatches` is not 0 the probe receipt is itself
defective (frozen kill rule) and this bullet does not go in.

**Heading (optional draft, L1's choice — not part of my five items):**

```
## Round 45 (hyaku run 9, 2026-10-26) — the advertised fixture fence calibrated to zero contradictions (C1); eleventh TB2 grader executed
```

Round 44's heading names its kill count and landed grader; C1's kill count for round 45 is `R45SentFenceDesign`'s
and the L1's to fill, so the parenthetical is a placeholder, not a claim.
