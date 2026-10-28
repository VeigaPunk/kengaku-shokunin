# R50C1ExecCounterSelftest — selftest of `plans/round50_c1_verify.py` at the stage-1 freeze

Seat: executor (leaf) · lane `kengaku-shokunin` · round 50 · wave 1 · serves **R50-C1 (novelty)**.
Item: the six-case self-test of the C1 counter on a clone at the stage-1 freeze. Nothing else was touched.

**No admission is claimed for R50-C1 or R50-C2.** No production file, `SCORECARD.md`, `LOG.md` or `corpus/` path
was written. Every run below is a **control**, not a scored run.

## Axes named (Godspeed)

1. **Falsification power per frozen leg** — destroy one leg's evidence; does the predicate still fail? (cases b–e)
2. **Literal independence** — can the counter satisfy an expectation from the files it reads, instead of from the
   frozen literals `126 / 20 / 12 / SEALED50_MIN`? (b, c, d)
3. **Receipt reproducibility and failure attribution** — is a printed line byte-stable across runs, and does the
   receipt say *which* condition failed? (f, all runs)
4. **Setup-error contract** — do operator mistakes land on the documented exit codes (0 pass / 1 fail / 2 setup)?

Cheap, parallel, one clone; a case that improves (1)–(4) and harms nothing is kept. All 13 runs are declared below,
including the ones that came back as expected.

## Revision measured (REV)

    REV 3b02d573d58cc6d2e0d27ef92ac0815354912252      <- printed by every one of the 13 runs

Ancestry asserted before any measurement, in the live lane (read-only):

    $ cd /home/vgpnk/Projects/shokunin/kengaku-shokunin
    $ git rev-parse HEAD               -> 5c56819f7964f4af19c960de08a49cd8f95781ce
    $ git merge-base --is-ancestor 3b02d573d58cc6d2e0d27ef92ac0815354912252 HEAD   -> ANCESTOR=yes

Frozen digests re-confirmed inside the clone, before measuring:

    f9b9873e602dd09228d0164412d450b2cef95c3055ce9347fa05b9377637bd76  plans/round50_c1_verify.py
    05d5fe03aa3be6b79eb2469b7c86d0a20c9b424bea2e058d580e31a96c8aad5e  plans/fixture_fence.py
    b5197f941a9f523eaedae6bd7be39531a0f80e10c6b05030687dbeacfb3fae69  plans/honest50/population.txt

## Environment

    S=/fast/scratch/hyaku/kengaku-r50/R50C1ExecCounterSelftest
    export TMPDIR=$S
    git clone --shared /home/vgpnk/Projects/shokunin/kengaku-shokunin "$S/lane"
    git -C "$S/lane" rev-parse --show-toplevel        -> $S/lane     (asserted before checkout)
    git -C "$S/lane" checkout --detach 3b02d573d58cc6d2e0d27ef92ac0815354912252
    git -C "$S/lane" status --porcelain | wc -l       -> 0

Python 3.14.8, git 2.56.0, 32 cores. One clone per seat; each case measured on its own `cp -a` copy of the clone
(`case-b`, `case-c`, `case-c2`, `case-d`, `case-d2`, `case-e`, `case-e3`, `case-f`). `rev-parse --show-toplevel` was
asserted equal to itself on `lane`, `case-b`, `case-c`, `case-c2`, `case-d` and `case-e`; `case-d2`/`case-e3` are
`cp -a` of already-asserted trees and each printed `REV 3b02d573…` from its own `git -C . rev-parse HEAD`. No tool
was installed or updated. No git mutation outside the scratch clones.

Canonical command shape used for every run (cwd = the tree under test; `--work` pre-created because the counter
does not create it — see D4):

    ( cd <tree> && python3 plans/round50_c1_verify.py --lane . --work "$S/work-<case>" [flags] ) > out 2>&1

## Case table — one line per case, with exit code

