# GateMutate70 — hostile attack on the R70-C2 mutation matrix

Seat: GateMutate70 (mutation-tester, leaf). Lane: `kengaku-shokunin`, branch `master`.
Target: the `--mutants` / `--selftest` control matrix of the R70-C2 routed-defect gate.

**Measurement pin — worktree bytes at gate sha256 `367ce58e41799a75b9fd3a9df5ad032c1fe30acc89b7fb4bba32ffb7c35a36fb`.**
The lane was landing concurrently. The probe first pinned gate `011b5d13…`; between rounds the L1
advanced the gate to `367ce58e…` with a hardening outside the control code: E3/E4's `used-by` test became
`if len(c) != 11 or NGINX_ENTRY not in c[10]` (was `if len(c) > 11 and NGINX_ENTRY not in c[11]`), which
silently skipped the test on a short row. `git diff master -- plans/round70_c2_routed_defects.py` is now
that plus the A1 E1 argument-order hunk (`4 insertions(+), 3 deletions(-)`); **nothing inside `check()`,
`selftest()` or `mutants()` changed**, and every tally below re-ran identical at both pins. The evidence
here is the `367ce58e…` round, pinned before and after with zero drift. Every gate line number below is
the running worktree file (verified unchanged by the byte-length-neutral edits); in the master blob the
`check()`/`selftest()`/`mutants()` lines are one lower after 152. Companion pins in
`shipped/source-shas.json`: SKILL `baf3c714…`, README `b4342d69…`, SOURCES `b1acdb73…`,
QUALITY `89e39c4a…`, nginx entry `d02a5b37…`, lesson `80066383…`. Python 3.14.8. **No tool installed or
upgraded**; no pacman, npx or uv call.

Scratch: `/fast/scratch/hyaku/kengaku-r70/GateMutate70` and the re-pin round
`/fast/scratch/hyaku/kengaku-r70/GateMutate70-r2` (both deleted after these receipts were copied here).
All work is read-only against the lane: the hostile gates are copies under scratch, and every
lane-root run used `--root` with no write path.

## 1. Commands and rc

| # | command (cwd = lane root unless noted) | rc |
|---|---|---|
| 1 | `python3 plans/round70_c2_routed_defects.py` | 0 |
| 2 | `python3 plans/round70_c2_routed_defects.py --mutants --work <scratch>/shipped/mutants/work` | 0 |
| 3 | `python3 plans/round70_c2_routed_defects.py --selftest --work <scratch>/shipped/selftest/work` | 0 |
| 4 | `python3 <scratch>/repro_hostile_mutants.py --lane <lane> --scratch <scratch>/repro` | 0 |
| 5 | each hostile gate `--root <lane>` (live green lane, read-only) | 0 for all six |

Transcripts: `shipped/{plain,mutants,selftest}/`, `transcript-repro.txt`, `arms/<gate>/<arm>/`, `live/`.
The harness is committed here as `repro_hostile_mutants.py`; it rebuilds the shadow lane, generates all
six hostile sources with asserted single-hit substitutions, and runs every arm.

## 2. The shipped arms reproduce, verbatim

```
DEFECTS n=0
PREDICATE R70-C2 pass
```
```
MUTANT 1 depth-gate-identity defects=7 killed=True      … (8 lines, all killed)
MUTANTS total=8 killed=8
```
```
E1..E8 defect … (fake lane)
DEFECTS n=8
PREDICATE R70-C2 fail
SELFTEST defects-in-fake=8 want=8 all-fail=True
SELFTEST e2-byte-flip-red=True
SELFTEST ok=True
```

The claims' C2 control tallies are reproducible at this pin. Nothing below disputes them; the attack is
on what the matrix can discriminate, not on whether it ran.

## 3. Hostile mutants the shipped matrix cannot generate

Method. `build_fake()` reads ten lane files, so a shadow lane holding exactly those files (same bytes,
sha-pinned in the transcript) makes `LANE` resolve and lets the **shipped** `selftest()`/`mutants()`
code run unmodified on a hostile source. Each hostile source is derived from the gate by substitutions
that assert exactly one hit; each is `ast.parse`-checked. Sources: `mutants/*.py`.

`--mutants` generates exactly one mutation shape: delete a whole `CHECKS` line
(`for n, name, _ in CHECKS` at `plans/round70_c2_routed_defects.py:432`; regex `^    \(%d, %s, .*\),\n`
at `:433`). It never mutates a check body and never changes the lane state. The six gates below are
outside that space.

