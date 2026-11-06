# CriticClaims — round 98 falsification (R98-C1 coverage, R98-C2 freshness)

Seat: leaf critic, round 98, lane `kengaku-shokunin`. Contract: BASE `49a1c4f1`, P0 `5584a6f7`,
P1 `350d0e59`, P2 `c71f04e6`, F `e1a3afd9`, measured T `8e37fc65`. Read-only on the lane; all
runs in an isolated `git clone --shared` at T under
`/fast/scratch/hyaku/kengaku-r98/CriticClaims/` (scratch removed after receipts were copied).
No production edits, no task calls, no frozen-instrument repair.

Commands run (all from the clone root unless noted):

- `python3 plans/round98_c1_replay.py --lane . --rev 8e37fc65... --work SCRATCH/w --grader-venv SCRATCH/G`
  → `LEGS L1..L10=pass`, the exact frozen `TARGET executed_rows=42 ... defects=0`, `PREDICATE R98-C1 pass`, rc 0
  (818.7 s; `c1-T.txt`).
- `python3 plans/round98_c2_nested_bind.py --lane . --rev 8e37fc65... --work SCRATCH/w2b`
  → `LEGS K1..K7=pass`, `GATE defects base=86 rev=45`, the exact frozen `TARGET pop=39 ... new_old_row_defects=0`,
  `PREDICATE R98-C2 pass`, rc 0 (`c2-T.txt`).
- `python3 plans/anchor_digest_check.py --lane <tree> --verbose` at BASE, at T, and on two
  separability fixtures (F + C1 files only; F + PROVENANCE.md only) (`gate-*-verbose.txt`,
  `gate-c1only.txt`, `gate-c2only.txt`).
- `sources-census.sh validate --root /home/vgpnk/Projects/shokunin kengaku` at the lane tip
  (`census-validate.txt`; rc 0, pre-existing W04 only).

## Verdicts

| claim | verdict |
|---|---|
| **R98-C1 / coverage** | **verifies as declared.** The frozen predicate and exact target string reproduce at T in an independent run; the ledger set equality, capture pins, probe rerun, L10 gate leg, prefreeze controls, Q80 and separability all hold. The unenumerated clauses listed in §C1-5 are counter-coverage gaps, not false statements at T. |
| **R98-C2 / freshness** | **verifies as declared** on its frozen predicate, exact strings and kill rule; **the declared population/mechanism is not the change's full effect** (material unenumerated side effect, not a predicate failure). The predicate and exact target string reproduce at T; the BEFORE fails `still=39`; controls, Q80 and separability hold. But the new file clears **41** gate defects, not 39: S213 (`anchor-unbound`) and S230 (`digest-wrong-capture`) are re-bound by the gate's **provenance-url** rule, outside the declared POP. The counter cannot see cleared defects (K7 is new-classes-only) and the claim's universal "no SOURCES row or capture changes" is POP-scoped in K5/K6. The smallest safe correction is verified in §C2-2. |

---

## R98-C1 — coverage (sixteenth member replay, `regex-chess`)

### C1-1 Do-nothing reachability — no cheap lane edit reaches the target beyond the controls

The target's core is forced by the frozen probe rerun: L6 runs `git archive T` + the frozen
`plans/round98_regexchess_probe.py` with the caller's grader venv and requires the receipt's
observation block to match byte-for-byte, with `TOOL_SHA`, `CASE_TABLE_SHA`, `GRADER_SIDE` stamps
equal. The committed receipt (`corpus/evidence/round98/regexchess-probe.txt`) is a real run: 12
CASE lines with 5 observed legs, `mismatches 0`, `LANE_TIP e1a3afd9` (F, an ancestor of T), and
the capture pins. The controls already cover ledger-only flip, forged receipt, extra unearned
member, and the c2-only state; all fail the expected legs (`c1-do-nothing`, `c1-forged-receipt`,
`c1-extra-member`, `c1-c2only`). I found no cheap lane edit that reaches
`executed_rows=42 ... defects=0` without the replay.