| # | case | tree | flags | key observed lines (verbatim) | exit |
|---|------|------|-------|-------------------------------|------|
| a | fence with no `breach` | `lane` | `--fence $S/nobreach.py --skip-mutants` | `HONEST fixtures=126 admitted=0 refused=0 error=126`; `REFUSALS total=20 clean=0 leaked=0`; `SEALED total=12 clean=0 leaked=0`; `PREDICATE R50-C1 fail` | **1** |
| b | one population row deleted | `case-b` | `--allow-dirty --skip-mutants` | `POPULATION fixtures=125 … mismatched=0 build_errors=0`; `HONEST fixtures=125 admitted=112 refused=13`; `PREDICATE R50-C1 fail` | **1** |
| c | one `tree_sha256` corrupted in `population.txt` | `case-c` | `--allow-dirty --skip-mutants` | `POPULATION fixtures=126 pin=2365fc6f… mismatched=1 build_errors=0`; `POPULATION-MISMATCH a_class-x14-two-errata`; `PREDICATE R50-C1 fail` | **1** |
| c2 | one row's **built** tree corrupted, pin intact | `case-c2` | `--allow-dirty --skip-mutants` | `POPULATION fixtures=126 pin=b5197f94… mismatched=1`; `POPULATION-MISMATCH n21-separate-gitdir`; `PREDICATE R50-C1 fail` | **1** |
| d | `plans/sealed46` emptied | `case-d` | `--allow-dirty --skip-mutants` | `SEALED total=0 clean=0 leaked=0 build_errors=0`; **no** `SEALED-TOTAL`/literal line; `PREDICATE R50-C1 fail` (attributable only to `HONEST refused=13`) | **1** |
| d2 | d **plus** `plans/sealed50` with 6 modules | `case-d2` | `--allow-dirty --skip-mutants` | `SEALED total=0 clean=0 leaked=0` **and** `SEALED total=6 clean=6 leaked=0`; no aggregate, no floor line; `PREDICATE R50-C1 fail` (HONEST only) | **1** |
| e | one mutant payload that cannot apply (23-row battery) | `case-e` | `--allow-dirty` (mutant leg on) | `MUTANT broken c1-mut-03-drop-file-mountbound patch-rc=1 …`; `MUTANTS total=23 caught=2 broken=13 floor=12 verdict=unmet` | **1** |
| e' | literal `broken=1` (one-row battery, inapplicable payload) | `case-e3` | `--allow-dirty` | `MUTANT broken c1-mut-03-drop-file-mountbound patch-rc=1 …`; `MUTANTS total=1 caught=0 broken=1 floor=12 verdict=unmet` | **1** |
| f | dirty tree, default mode | `case-f` | `--skip-mutants` | `TREE dirty=1`; every leg line identical to the clean run; `PREDICATE R50-C1 fail` | **1** |
| f' | same dirty tree + `--allow-dirty` | `case-f` | `--allow-dirty --skip-mutants` | **byte-identical** to (f) except two work-dir-embedded lines (D5) | **1** |
| — | clean control | `lane` | `--skip-mutants` | `TREE dirty=0`; `HONEST fixtures=126 admitted=113 refused=13 error=0`; `REFUSALS total=20 clean=20 leaked=0`; `SEALED total=12 clean=12 leaked=0`; `PREDICATE R50-C1 fail` | **1** |
| — | clean control, full | `lane` | (none) | as above plus `MUTANTS total=23 caught=3 broken=12 floor=12 verdict=unmet` | **1** |
| — | clean control + `--allow-dirty` | `lane` | `--allow-dirty --skip-mutants` | identical to the clean control except the two work-dir-embedded lines | **1** |

All 13 exit codes are also in `.ufo`-external scratch log form (transcribed below because scratch was removed):

    c0-baseline-clean            exit=1  PREDICATE R50-C1 fail
    c0b-baseline-clean-full      exit=1  PREDICATE R50-C1 fail
    c0c-control-clean-allowdirty exit=1  PREDICATE R50-C1 fail
    cA-no-breach-fence           exit=1  PREDICATE R50-C1 fail
    cB-row-deleted               exit=1  PREDICATE R50-C1 fail
    cC-tree-corrupt-inrow        exit=1  PREDICATE R50-C1 fail
    cC2-tree-corrupt-built       exit=1  PREDICATE R50-C1 fail
    cD-sealed46-empty            exit=1  PREDICATE R50-C1 fail
    cD2-sealed46-empty-50of6     exit=1  PREDICATE R50-C1 fail
    cE-mutant-payload-broken     exit=1  PREDICATE R50-C1 fail
    cE3-single-broken-row        exit=1  PREDICATE R50-C1 fail
    cF-dirty-default             exit=1  PREDICATE R50-C1 fail
    cF2-dirty-allow              exit=1  PREDICATE R50-C1 fail

Wall time 7–16 s per run on 32 cores (158 fixtures + 20 + 12 hostile builds).

### Exactly what each copy was mutated by (reproducible)