| id | mutation (relative to the running gate) | fake-lane `DEFECTS n=` | `--selftest` | `--mutants` | verdict |
|---|---|---|---|---|---|
| H1 | `check_instruction_row` body replaced by `return True, "problems=[]"` | **7** (`E3 ok`) | `defects-in-fake=7 want=8 all-fail=False`, rc 1 | `total=8 killed=1` (only `3:7K`; the rest 6), rc 1 | **caught** (both arms) |
| H2 | delete `CHECKS` entries 5 and 8 (`corpus-index`, `wave-validation`) | **6** | `defects-in-fake=6 want=8 all-fail=False`, rc 1 | `total=6 killed=0`, rc 1 | **caught** (both; total is self-derived) |
| H3 | E5's boolean is skipped by the counter: `E5 defect` is printed, `defects` is not incremented | **7 counted, 8 defect lines** | `defects-in-fake=8 want=8 all-fail=True`, **`ok=True`, rc 0** | `total=8 killed=1` (only `5:7K`), rc 1 | **caught by `--mutants` only; `--selftest` is fooled** |
| H4b | entries 5 and 8 deleted, re-added as distinct-text aliases of E7's check: `(5, "corpus-index-v2", check_gate_reject)`, `(8, "wave-validation-v2", check_gate_reject)` | **8** | `8 want=8 all-fail=True`, `ok=True`, rc 0 | `total=8 killed=8`, rc 0 | **survived** |
| H5 | `check_gate_reject` short-circuits: `if (root / LESSON70).is_file(): return True, "problems=[]"` | **8** | `8 want=8 all-fail=True`, `ok=True`, rc 0 | `total=8 killed=8`, rc 0 | **survived** |
| H6 | H2 plus both control constants derived: `ok = failed == len(CHECKS)`, `want={len(CHECKS)}`, `dead = got == len(CHECKS) - 1` | **6** | `defects-in-fake=6 want=6 all-fail=True`, `ok=True`, rc 0 | `total=6 killed=6`, rc 0 | **survived** (only the printed 6 vs frozen 8 tells) |

The per-mutant lines are in `arms/<gate>/mutants/stdout.txt`. H1/H3's `killed=1` localises the vacuous
entry by elimination; that is a real strength of the matrix and is credited in the verdict.

## 4. Each hostile gate against the one frozen defect it hides

Four-lane fixture: `BASE_green` (all eight corrections present, synthetic), and one lane per defect
(`L_E3` entry anchor reverted, `L_E5` README round-69 row/block removed, `L_E7` lesson `## Gate` with no
reject-with-reason, `L_E5E8` README broken + wave receipts dropped). Each lane is built from the same
sha-pinned shadow bytes; the mutations assert they bit. The honest gate goes red on every defect lane,
so the *checks* discriminate these states; only the hostile gates below do not.

| lane | honest gate | hostile gate | hostile output |
|---|---|---|---|
| `BASE_green` | `n=0 pass` rc 0 | all six | `n=0 pass` rc 0 |
| `L_E3` (E3 open) | `n=1 fail`, `E3/F instruction-row` | **H1** | `n=0 pass` rc 0 — the E3 defect is reported `E3 ok` |
| `L_E5` (E5 open) | `n=1 fail`, `E5/F corpus-index` | **H3** | prints `E5 defect corpus-index …` **and** `DEFECTS n=0`, `PREDICATE pass`, rc 0 |
| `L_E5` | `n=1 fail` | **H2**, **H4b** | `n=0 pass` rc 0 (H2 with six E lines; H4b with the two alias names) |
| `L_E5E8` (E5+E8 open) | `n=2 fail`, `E5/F` + `E8/F` | **H2**, **H4b**, **H6** | `n=0 pass` rc 0 |
| `L_E7` (E7 open) | `n=1 fail`, `E7/F gate-reject` | **H5** | `n=0 pass` rc 0 |

Transcripts: `hide-*.txt`.

## 5. The live green lane

At the pin, the real lane is green (`shipped/plain` → `n=0 pass`). Running the hostile gates with
`--root <lane>` (read-only) gives:

- **H2**: six E lines — `depth-gate-identity`, `trio-receipt`, `instruction-row`, `s241-correction`,
  `r69-landing-receipt`, `gate-reject` — then `DEFECTS n=0`, `PREDICATE R70-C2 pass`, rc 0.
  Two of the frozen eight checks are absent and the frozen predicate sentence's printed evidence is
  satisfied. This is the most direct coverage finding: the predicate text does not bind the eight.
- **H4b**: eight lines, but `E5 ok corpus-index-v2` and `E8 ok wave-validation-v2` replace the frozen
  `corpus-index` / `wave-validation`; `n=0 pass`.