Residual path, stated as a limit: L6 re-runs the probe in the **caller-supplied** venv. A venv that
reports the three pinned versions (the probe's `check_venv`) but fakes observations would satisfy
L6; the receipt's `GRADER_SIDE` is only a version stamp. This is the measurement environment's
trust boundary, not a lane edit, and the official run uses the pinned venv.

### C1-2 Causal separability — verified

- C1's exact string is reachable without C2: `c1-positive-run{1,2}.txt` pass with no
  `corpus/evidence/PROVENANCE.md`; `c1-c2only-run{1,2}.txt` fail. At T, L10 only inspects the
  SOURCES rows added after BASE (S326–S333); C2's file binds no regex-chess row.
- C2's exact string is reachable without C1: `c2-positive-run{1,2}.txt` pass on a P1 fixture with
  no C1 candidate bytes; `c2-c1only-run{1,2}.txt` fail. At T, K7 sees no new defect class on a
  BASE row; the C1-only gate fixture (F + C1 files) is 86 defects, the same as BASE, so C1 adds
  no gate defect.
- Neither predicate names a quantity the other changes: C1's L10 is added-rows-scoped; C2's K2/K3/K4/K5
  are BASE-row-scoped.

### C1-3 Q80 — satisfied on the committed artifacts

`c71f04e6` (P2) is an ancestor of `e1a3afd9` (F); the run receipts are unchanged P2→T (the only
P2→T changes under `controls/` are the disclosed README amendment and `candidate/SKILL.md`). Six
C1 controls × two runs: every pair agrees line-for-line after excluding the declared
fixture-commit lines; `c1-forged-receipt-run1/2` differ only in the two `DEFECT L3` fixture hashes
(`6e30af5a…` vs `c60ba5ac…`), which is run-distinguishing evidence. The positive TARGET equals the
frozen string in both runs. The fixture-only freeze table is disclosed in `run_c1_controls.sh`;
the instruments are P1 bytes (P1→F→T diff on all six frozen scripts is empty).

### C1-4 Axis naming — coverage, per AXES.md and the task's expected naming

Coverage = "fraction of the domain's real surfaces the skill governs"; a member replay adds one
grader surface and moves the ledger cells `file-artifact` 32→33 of 76 and
`serialization-schema` 7→8 of 10. Coverage is the lowest non-retired axis at its L0 cap 7
(`SCORECARD.md` rounds 83–97 all record "held at its L0 cap"). The score is held, not moved: the
move is the count (executed 41→42, cells 32→33/7→8), which is the lane's established cap
practice. Naming verifies.

### C1-5 Universal clauses not enumerated by the counter

1. **SKILL class cells.** "the two SKILL class cells (file-artifact 32 → 33 of 76,
   serialization-schema 7 → 8 of 10)" — no round-98 counter reads `SKILL.md`
   (`grep -c SKILL plans/round98_*.py` → 0 in all three; the controls README says so). The
   candidate-bytes table pins the SKILL sha and the bytes at T do say 33/76 and 8/10, but the
   predicate does not verify the derivation. A cheap edit could leave SKILL at 32/7 and still pass.
2. **Source admission.** "S326–S330 admitted (tier A), S331–S333 rejected with flips" — L10 only
   checks that none of the added rows is gate-flagged. A tokenless row (the gate's presence limit)
   or a mis-tiered/mis-status row would pass L10. The rows at T do match (tier A for S326–S332,
   tier B for S333; S331–S333 `rejected` with flip text), and the census validate is rc 0, but the
   counter does not enumerate the clause.
3. **"test.sh's uvx pins".** `test.sh` pins four packages (`pytest==8.4.1`, `chess==1.11.2`,
   `pytest-json-ctrf==0.3.5`) plus `-p 3.13`; the replay venv has three (no
   `pytest-json-ctrf`). The probe's `GRADER_WANT` checks only python/chess/pytest. The ctrf plugin
   is unused by the replay's runner (`pytest.main` without `--ctrf`), so the verdicts do not depend
   on it, but "the verifier side is a venv with test.sh's uvx pins" is not exact.
4. **"before any case ran".** The predictions file's own header says "positive-run timing job bg_5
   was the only grader execution so far (unmodified solve.sh)". C01 is the positive control;
   its prediction was filed after that execution. The other 11 predictions are ex-ante. The
   counter's L5 checks predicted/observed/frozen, not timing. This is a calibration overclaim
   (secondary to the judged axes), disclosed in the file's header rather than concealed.
5. **"the frozen anchor-digest gate binds the new rows".** L10 checks "the BASE gate bytes flag
   none of the SOURCES rows added after BASE", not "bind". At T the gate does bind all eight
   (`BIND S326..S333 ... by=url-task`, `RESOLVED ...`), so the claim is true at T, but a tokenless
   row would pass L10 without binding.
6. **"the probe receipt written by the official run at F".** L3 accepts any ancestor of T; a P1
   receipt with matching observations would pass. The committed receipt's `LANE_TIP` is F, so the
   claim is true at T, but the counter does not require F specifically.

---

## R98-C2 — freshness (nested-capture provenance binding)

### C2-1 The strongest counterexample: the change clears 41 gate defects, not 39

The counter's own `GATE defects base=86 rev=45` line (in `c2-T.txt`, `c2-tip.txt`, and both
positive runs) is the evidence. Diffing the gate's `DEFECT` sets at BASE and T:

