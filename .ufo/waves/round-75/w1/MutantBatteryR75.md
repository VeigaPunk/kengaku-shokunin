# MutantBatteryR75 — instrument mutation battery (kengaku round 75, wave w1)

Role: mutation-tester. Instruments under test: `plans/round75_c1_index_parity.py` (C1) and
`plans/round75_c2_registry_audit.py` (C2). Scratch clone only; lane tree untouched.

## 1. Setup (all under `/fast/scratch/hyaku/kengaku-r75/MutantBatteryR75/`)

- `git clone --shared /home/vgpnk/Projects/shokunin/kengaku-shokunin lane` → clone HEAD
  `43255758ed7d74ea05c8e03686dd9ad37837f0cd` (Amendment A1), branch `refs/heads/master`,
  `git rev-parse --show-toplevel` → `/fast/scratch/hyaku/kengaku-r75/MutantBatteryR75/lane`.
- Pristine sha256 (before any mutation):
  - C1 `b1597c4edf46eb961d4430d487f86034018ab63b13d8b4b84c154e623146545f`
  - C2 `2a251098f4d98b2f2f887477bd5835ccbc7a8ba65cfe527e3a34acdb1ef523ff`
- No lane-tree edit, no git mutation anywhere in the lane or the clone. Fixture git ops
  (§5 demo repo) were preceded by `git rev-parse --show-toplevel` printing the fixture dir,
  per host guard.

## 2. Detector (bounded, same for pristine / mutated / restored bytes)

`python3 plans/round75_c{1,2}_registry_*.py --selftest --work <fresh dir>` run from the clone
root. **KILLED** = rc≠0 or per-arm `SELFTEST` case lines differ from the pristine baseline;
**SURVIVED** = rc=0 and case lines identical. The `LANE_TIP/WORKTREE` header is excluded from
the comparison: during any mutation window the tracked instrument itself is edited, so
`WORKTREE` legitimately reads `dirty` (it read `clean` in the pristine baselines and again
after restoration).

## 3. Pristine baselines (clone at `43255758`, `WORKTREE clean`)

- C1 `--selftest`: 5 case lines all `ok`, `SELFTEST cases=5 red=4 failures=0 ok=True`, rc=0.
- C1 `--lane .`: Before-state reproduced exactly — `UNIVERSE knowledge files=74 indexed=71
  missing=3 orphan=0`, `lessons files=123 indexed=87 missing=36`, `evidence dirs=66 indexed=46
  missing=20`, 59 `MISSING*` lines by name, `PREDICATE R75-C1 fail`, rc=1.
- C1 `--control-rowshuffle`: `NAIVE rows=6 surfaces=6 equal=True`, 4 `MISSING*` defects,
  `PREDICATE R75-C1-control pass`, rc=0.
- C2 `--selftest`: 4 arm lines all `ok`, `SELFTEST arms=4 failures=0 ok=True`, rc=0.
- C2 `--control-attribute`: `R74-METRIC killed=10/10 (any-defect counting)`,
  `R75-METRIC expected_matched=9/10 wrong_id=1`, `OFF-TARGET … matched=False`,
  `NULL-ARM defects=0`, pass, rc=0 — matches receipt `c2-control-attribute.txt` byte-for-byte
  in content.
- C2 full verdict `--lane . --mutants --check-stamps corpus/evidence/round75`: `MISMATCH 0`,
  `DEFECTS n=0`, `MUTANTS real=9 expected_matched=9 wrong_id=0 survived=0 null_arms=1
  null_survived=1 total=10`, `STAMPS files=0 stamped=0 unstamped=0 unresolved=0
  not_ancestor=0`, `PREDICATE R75-C2 pass`, rc=0.

## 4. Mutations — one at a time, each restored before the next

Restoration after every mutation: `cp` of the pristine snapshot back over the instrument,
sha256 re-checked equal to the pristine hash, `git status --porcelain --<file> | wc -l` → 0.
Final leg (§6): both batteries rerun on restored bytes reproduce the baselines exactly.

### C1 (`round75_c1_index_parity.py`) — 9 mutants, SURVIVORS n=4