- **H1, H3, H5**: eight lines with the frozen names, `n=0 pass` — identical to the honest gate on a
  green lane; their defect exists only on a wrong-correction lane (section 4).
- **H6**: same six-line green output as H2, and both control arms green as well (section 3).

`live/live-summary.json` records rc, `n`, and the observed name list for each.

## 6. Blind spot, named

Both arms are **count-only over one lane state**, and each derives its expectation from the object
under test:

- `selftest` counts printed lines, not the counter, and never compares the two:
  `failed = sum(1 for ln in out.splitlines() if ln.startswith("E") and " defect " in ln)` (`:401`),
  `ok = failed == 8 and rc == 1` (`:402`). H3 prints a defect and is not counted; the line count still
  reads 8. H4b/H5 print eight lines and H6 six; all pass.
- `mutants` derives its mutant set from `CHECKS` and its expected count from `len(CHECKS)`:
  `total={len(CHECKS)}` (`:448`), `return 0 if killed == len(CHECKS) else 1` (`:449`). The absolute 7
  is hardcoded (`dead = got == 7 …`, `:445`) but never cross-checked against an observed name set.
  H6 shows the whole criterion is satisfiable with six entries and six sub-mutants.
- `check()` prints `DEFECTS n={defects}` over whatever `CHECKS` holds (`:337–350`); no arm, and no line
  of the frozen predicate, compares the observed `(n, name)` pairs to the frozen E1–E8. H2 and H4b on
  the live lane prove the printed contract survives 6 checks or aliased names.
- The only "present but wrong" state any arm builds is E2's EOF append
  (`(fake / TRIO_NGINX).write_text(fresh + "x", …)`, `:410`). E1 and E3–E8 are only ever exercised in
  the **fully absent** state, which is exactly the state H5 is built to pass.

So: the matrix tests harness plumbing — each frozen entry contributes exactly one defect on the
all-stripped lane — not whether each check still derives its correction. H4b (aliases keep the total),
H5 (vacuous when the artifact exists), and H6 (constants derived from the artifact) are the survivors;
H2 is caught only because `killed == len(CHECKS)` collapses, and its live run defeats the predicate
sentence itself.

## 7. Hardening shape (report only — no predicate, case table, digest, kill rule or target edited)

These are proposals for a next round's matrix, not changes to R70-C2:

1. Pin the observed set: a module constant `FROZEN_CHECKS = ((1, "depth-gate-identity"), …)` and
   `assert [(n, name) for n, name, _ in CHECKS] == FROZEN_CHECKS` before printing. Kills H2, H4b.
2. Add a per-check **wrong-correction** arm: start from the green lane and mutate each check's own
   artifact by one byte/section; require that check red. The honest gate already goes red on the four
   lanes I built (`L_E3`, `L_E5`, `L_E7`, `L_E5E8`), so the detectors exist; only the arm is missing.
   Kills H1, H3, H5.
3. Make `selftest` compare `failed` to the counter and to the frozen name list, not only to the literal
   8. Kills H3.
4. Keep the absolute cardinality out of the artifact under test: `want=8`, `got == 7` and
   `total == 8` should be constants the mutant copies cannot edit. Kills H6.

Coverage limits of this probe, stated: I built wrong-correction lanes for E3, E5, E7, E8 only; E1, E4
and E6 were exercised green plus the shipped absence arm, and E2's flip arm was not re-attacked beyond
noting it appends at EOF. The fixtures are synthetic lanes under scratch, not lane bytes.

## Verdict

**R70-C2's mutation matrix is a valid plumbing test and a partial vacuity detector, but not a
discriminator of check validity.** At pin `367ce58e…` (and identically at the earlier `011b5d13…`) it reproduces `MUTANTS total=8 killed=8` and
`SELFTEST defects-in-fake=8 want=8 all-fail=True`, and it catches H1 and H2 outright and H3 through the
mutants arm alone; H3's printed-but-uncounted defect, however, passes `--selftest` with `ok=True`
rc 0, and three hostile gates (H4b aliased entries, H5 existence-as-proof, H6 self-referential
constants) survive **both** arms with rc 0. The blind spot is structural: both arms are count-only over
the single all-stripped lane, `CHECKS`/`len(CHECKS)` are the only cardinality the code knows, and no arm
compares the observed `E<n> <name>` set to the frozen eight or exercises a correction that is present
but wrong. The committed gate is green and its eight corrections are present; this is a coverage
finding about what the controls would fail to catch, not a claim that they are currently lying.