- cleared: **41** = the 39 POP rows + **S213 `anchor-unbound`** + **S230 `digest-wrong-capture`**;
- new: 0.

Mechanism, verified by two separability fixtures:

- F + `corpus/evidence/PROVENANCE.md` only → `rows=317 tokens=201 defects=45` (`gate-c2only.txt`).
  So the new file alone produces the 45.
- F + C1's files only (SKILL, ledger, SOURCES, receipt) → `rows=325 tokens=209 defects=86`
  (`gate-c1only.txt`). So C1 alone changes nothing in the gate.

S213 and S230 are not in `POP`: S213 carries two defects at BASE (`token-outside-anchor` +
`anchor-unbound`), so the population rule "only `anchor-unbound`" excludes it; S230's only defect
is `digest-wrong-capture`, not `anchor-unbound`. At T both bind by **`provenance-url`**, not
`provenance-row` (`gate-T-verbose.txt`):

```
BIND S213 capture=corpus/evidence/round52/graders/chess-best-move/tests/test_outputs.py by=provenance-url
BIND S230 capture=corpus/evidence/round52/graders/kv-store-grpc/tests/test_outputs.py by=provenance-url
```

The cause is the URL column of `PROVENANCE.md`: the S201 line carries the `chess-best-move` URL
and the S234 line the `kv-store-grpc` URL; the gate's rule 2 ("a provenance URL — an evidence
markdown naming the same `<repo>/<subpath>`") then binds any row naming that URL, including the
correction row S213 and the sibling S230, which the table never names. The bindings are *true*
resolutions (S213's token is the chess-best-move capture digest; S230's token is the kv-store-grpc
capture digest, equal to SHA256SUMS line 80), so this is not laundering and not a soundness harm.
It is an undeclared effect:

- the claim's population sentence ("39 rows at BASE") is true for its rule, but the change's
  cleared set is 41;
- the claim's mechanism sentence ("binds each row ... through the gate's provenance-row rule")
  is true for the 39 but not exhaustive: two rows bind by a different rule;
- the claim's universal "no gate byte, SOURCES row or capture changes" is true in bytes, but the
  counter's K5/K6 are POP-scoped, and **K7 only detects new defect classes** (`after - before`),
  so cleared defects outside the POP are invisible;
- the controls README calls the `GATE defects base=… rev=…` line "informational ... (it counts
  rows outside the population)" without explaining the 41-vs-39 delta; the positive/do-nothing
  receipts show 86→45 and 86→86, so the delta was visible at P2.

### C2-2 Smallest safe correction (verified)

Drop the pinned-URL column from `corpus/evidence/PROVENANCE.md`. The gate's provenance-row rule
needs only the row id and a backticked filename that resolves beside the file; the URL column is
not needed for the 39 bindings and is the sole cause of the provenance-url re-bindings. Fixture
test (F + PROVENANCE.md with the URL cell removed):

```
rows=317 tokens=201 defects=47          # 86 - 39, exactly the POP
DEFECT S213 ... anchor-unbound ...      # restored
DEFECT S230 ... digest-wrong-capture ...# restored
BIND S230 capture=.../SHA256SUMS by=row-path
LEGS K1..K7=pass
GATE defects base=86 rev=47
TARGET pop=39 cleared=39 still=0 unbound=0 rows_changed=0 captures_changed=0 new_old_row_defects=0
PREDICATE R98-C2 pass
```

(`gate-nourl.txt`, `c2-nourl.txt`.) The predicate still passes and the gate delta now equals the
claim's `cleared=39`. Alternative if the URL column is wanted for human provenance: declare the
41/2 effect in the claim and add a K8 that asserts the gate's cleared set equals POP (the current
K7 cannot).

### C2-3 Do-nothing reachability — the target's core is forced; the file identity is not

The target requires each POP row to bind by `provenance-row` to its expected capture (K4 requires
`binds[sid] == [(path, "provenance-row")]` and `(token, path) in resolved`). The controls cover
do-nothing (`still=39`), partial (one line short → `still=1`), row-edit (tokens blanked → K3/K4/K5/K7),
wrong-capture (round-52 twins → `unbound=10`), gate-edit (K1), capture-edit (K3/K4/K6/K7), c1only
and both. No cheap edit reaches the target without the 39-row table.

