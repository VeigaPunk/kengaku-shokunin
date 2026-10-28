# R49C2MutDup — duplicate/remove one frozen case; does the counter inventory catch count drift?

Seat: R49C2MutDup (mutation-tester), kengaku round 49 wave 1, serving R49-C2 (coverage).
Date: 2026-10-28. Item: *duplicate or remove one frozen case; test whether the counter inventory catches
count drift.* Axes: coverage (mutation-sensitivity of the frozen-case inventory); no other axis touched.

## Freeze verification (precondition for any scored run)

- `git -C <lane> cat-file -t 9d2900af41e4d1fc6022eff99010436fde6dbd93` → `commit`;
  `log -1 --format='%H%n%ci%n%s'` → `2026-10-28 09:14:40 -0300`, "round-49: stage-1 freeze of C1 … and C2
  (TB2 grader admission, Q40 counter, receipt ordering) claims".
- `git merge-base --is-ancestor 9d2900af… master` → YES. Commit predates this measurement (first detector run
  ≈09:2x−03:00). Blocker absent → scored runs permitted.
- One live clone: `git clone --shared <lane> <scratch>/clone` + `checkout 9d2900af…`; HEAD verified
  `9d2900af41e4d1fc6022eff99010436fde6dbd93`; `git rev-parse --show-toplevel` asserted equal to the clone dir
  before every write/restore. Clone status `--porcelain` empty before baseline and after each restore.

## Detector (bounded)

The r49 counter `plans/round49_c2_verify.py` is not in the frozen tree (stage-2 pin). The frozen claims
declare the r49 counter to be `plans/round46_c3_verify.py` (digest-pinned, imported) plus deltas, so the
detector is that committed module **unmodified** (sha256
`a971c24dd5d0cb880e97ad4dd80315fcf58afaa02f8cffb5cc2e803aa292a8d4`), imported by a scratch driver that runs
exactly the inventory legs **V3, V4, V5, V7, V9, V10**. Excluded: V2 (would run `pkg_gate.py --rerun`, the
P10 fresh-probe leg — forbidden pre-receipt by the frozen Q30 ordering; verified at counter lines 250–263),
V11 (bubblewrap grader run, unrelated to count drift), V1/V6/V8/V12/V13 (do not read the frozen case
inventory). Leg output format and notes are produced by the counter's own `run_legs()`.

Driver (scratch-only, transcribed; scratch now removed):

```python
import pathlib, sys
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / "clone" / "plans"))
import round46_c3_verify as C  # committed bytes, unmodified
lane = HERE / "clone"; pkg = C.real_pkg(lane)
work = HERE / "work"; work.mkdir(parents=True, exist_ok=True)
res = C.run_legs(lane, pkg, work, ("V3", "V4", "V5", "V7", "V9", "V10"))
defects = sum(1 for _n, ok, _note in res if not ok)
print(f"checks={len(res)} defects={defects}")
print(f"PREDICATE C3 {'pass' if defects == 0 else 'fail'}")
sys.exit(0 if defects == 0 else 1)
```