| id | mutation (old → new) | mutated sha256 | `--selftest` behavior | verdict |
|----|----------------------|----------------|----------------------|---------|
| M1 | census missing leg inverted: `[f for f in files if f not in targets]` → `if f in targets` | `c0ba5e19…` | `FAIL clean` + `FAIL missing-knowledge` + `FAIL missing-lesson`, `failures=3 ok=False`, rc=1 | **KILLED** |
| M2 | orphan leg dropped: `orphan = sorted(...)` → `orphan: list[str] = []` | `ba626c08…` | `FAIL orphan-knowledge rc=0 want=1`, `failures=1`, rc=1 | **KILLED** |
| M3 | `MISSING-EVIDENCE` zeroed: `missing_ev = [...]` → `missing_ev: list[str] = []` | `72a754ed…` | `FAIL missing-evidence rc=0 want=1`, `failures=1`, rc=1 | **KILLED** |
| M4 | `drop_row` disabled in `build_fixture`: `keep = [r for r in rows if not drop_row or drop_row not in r]` → `keep = list(rows)` | `453f9fbd…` | `FAIL missing-knowledge` + `FAIL missing-lesson`, `failures=2`, rc=1 | **KILLED** |
| M5 | `LANE_TIP` line dropped from `emit()`'s report text | `3f22317f…` | byte-identical, rc=0 | **SURVIVED** |
| M6 | `orphan_ev` inverted (dropped `not` before `(ev_root / m).is_dir()`) | `463f1c03…` | `FAIL clean rc=1 want=0`, rc=1 | **KILLED** |
| M7 | report arithmetic lie: `indexed={len(files) - len(missing)}` → `indexed={len(targets) - len(missing)}` | `fa694a1b…` | byte-identical, rc=0 | **SURVIVED** |
| M8 | `emit()` rc masked: `return 0 if not defects else 1` → `return 0` | `f7c70efe…` | byte-identical, rc=0 | **SURVIVED** |
| M9 | predicate word flipped: `{'pass' if not defects else 'fail'}` → `{'pass' if defects else 'fail'}` | `bda4d378…` | byte-identical, rc=0 | **SURVIVED** |

Killed 5 / survived 4 / inconclusive 0. Every survivor is real (demonstrated, not equivalent):

- **M5** — mutated `--lane .` body starts with a second `WORKTREE dirty` line; the `LANE_TIP`
  line is gone from the bytes `emit()` prints and writes to `--receipt`. Such receipts would be
  refused by C2 `--check-stamps` as `UNSTAMPED`, yet the C1 battery stays green.
- **M7** — mutated `--lane .` prints `UNIVERSE knowledge files=74 indexed=68 missing=3` and
  `UNIVERSE lessons files=123 indexed=51 missing=36` (pristine: 71 / 87). The frozen target
  lines (`indexed=74`, `indexed=123`) become unreachable; battery blind because `selftest`
  discards report lines (`defects, _ = census(d)`).
- **M8** — mutated `--lane .` prints `PREDICATE R75-C1 fail` over 59 defects and **exits 0**
  (pristine rc=1). The claim's `rc 0/1` semantics are masked.
- **M9** — mutated `--lane .` prints `PREDICATE R75-C1 pass` over the same 59 defects (rc still 1).

Check that failed to bite (all four): `selftest()` exercises only `build_fixture` + `census`
and never calls `emit()`/`main()`; M5/M8/M9 live in `emit`, M7 in the report lines the battery
throws away. **Proposed arm that kills all four** (one arm class): a golden-output arm — run
`emit()` on the clean fixture and on one red fixture (e.g. the `missing-knowledge` kwargs) and
assert the exact fingerprint: lines[0] == `LANE_TIP <resolved 40-hex>`, lines[1]
startswith `WORKTREE `, the exact `UNIVERSE knowledge files=2 indexed=2 missing=0 orphan=0`
report lines, `PREDICATE R75-C1 pass` on clean vs `fail` + rc==1 on red (and rc==0 on clean).

### C2 (`round75_c2_registry_audit.py`) — 11 mutants, SURVIVORS n=8