- `$S/nobreach.py` (case a): single line `x = 1  # a fence module with no breach() callable`,
  sha256 `9826c2ed0c12813c20aa05e350d8e0e482171e1a262c35bedfc388d31f3cf2cb`.
- `case-b`: deleted population line 130, i.e.
  `HONEST 2f30385bc3b6929684a579996406a507361b83920472aa28d3491855d084e563 r46novel plans/honest50/modules/r46novel/n09_ignored_untracked.py#build n09-ignored-untracked anchor`
  (126 → 125 rows).
- `case-c`: row `a_class-x14-two-errata`, field 2 `8ec1d843…2186f3` → `0ec1d843…2186f3` (first hex char flipped).
- `case-c2`: `plans/honest50/modules/novel50/n21_separate_gitdir.py`,
  `ctx.write(wt / "b.txt", "two\n")` → `ctx.write(wt / "b.txt", "TWO-ISOLATION\n")` (built identity changes;
  `population.txt` and its pin are untouched).
- `case-d`: removed the 12 `plans/sealed46/*.py` (directory and `__pycache__` left in place, so the leg still
  enumerates — it just finds nothing).
- `case-d2`: `case-d` **plus** `plans/sealed50/` holding 6 **copies** of sealed46 modules (no new hostile code was
  authored; this is an arithmetic probe of the `S` floor, not a blind module set).
- `case-e`: 23-row battery, row `c1-mut-03-drop-file-mountbound` payload replaced by
  `--- a/plans/fixture_fence.py / +++ b/… / @@ -1,1 +1,1 @@ -THIS CONTEXT LINE IS NOT IN THE FENCE +NOT APPLICABLE`.
- `case-e3`: same substitution, battery reduced to that single row.
- `case-f`: untracked file `dirty-marker.txt` at the tree root.

## What the six cases actually established