Inventory under test: `corpus/evidence/round46/polyglot-c-py-dry-cases-freeze.txt`, pristine sha256
`99adfea6bd404b469a58a7fe8a6f44a3cc0a5b035fc589d1f5a4e58cb9489536` (equals the counter's `DRY_SHA256` pin),
7 TAG rows + 18 CASE rows + footer `cases=18 predicted_pass=7 predicted_fail=11`.

Known-bad baseline: the committed r46 state carries the V7 unsatisfiable-tag defect
(`both-print`/`toolchain` no violating case). Per protocol a baseline failure is inconclusive, so the kill
criterion is the **delta**: a mutant is killed iff it ADDS defects naming the count drift AND the restored
run is byte-identical to pristine.

Pre-registered predictions: any single-CASE add/remove flips V4 (id-list order + summary arithmetic),
V5 (digest pin), V10 (DECISIVE key set); V7 unchanged (TAG rows untouched); V3/V9 unchanged.

## Runs (verbatim transcripts: `.ufo/waves/round-49/w1/R49C2MutDup-runs.txt`)

**Pristine** — `V3 ok rows=7`, `V4 ok cases=18`, `V5 ok probe=frozen dry_byte_equal=True`,
`V7 DEFECT … tags missing=['both-print', 'toolchain'] …`, `V9 ok case_rows=18/18`,
`V10 ok mechanism_rows=18/18` → `checks=6 defects=1`, `PREDICATE C3 fail`, rc=1 (re-derived).

**M1 — remove one frozen case** (`CASE value-plus-line`, the sole `stdout-only` violator; table sha256
`8e3958ad6f75d5f1d136c483bd50845cbd017a295ddc3a4df2a21cadb304cfe8`):

```
V3 ok rows=7 bad=0
V4 DEFECT cases=18 mismatches_named=0/0 bad=['case ids differ from the frozen table', 'summary disagrees with the CASE lines']
V5 DEFECT probe or dry table not at its freeze digest
V7 DEFECT rows=5 tags=7 bad=["unparsed row '| instruction.md:7 | both-print | not exercised | '", "unparsed row '| instruction.md:9 | toolchain | not exercised | n'", "tags missing=['both-print', 'toolchain'] duplicated=0"]
V9 ok case_rows=18/18 bad=0
V10 DEFECT DECISIVE keys differ from the frozen case ids (stage-2 pin not aligned)
checks=6 defects=4
PREDICATE C3 fail
```

**M2 — duplicate one frozen case** (same line twice; table sha256
`f03ead92c2311a68e43f37d71150e4be675551a6deb01bcea8ae11c89d3e6fe9`): identical leg pattern —
`V4 DEFECT … bad=['case ids differ from the frozen table', 'summary disagrees with the CASE lines']`,
`V5 DEFECT probe or dry table not at its freeze digest`, `V7 DEFECT` (unchanged),
`V10 DEFECT DECISIVE keys differ from the frozen case ids (stage-2 pin not aligned)` →
`checks=6 defects=4`, `PREDICATE C3 fail`.

## Restoration evidence

After each mutant: `git -C <clone> rev-parse --show-toplevel` asserted = clone dir, then
`git -C <clone> checkout -- corpus/evidence/round46/polyglot-c-py-dry-cases-freeze.txt`; table sha256
returned to `99adfea6…` both times; `git status --porcelain` empty; restored runs byte-identical to pristine
(`cmp` → equal, both after M1 and M2); final clone HEAD `9d2900af…`. Both predictions held exactly.

## Verdict

- **M1 (remove) KILLED** — new defects V4+V5+V10; V4 and V10 are substantive legs (V3/V4/V7/V9/V10/V12).
- **M2 (duplicate) KILLED** — same delta.
- The counter inventory catches count drift in both directions, behaviorally (V4 order+count+summary
  arithmetic; V10 set-equality) and by digest pin (V5). The surviving-baseline V7 defect is the known
  committed r46 state, present in pristine, mutant and restored runs alike — not caused by either mutant.

## Findings and limits

1. The dry table's own footer (`cases=18 predicted_pass=7 predicted_fail=11`) is parsed by **no** counter
   leg (`SUMMARY` regex reads only the receipt; `predicted_pass` appears nowhere in the counter). A drift
   confined to the frozen table's footer, with rows and receipt untouched, would flip only V5's digest pin —
   no behavioral count leg reads it. Residual coverage edge, not exercised further (beyond this item).
2. V7 is case-count-insensitive by design (TAG rows only) — consistent with the r49 V7 amendment, which adds
   violating cases, not counts.
3. Measured the declared imported base counter at the frozen base; the stage-2-pinned `round49_c2_verify.py`
   could re-implement these legs — unverifiable before stage 2 (no scored run of it exists yet).
4. V2/V11 not exercised (bounds above); V5's probe `--dry` ran (permitted pre-receipt) and was byte-equal in
   pristine/restored runs.
5. Usability note for the stage-2 `plans/mutants49/plan.json` battery: each of these two mutants flips two
   substantive legs, satisfying the V14 "flip at least one substantive leg" bar. No admission claimed.

## Discipline

- Lane untouched (read-only); only writes were this report, the sibling receipt file, and scratch (removed —
  `ls` confirms `/fast/scratch/hyaku/kengaku-r49/R49C2MutDup` absent). No git/jj mutation anywhere; no
  production file, wave peer path, or fleet-root file touched; no C1/C2 admission claimed.
- Sources opened: local lane files only (paths above, at commit `9d2900af…`); no web source opened, so no
  URL/quote entries are due.
- Tooling: nothing installed or upgraded; no pacman transaction attempted.

VERDICT: R49-C2 inventory count-drift probe — M1 remove KILLED, M2 duplicate KILLED (delta V4+V5+V10,
defects 1→4 each; baseline V7 unchanged; bytes restored hash-exact, outputs byte-identical to pristine);
counter inventory catches count drift.