| id | mutation (old → new) | mutated sha256 | `--selftest` behavior | verdict |
|----|----------------------|----------------|----------------------|---------|
| N1 | arm 3 weakened to any-defect counting: `if exp not in " ".join(defs)` → `if not defs` | `ce739f49…` | byte-identical, rc=0 | **SURVIVED** |
| N2 | verdict tally literals: `wrong_id={len(results) - len(matched)} survived={…}` → `wrong_id=0 survived=0 ` | `2449cd1c…` | byte-identical, rc=0 | **SURVIVED** |
| N3 | `null_survived={0 if null_defects else 1}` → literal `null_survived=1` | `396b2b79…` | byte-identical, rc=0 | **SURVIVED** |
| N4 | merge-base ancestor check disabled: `if tip != "unknown" and git(...).returncode != 0:` → `if False:` | `e034bd51…` | byte-identical, rc=0 | **SURVIVED** |
| N5 | `flag-not-declared` append → `pass` (S250 flip leg neutered) | `a856605b…` | `FAIL expected-id: mismatched=1` (M8 fixture unmatched), rc=1 | **KILLED** |
| N6 | arm 3 containment inverted: `exp not in` → `exp in` | `158e7e15…` | `FAIL expected-id: mismatched=9`, rc=1 | **KILLED** |
| N7 | unknown-stamp refusal dropped: `if not m or m.group(1) == "unknown":` → `if not m:` | `44105891…` | byte-identical, rc=0 | **SURVIVED** |
| N8 | HEX40 format gate disabled: `if not HEX40.match(rev_id):` → `if False:` | `628870c4…` | byte-identical, rc=0 | **SURVIVED** |
| N10 | null measurement stubbed: `null_defects = defects_of(null_dir)` → `null_defects: list[str] = []` | `ee2d342b…` | byte-identical, rc=0 | **SURVIVED** |
| N11 | off-target expected id relabelled to an id present in its defects (`":entry:unbacked-flag:"` → `"MALFORMED-ROW columns=9"`) | `98f28578…` | `FAIL off-target: expected MALFORMED-ROW columns=9 absent, other defects 1`, rc=1 | **KILLED** |
| N12 | selftest dispatch rc masked: `return 0 if fails == 0 else 1` → `return 0` | `c70c877f…` | byte-identical, rc=0 | **SURVIVED** |

Killed 3 / survived 8 / inconclusive 0. Survivor evidence (each demonstrated against a pristine
reference run of the same command):

- **N1** — on green data every real mutant's defect set is nonempty, so any-defect counting
  coincides with attribution; arm 1 prices only the off-target fixture boolean, not the tally
  derivation. (R74-D4 regression in miniature.)
- **N2/N3** — even the mutated **full verdict** (`--lane . --mutants --check-stamps
  corpus/evidence/round75`) prints the same `MUTANTS real=9 expected_matched=9 wrong_id=0
  survived=0 … null_survived=1 total=10` line: the literals coincide with the derived truth at
  A1. The derivation is severed and nothing in the battery would notice until the matrix shifts.
- **N4** — hermetic demo (§5): mutated `--lane ../work/foreignrepo --check-stamps
  ../work/demo_foreign` → `STAMPS files=2 stamped=2 unstamped=0 unresolved=0 not_ancestor=0`
  (orphan-root receipt accepted); pristine → `stamped=1 … not_ancestor=1` +
  `DEFECT REVISION:not-ancestor foreign.txt ee6dfa91d1ef`.
- **N7** — demo dir `../work/demo_stamps` (unstamped / `LANE_TIP unknown` / `LANE_TIP
  not-a-hash` / tip-stamped / ancestor-side-branch-stamped): mutated → `DEFECT STAMP-MALFORMED
  unknown.txt unknown`, tally `unstamped=1 unresolved=2`; pristine → `DEFECT UNSTAMPED
  unknown.txt`, `unstamped=2 unresolved=1`.
- **N8** — same demo dir: mutated → `DEFECT REVISION:unresolvable malformed.txt not-a-hash`
  (unresolved=1); pristine → `DEFECT STAMP-MALFORMED malformed.txt not-a-hash` (unresolved=1).
  Tally shape unchanged, defect class silently rebranded.
- **N10** — the R74-D4 hard-coded-literal class replayed on the null arm: arm 2 asserts
  `not null_defects`, which the stub satisfies vacuously because the true null tally is 0.
  Recomputation cannot distinguish either (the true value **is** `[]`); no data-dependent arm
  on green fixtures can kill it.
