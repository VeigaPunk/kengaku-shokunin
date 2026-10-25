# R33FControl — C1 frozen control receipt mismatch

**Seat:** KengakuR33.R33FControl · **Target:** C1 control description (`plans/round-33-claims.md:57-59`) vs committed receipt (`.ufo/waves/round-33/claims/control-nothing.txt`).
**Method:** read-only lane access; all mutations confined to `/tmp/r33f-control` (fresh sandbox, `git -C <lane> archive` into it). No lane file, index, or git state touched except this report.

## Q1 — Does the control print `entries=0` or `entries=1`?

**`entries=1`.** The frozen sentence is wrong; the committed receipt is right.

- Frozen claim, `plans/round-33-claims.md:57-59`: "the same counter on the pre-append tree prints `entries=0 …` and exits 1".
- Committed receipt, `control-nothing.txt:5-6` (created only at `f0b20ae`, "round-33: frozen claims, counters, freeze controls"; worktree bytes identical to `f0b20ae`, sha256 `2adeefd768764064270615422037c3f1ad1e8434aa3cfe37ae3f5728ed3ef480` both):
  ```
  entries=1 indexed=1 cited_rows=3 rows_present=3 rows_mined=1 usedby_ok=0 census=ok
  exit=1
  ```
- First-hand rerun at the freeze tree, sandboxed (`git -C kengaku-shokunin archive f0b20aea | tar -x -C /tmp/r33f-control/f0b20aea`, then inside it):
  ```
  $ python3 plans/adoption_check.py --expect .ufo/waves/round-33/claims/adoption-expect.json --census
  entries=1 indexed=1 cited_rows=3 rows_present=3 rows_mined=1 usedby_ok=0 census=fail
  EXIT=1
  ```
  All six content fields and the exit reproduce exactly; `census=fail` vs the receipt's `census=ok` is a sandbox artifact: `plans/adoption_check.py:35,132-141` shells out to the fleet-root census (`sources-census.sh validate --root <lane.parent> <lane_name>`), which cannot pass under `/tmp`. The receipt's `census=ok` was measured in the real lane root and is environment-bound, not tree-bound (same artifact observed by R33ReconRegistry on HEAD-only archives).
- Pinned hash checks out: receipt pins `expect_sha256=fbd7b47ededdfe251465c13ee1c2b758453f2b691bc0639d8a74df3e0752a214`; recomputed over both the worktree and `f0b20ae:.ufo/waves/round-33/claims/adoption-expect.json` — identical match. The receipt was not edited after freeze.

**Provenance of the drift:** the sentence is round-32's verbatim. `.ufo/waves/round-32/claims/control-nothing.txt:5` reads `entries=0 indexed=0 cited_rows=0 rows_present=0 rows_mined=0 usedby_ok=0 census=ok` — a genuinely empty pre-draft tree. Between that round-32 freeze and the round-33 baseline, commit `bcd2a6c` created the draft `corpus/knowledge/benchmark-grader-semantics.md`, its `README.md:67` index row, and the S094/S097 `rejected` rows. I confirmed the drift is not even commit-boundary sensitivity: the same counter on the baseline tip `112091c2` (expect file transplanted from `f0b20ae`, since the expect file exists only from `f0b20ae`) also prints `entries=1 indexed=1 cited_rows=3 rows_present=3 rows_mined=1 usedby_ok=0 census=fail`, `EXIT=1`. No tree reachable from the round-33 baseline prints `entries=0`.

**Decode of the six fields at freeze** (why `rows_present=3` with zero S103/S104 rows — the registry at `f0b20ae` has 95 rows, max S102, and no S103/S104 row in any indentation): the draft entry still cites the refused ids `source: S093/S094/S097` (`benchmark-grader-semantics.md:1-3`); S094/S097 exist as `rejected` rows, S093 as `mined`. Hence `cited_rows=3 rows_present=3 rows_mined=1`; `usedby_ok=0` because the expect file declares sources S093/S103/S104 and S103/S104 are absent from the registry, failing the all-of linkage.

## Q2 — Does it falsify the frozen target despite the mismatch?

**Yes.** The frozen predicate (`plans/round-33-claims.md:51-52`) requires `entries=1 indexed=1 cited_rows=3 rows_present=3 rows_mined=3 usedby_ok=1 census=ok` **and exit 0**. The do-nothing tree delivers `rows_mined=1 usedby_ok=0` and `exit=1` — three independent clauses fail, so the counter rejects the do-nothing world. `entries` was never a discriminating clause for C1: the predicate pins `entries=1` in the after-state too. The mismatch damages the *description* of the control, not its falsifying power.

## Verdict

**Caught (record defect; control itself valid).** The frozen C1 control sentence (`plans/round-33-claims.md:58`) misstates the measured output of the receipt it cites in the same sentence: claimed `entries=0`, actual `entries=1 … rows_mined=1 usedby_ok=0 census=ok`, `exit=1`. Number-drift from round-32's verbatim sentence; the committed receipt is faithful, hash-pinned, and unmodified since `f0b20ae`. C1's falsification logic survives intact — the do-nothing control still exits 1 on `rows_mined`, `usedby_ok`, and the exit code.

## Residual risk and verification gaps

- The census clause of the frozen predicate (`census=ok`) is only reproducible at the real fleet root; sandbox re-verification can confirm the six content fields and exit but not that field. Not a receipt defect — a measurement-environment coupling worth knowing for any future offline re-run.
- `entries=1 indexed=1` at the pre-append tree means the "new corpus bytes" framing of C1 is partly pre-staged (draft entry + index row pre-exist); the genuinely moving clauses are `rows_mined` (1→3), `usedby_ok` (0→1), and exit (1→0). Sibling seats (R33ClaimsReview's S093 used-by finding) cover the adjacent S093 transition claim; not re-litigated here.
- The `112091c2` measurement transplanted the `f0b20ae` expect file (that file does not exist before the freeze commit); the transplanted measurement is a reconstruction, the `f0b20ae` measurement is not.