**Expected behaviour, reproduced, keep:** (a) a fence module without `breach` yields
`HONEST … admitted=0 refused=0 error=126` — every fixture ERROR, no admission, predicate fail. Crucially the hostile
legs report `clean=0 leaked=0`, i.e. an exception is **not** counted as a leak and `clean != len(files)` does fail
the predicate: no false clean. (b) a deleted row prints `fixtures=125` and fails *only* because the frozen literal
`HONEST_TOTAL = 126` and the row count disagree — the population cannot self-satisfy its own denominator, which is
the property the claim froze. (c) a corrupted row prints `mismatched=1` and a `POPULATION-MISMATCH` line naming the
`fid`. (c2) strengthens (c): the identity check fires with the **pin intact** (`pin=b5197f94…`, `mismatched=1`), so
`mismatched` is an independent gate, not a side effect of the pin hash changing. (e/e') `broken` increments exactly
by one per non-applying payload (`12 → 13` on the real battery, and the literal `broken=1` on a one-row battery).

**Contradicted by measurement — six defects.** Line numbers are the clone at `3b02d573…`.

**D1 — the SEALED leg is not gated by any literal (the item's clause "must still fail on REFUSALS/SEALED compared to
literals" is NOT met).**
- `SEALED46_TOTAL = 12` at line 64 is **defined and never read**. `grep -n SEALED46_TOTAL` returns exactly one hit —
  the definition. `REFUSALS_TOTAL` *is* compared (lines 259–260); the sealed analogue does not exist.
- Consequence, measured (case d): `SEALED total=0 clean=0 leaked=0 build_errors=0` and the guard at line 255
  (`if clean != len(files) or leaked or nfail`) evaluates `0 != 0` → False, `leaked=0`, `nfail=0`, so **nothing sets
  `ok = False` for the sealed leg**. The run still exits 1, but only because `HONEST refused=13` (the stage-1 base
  fence). The differential against the clean control differs in exactly one line (`total=12` → `total=0`) and not in
  exit code, so the sealed-total axis carries no weight in the predicate.
- **D1b — a missing `plans/sealed50/` is silent.** The blind leg is only looked at `if (lane / "plans/sealed50").is_dir()`
  (line 262). On the stage-1 tree the directory does not exist: the run prints `SEALED total=12` with no
  `SEALED50-TOTAL` line and no failure. The claim's `SEALED total=<S>`, `S ≥ 18`, is therefore enforced by nothing
  until a directory happens to exist.
- **D1c — the frozen line cannot be produced.** `SEALED` is printed once per directory (`leg()` is called per
  `REFUSALS_REL`/`SEALED_RELS` entry), so at stage 3 the output will contain **two** `SEALED total=` lines
  (`total=12` and `total=<sealed50>`); there is no aggregate `S` and no `S ≥ 18` comparison anywhere. Measured in
  case d2: `SEALED total=0 …` followed by `SEALED total=6 …`.
- **D1d — measured false clean:** case d2 prints `SEALED total=6 clean=6 leaked=0` — 6 is below the claim's floor of
  18 — with no diagnostic and no predicate contribution. `[INFERENCE]` With `HONEST` repaired (the S2 aim) and the
  same 6-module sealed50 / empty sealed46 layout, lines 244–266 and 293 are all satisfied and the counter would print
  `PREDICATE R50-C1 pass` with `S = 6`. Not demonstrated empirically, because authoring a fence that passes would
  itself invalidate the round.

**D2 — `broken` is not part of the gate.** Line 290 is
`if caught < MUTANT_MIN or len(mutants) < MUTANT_MIN: ok = False`. A run can print
`MUTANTS … caught=13 broken=1 … verdict=met` and `PREDICATE R50-C1 pass`, contradicting the frozen predicate line
`MUTANTS total=<M> caught=<k> broken=0`. Two measured aggravations: (i) `total` counts non-applicable rows, so the
`len(mutants) >= 12` half of the floor is satisfiable by rows that never ran; (ii) at `3b02d573…` **12 of 23** rows
do not apply at all, so `broken=12` is the *normal* state of the carried battery on the base fence.
Corroborates the sibling critic's correction (`R50C1CritPredicate.md`, "plus `broken == 0` in the mutant gate"),
measured here on the frozen battery.

**D3 — no failure attribution, and `--allow-dirty` is invisible in the receipt.** `PREDICATE R50-C1 fail` is
printed with no summary of which leg failed; the dirty gate (line 178) sets `ok = False` and prints nothing but
`TREE dirty=<n>`. Case (f) vs (f') are byte-identical apart from two path lines, both exiting 1 — a reader cannot
tell from the receipt that the clean-tree requirement was violated, nor that `--allow-dirty` was supplied. The same
gap applies to the population leg: case (b) prints `fixtures=125` with no `expected=126` (contrast
`REFUSALS-TOTAL … expected=20`, which does).

**D4 — setup errors do not land on exit 2.** `--work` is handed to `tempfile.mkdtemp(dir=...)` (line 165), which does
not create it; `--fence` is hashed at line 80 before the build. Both produce a bare traceback and **exit 1**, the same
code as a predicate fail, with no `SETUP` line and no `PREDICATE` line:

    P2 --work $S/no-such-work-dir   -> FileNotFoundError … exit=1
    P1 --fence $S/does-not-exist.py -> FileNotFoundError … exit=1

Only missing *lane* files get the documented `SETUP missing <rel>` + `return 2`. The C1 kill rule ("`PREDICATE` line
absent or `fail`") still excludes these receipts, so this is a diagnosability defect, not an admission hole.

**D5 — two receipt lines are not reproducible.** The refusal reasons for `n14-stash-entry` and `n16-notes-ref` embed
the fixture path relative to the random `mkdtemp` work directory, e.g.
`…/work-cF-dirty-default/k50-c1-e6notv7p/honest/m026-…/repo/.git/logs/refs/stash`. Two runs of the **same** tree
differ in exactly those two lines (diff of `c0` vs `c0c`, and of `cF` vs `cF2`). Every predicate-relevant line is
stable; a committed `corpus/evidence/round50/c1-receipt.txt` re-run will not be byte-identical.

**D6 — the carried battery, measured (observation, not a defect of the counter).** On the base fence at
`3b02d573…`, `MUTANTS total=23 caught=3 broken=12 floor=12 verdict=unmet`:

- **caught (3):** `c1-mut-03-drop-file-mountbound`, `c1-mut-13-entry-cap-shrink`, `c1-mut-19-lane-membership`
- **survived (8):** `c1-mut-05-git-top-commondir`, `c1-mut-07-config-cr`, `c1-mut-10-inside-prefix`,
  `c1-mut-12-store-required`, `c1-mut-14-argv-placeholder`, `c1-mut-16-argv-shape-tail`,
  `c1-mut-20-packedref-peel`, `c1-mut-22-fixture-symlink`
- **broken (12):** `c1-mut-01-gitdir-file`, `c1-mut-02-symlink-dir-dead`, `c1-mut-04-hardlink-threshold`,
  `c1-mut-06-objinfo-fallthrough`, `c1-mut-08-config-unknown-key`, `c1-mut-09-url-insteadof`,
  `c1-mut-11-head-ref-widen`, `c1-mut-15-hook-suffix`, `c1-mut-17-config-value-backslash`,
  `c1-mut-18-graph-magic-empty`, `c1-mut-21-log-namespace`, `c1-mut-23-gitdir-repo-reorder`

The brief's starting state says "4 of 23 change the verdict vector"; on this tree, with this command and the
counter's own three-leg reference vector, the number is **3** (partition 3 + 8 + 12 = 23, checked programmatically).
The difference is definitional (which verdict vector counts) and does not change the conclusion: the battery is a
candidate only, S2 must re-derive it with witnessed kills, and 12 rows cannot witness anything against the base
fence because they do not apply.

## Consequences for the round (no judgement, only what the measurements force)

- Cases (a), (b), (c) confirm the counter's *admission* and *identity* gates behave as frozen, including the
  literal-independence and the pin-independent `mismatched` gate. Those legs are not the problem.
- Cases (d) and (e) are **not** satisfied as the item states them: an emptied `sealed46` does not fail on any
  SEALED literal (D1), and `broken` is not gated (D2). Both are inside the open window's allowed repair list —
  "a measured defect (a leg that cannot run, a false clean …)" — and neither touches the frozen sentence, the four
  leg names, the literals `126/20/12/SEALED50_MIN` or the pin.
- Read with `R50C1CritPredicate.md` (which reports a fence reaching `PREDICATE R50-C1 pass` by keying on fixture
  paths and by rebinding `apply_mutant`), the instrument as frozen at `3b02d573…` cannot carry a scored C1 run before
  the open-window repairs. That is the L1's call, not this seat's.

## Limits

- Measured only at `3b02d573d58cc6d2e0d27ef92ac0815354912252`; the S2 fence, the re-derived battery and any
  `plans/sealed50/` do not exist yet, so every `SEALED` figure here is the 12-module stage-1 leg.
- Cases (b)–(f) required `--allow-dirty` (a copy of the lane cannot be committed by this seat); their leg lines are
  therefore the same as a clean run would print, but the clean-tree requirement itself is only exercised in (f)/(f').
- No passing fence was authored, and none may be: the counter's pass path is evidenced only by source reading, marked
  `[INFERENCE]` above.
- The dirty gate's *load-bearing* effect is confirmed at source (line 178) but cannot be isolated through exit codes
  on a stage-1 tree, because every admissible fence already fails `HONEST`; that is exactly what (f)/(f') show.
- Not measured: behaviour when the `patch` binary is absent (`apply_mutant` would raise, exit 1, no `broken` row);
  hostile-module build failures; the `--fence` + `--skip-mutants` combination on the hostile legs beyond case (a);
  anything about out-of-`d` reads (`plans/round46_c1_verify.py`'s property, unchanged).
- Host sensitivity of the population is unchanged and untested here (git 2.56.0 in this environment).

## Scratch

Scratch root `/fast/scratch/hyaku/kengaku-r50/R50C1ExecCounterSelftest` (one clone, eight case copies, thirteen work
dirs, 5.1 GB, all output files) was removed with `trap 'rm -rf -- "$S"' EXIT` before yield. Everything citable is transcribed above
verbatim; no evidence lives only in scratch, and no receipt file was placed in the lane tree beyond this report (the
seat's write scope is its own report).

## VERDICT

**The counter's admission and identity gates are sound; its SEALED-literal gate and its mutant `broken` gate are not
gated at all, and its receipt cannot attribute a failure.** At `REV 3b02d573…`, cases (a) `HONEST … error=126` +
`PREDICATE fail`, (b) `fixtures=125` + fail, (c) `mismatched=1` + fail, (d) `SEALED total=0` with **no literal
comparison and no failure attributable to SEALED**, (e) `broken=1` (`broken=13` on the real battery) with `broken`
excluded from the gate at line 290, (f) `TREE dirty=1` + fail but with output identical to the `--allow-dirty` run —
all exit 1 on this tree, so **exit code alone proves nothing for cases d–f**; the leg lines do. Required before any
scored C1 run: compare each SEALED leg to its literal (`12`, `SEALED50_MIN`) and print one aggregate `S`, require
the blind directory's presence, add `broken == 0` (and count only applicable rows) to the mutant floor, print a
failure reason, and emit `SETUP` + exit 2 for bad `--work`/`--fence`. No R50-C1/R50-C2 admission is claimed; no
production file was modified.