- **N12** — red-path-only mutant: with failing arms the battery would print `FAIL` lines yet
  exit 0, masking failures from every rc-keying consumer (the claim's kill rule reads rc).

Proposed killing arms:

1. **Attribution/tally arm (kills N1, N2, N3):** inside `--selftest`, append the off-target arm
   to arm 3's list with its wrong id and require the derived `mismatched == ["X-off-target"]`
   (i.e. wrong_id=1 computed from data), and assert the printed `MUTANTS` line equals the line
   re-derived from `mutate()` results (golden derivation cross-check).
2. **Stamp-leg red receipts (kills N4, N7, N8):** extend arm 4's fixture with three receipts —
   `LANE_TIP unknown`, `LANE_TIP not-a-hash`, and a resolvable non-ancestor (orphan-root commit
   in a hermetic fixture repo, §5) — and require `UNSTAMPED unknown.txt` (unstamped+1),
   `STAMP-MALFORMED` (unresolved+1), `REVISION:not-ancestor` (not_ancestor+1) while the
   tip-stamped receipt stays `stamped`.
3. **Null-measurement liveness (kills N10):** factor the null measurement behind a named
   function and add a canary arm asserting that function reports a known defect
   (`DUPLICATE-ROW`) on a known-bad fixture — a literal stub fails the canary; a green-only
   recomputation cannot.
4. **Red-exit assert (kills N12):** one arm that forces a failing scenario (tampered fixture)
   and requires the battery to exit 1 — golden red run.

## 5. Hermetic not-ancestor fixture (for the N4 demo)

`../work/foreignrepo`: `git init -q -b master`; `git rev-parse --show-toplevel` printed
`/fast/scratch/hyaku/kengaku-r75/MutantBatteryR75/work/foreignrepo` (host-guard assert) before
each mutating op; config user, `SKILL.md` added, root commit `0e658ca0c5a9ca47977e04f65de18da704e6a551`
on master; orphan root via `commit-tree` of the empty tree → `ee6dfa91d1ef46a42a9616f06e481da2a1a540c0`.
`../work/demo_foreign/{master-stamped,foreign}.txt` stamped with those hashes. No git op touched
the lane, the clone (beyond read-only queries), or anything outside the scratch root. Note: the
fixture lane trips an unrelated `D4 ERRATA:claims-doc-absent` defect (it has no registry); the
STAMPS leg's tallies are unaffected in both runs shown.

## 6. Restoration evidence

- After the final mutation, sha256 of both instruments equals the pristine snapshot hashes
  (§1). Both `--selftest` runs on the restored bytes reproduce the pristine baselines line for
  line (`cases=5 red=4 failures=0 ok=True` rc=0; `arms=4 failures=0 ok=True` rc=0), and the
  header reads `WORKTREE clean` again.
- `git status --porcelain --untracked-files=no | wc -l` → `0`; `git diff --stat | wc -l` → `0`.

## 7. Incidental observations (not mutant results)

1. At A1 the C2 verdict's stamp leg prints `STAMPS files=0 … not_ancestor=0` and still
   `PREDICATE R75-C2 pass` rc=0 — the claim's `K>0` clause is not enforceable by the instrument
   and would pass vacuously if the receipt directory were empty at scoring time. (`git ls-tree
   --name-only HEAD corpus/evidence/round75/` shows exactly one entry at A1 — `sources`, not a
   `.txt`; the receipts of record are wave products, present in the lane worktree as untracked
   files.)
2. The C1 battery's `red=4` is printed as `len(cases) - 1`; any drift in case count silently
   redefines "red". Cosmetic today; the golden-output arm above would pin it.

## 8. Bottom line

- C1: `SURVIVORS n=4` (M5, M7, M8, M9) of 9 — all in the `emit`/report surface the battery
  never executes; killed 5.
- C2: `SURVIVORS n=8` (N1, N2, N3, N4, N7, N8, N10, N12) of 11 — concentrated in the printed
  tallies (never re-derived), the stamp-leg red classes (never exercised red), and the
  null-measurement stub; killed 3 (N5, N6, N11 — the battery genuinely prices the S250 flip,
  containment direction, and off-target labelling).
- Every mutant lived in the scratch clone and was reverted before the next; the scratch root is
  deleted before this seat yields. The lane tree received zero edits from this seat.