Two unenumerated paths, neither reaching the target without the table: (a) K4 checks the binding
*route*, not the binder's identity — the same table appended to an existing evidence markdown
would pass, so "ONE new file, `corpus/evidence/PROVENANCE.md`" is not enumerated; (b) the builder
identity ("built by `plans/round98_provenance_build.py`") is not checked — a hand-built table
passes. Both are provenance-clause gaps, not do-nothing paths.

### C2-4 Causal separability — verified

`c2-positive-run{1,2}.txt` pass on a P1 fixture with no C1 candidate bytes;
`c2-c1only-run{1,2}.txt` fail. At T, C1's captures do not touch the POP bindings (they bind by
provenance-row; the round98 `task.toml` names `regex-chess`, not the POP tasks) and C1's SOURCES
rows are outside the POP. The C2 predicate's exact string is reachable without C1.

### C2-5 Q80 — satisfied on the committed artifacts

Nine C2 controls × two runs, committed at P2 (`c71f04e6`, ancestor of F), unchanged P2→T. Every
pair agrees line-for-line; the `GATE defects base=86 rev=…` lines are identical across runs
(`controls-agree.txt`). The positive TARGET equals the frozen string in both runs. The counters'
bytes at P1, F and T are identical (no diff on the five frozen scripts).

### C2-6 Axis naming — freshness, per AXES.md and the task's expected naming

Freshness = "drift detection — skill claims re-verified against live surfaces; stale items flagged
or fixed". The 39 SOURCES digest claims are re-verified against committed captures and the stale
`anchor-unbound` findings are fixed; the score is held at ceiling 10 (the lane's established
ceiling practice; `SCORECARD.md` rounds 67–97 record "freshness 10 (held)"). Naming verifies. The
side effect in §C2-1 is a freshness *bonus* (two more true resolutions) but outside the declared
population, so it does not change the axis verdict.

### C2-7 Universal clauses not enumerated by the counter

1. "no SOURCES row ... changes" — K5 iterates only `POP`; a non-POP row edit that adds no defect
   class would pass. At T the SOURCES changes are C1's eight added rows; no POP row changed.
2. "no ... capture changes" — K6 iterates only the POP captures; a non-POP capture change that
   does not affect a POP token would pass. At T the captures are unchanged except C1's additions.
3. "ONE new file, `corpus/evidence/PROVENANCE.md`" — K4 checks the route, not the file identity
   (§C2-3).
4. "cleared=39" — claim-local; the gate clears 41 (§C2-1); K7 cannot see cleared classes.
5. "through the gate's provenance-row rule" — true for the 39; the two extra rows bind by
   `provenance-url` (§C2-1).

---

## Smallest safe corrections (round 99; no frozen instrument repaired here)

1. **C2 (load-bearing):** remove the pinned-URL column from `corpus/evidence/PROVENANCE.md` (or
   make it non-matching) so the file binds only by provenance-row; verified: gate 86→47, C2
   predicate still pass (`c2-nourl.txt`). If the URL column is kept, declare the 41/2 effect and
   add a K8 asserting the gate's cleared set equals POP.
2. **C1 (disclosure):** state that the SKILL class cells and the S326–S333 tier/status/flip
   clause are inspected, not enumerated by the counter; state that `test.sh` also pins
   `pytest-json-ctrf==0.3.5` (unused by the replay runner); state that C01's prediction was
   informed by the positive-run timing job (the other 11 are ex-ante).
3. **Both (limit):** the counters' `--grader-venv` is caller-supplied; the receipt stamps only the
   three versions. If the claim is to be fully located, pin the venv's package digests or have the
   probe hash its own site-packages.

## Receipts

All under `.ufo/waves/round-98/w1/CriticClaims/`:

`c1-T.txt` (independent C1 run at T), `c2-T.txt` (independent C2 run at T), `gate-base-verbose.txt`,
`gate-T-verbose.txt`, `gate-c1only.txt`, `gate-c2only.txt`, `defect-diff.txt` (41 cleared / 0 new),
`gate-nourl.txt` + `c2-nourl.txt` (URL-drop fix), `sha-verify.txt` (13/13 frozen, 4/4 candidate at T),
`ledger-counts.txt` (BASE 41 → T 42, added exactly `regex-chess`), `controls-agree.txt` (15 run
pairs, 0 diff lines; C2 GATE lines identical), `census-validate.txt` (rc 0), `predictions-mechanism.txt`,
`test-sh-pins.txt`.
