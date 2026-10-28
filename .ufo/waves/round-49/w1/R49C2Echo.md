# R49C2Echo — echo-control critic report (coverage, serving R49-C2)

Axes named: **coverage** only. Item under test: *does copying dry-table output into the receipt satisfy the v4
counter?* No admission claimed for R49-C1 or R49-C2; no stage-2 counter exists yet, so the verdict below is
built from (i) the exact committed gate/order outputs measured on an echo control tree at the frozen base, and
(ii) the committed v3 leg functions (the legs v4 inherits verbatim by contract) replayed on the echo bytes.

## 0. Freeze gate (checked before any measurement)

```
$ git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin show -s --format='%H %cI %s' 9d2900af…
9d2900af41e4d1fc6022eff99010436fde6dbd93 2026-10-28T09:14:40-03:00 round-49: stage-1 freeze of C1 … and C2 … claims
```

`9d2900af…` is a commit object in the lane tree and predates every measurement here (all runs
2026-10-28, after ~09:14-03:00). `plans/round49_c2_verify.py` does **not** exist at the freeze or at lane tip
`af88aab1…` — it is a wave-1 artifact pinned at stage 2 — so **no scored v4 counter run was made**. What is
scored-classified here: committed gate/order_check runs on a control tree (permitted work, P10 disabled —
`--rerun` never passed, so the probe's graded path never ran), `probe --dry` (explicitly permitted
pre-receipt), and committed-function replay on committed/copied bytes.

Pinned instruments at `9d2900af…` (verified by `git show … | sha256sum`):

```
ea63882240e67e9906e481f3d652f94366c288dc91991bafbfcd651a766edd41  plans/pkg_gate.py
a971c24dd5d0cb880e97ad4dd80315fcf58afaa02f8cffb5cc2e803aa292a8d4  plans/round46_c3_verify.py
948d5e1d2b3429d76a598fd11c4b22856d9f43ec093efd2c6aa0025aa0fc6ecc  plans/order_check.py
67a8f4a68fcdf1904484853053e1565f95dce503105732f43102a9e64db85f26  plans/polyglot_c_py_probe.py
99adfea6bd404b469a58a7fe8a6f44a3cc0a5b035fc589d1f5a4e58cb9489536  corpus/evidence/round46/polyglot-c-py-dry-cases-freeze.txt
```

## 1. Echo control tree and transform

```
$ git clone --shared --quiet /home/vgpnk/Projects/shokunin/kengaku-shokunin ctl-echo
$ git -C ctl-echo checkout --quiet 9d2900af…        # rev-parse --show-toplevel asserted == ctl-echo
$ cp ctl-echo/corpus/evidence/round46/polyglot-c-py-dry-cases-freeze.txt \
     ctl-echo/corpus/evidence/round46/polyglot-c-py-probe.txt
$ git -C ctl-echo add corpus/evidence/round46/polyglot-c-py-probe.txt && git -C ctl-echo commit
REV 496140a090fb6a3e6900f812715588cd4e1f1d20   (child of 9d2900af…; REV_DIRTY 0; status --porcelain = 0 lines)
 transform diffstat: corpus/evidence/round46/polyglot-c-py-probe.txt | 54 +++++---  1 file, 26 insertions(+), 28 deletions(-)
```

Post-copy byte check: `sha256sum` of the receipt path and the dry table in the echo tree are identical
(`99adfea6…` both), i.e. the receipt literally *is* the dry-table output.

## 2. Verbatim dry-table-as-receipt: exact committed outputs

### 2a. Committed gate, P10 disabled, spec pinned at its frozen digest

`python3 ctl-echo/plans/pkg_gate.py package --root ctl-echo --spec ctl-echo/plans/pkg-spec-r46.json --require-clean-tree` →

```
P1 ok pinned=2 mismatched=0
P2 DEFECT receipt_sha256=99adfea6bd404b469a58a7fe8a6f44a3cc0a5b035fc589d1f5a4e58cb9489536
P3 ok rows=20 distinct_quotes=20 distinct_lines=20 out_of_word_range=0
P4 ok checked=20 bad=0 first=0
P5 ok manifest_entries=8 bad=0 first=0
P6 ok rows=7 bad=0 first=0
P7 ok source_lines=7 bad=0 first=0
P8 ok index_rows=53 knowledge_files=53 bad=0 first=0
P9 ok untracked=0 first=0
defects=1
EXIT=1
```

### 2b. Committed gate, P10 disabled, counter-style effective spec (receipt_sha256 := echo digest)

The counter's own V2 pattern recomputes `receipt_sha256` from the tree's current receipt bytes before invoking
the gate (`round46_c3_verify.py:255-260`; the spec's committed value is masked out of the digest check and
never compared to receipt bytes). With the effective spec the gate **fully accepts** the echo tree:

```
eff receipt_sha256=99adfea6bd404b469a58a7fe8a6f44a3cc0a5b035fc589d1f5a4e58cb9489536   [= dry-table digest]
P1 ok pinned=2 mismatched=0
P2 ok receipt_sha256=pinned
P3 … P9 ok            (all nine legs ok)
defects=0
EXIT=0
```

→ With P10 off, the gate is **not** the echo discriminator: a dry-table receipt sails through P1–P9 unchanged
from r48 (`R48C2ExecControls.md` §"Frozen V8 outcome, measured", same finding). The refusal must come — and
does — from the counter's content/ordering legs.

### 2c. Committed ordering gate on the echo tree

`python3 ctl-echo/plans/order_check.py --lane ctl-echo --claims plans/round-49-claims.md --receipt corpus/evidence/round46/polyglot-c-py-probe.txt` →

```
ORDER claims=plans/round-49-claims.md round=49 freeze=9d2900af41e4d1fc6022eff99010436fde6dbd93
ORDER receipt=corpus/evidence/round46/polyglot-c-py-probe.txt receipt_commit=8d7f74ce63c25ad200c69fe0d90158cc7099def6 claims_dir=.ufo/waves/round-49/claims/
ORDER FAIL freeze-contains-receipt 9d2900af… already has corpus/evidence/round46/polyglot-c-py-probe.txt
ORDER FAIL receipt-before-claims 8d7f74ce… is an ancestor of 9d2900af…
ORDER scanned commits=0 file_entries=0 distinct_blobs=0
ORDER FAIL freeze-contains-receipt receipt-before-claims hits=0
ORDER RESULT FAIL
EXIT=1
```

and the not-yet-existing r49 receipt path is a setup ERROR, never a pass:

```
ORDER ERROR receipt not committed in HEAD: corpus/evidence/round49/polyglot-c-py-probe.txt
ORDER RESULT ERROR
EXIT=2
```

### 2d. Committed receipt-parse legs replayed on the echo bytes

Loaded `plans/round46_c3_verify.py` (module) from the echo tree, constructed `Pkg` exactly as `real_pkg`
does, ran the receipt-reading legs:

```
receipt_cases parsed: 0                       (echo receipt = dry table)
receipt_cases parsed (real receipt): 18       (control: the committed r46 receipt parses fully)
violating coverage (real receipt): {'c-build': 2, 'fib-kth': 4, 'python-run': 1, 'single-file': 4, 'stdout-only': 1}
V4 DEFECT cases=18 mismatches_named=0/0 bad=['case ids differ from the frozen table', 'summary line count != 1']
V7 DEFECT rows=5 tags=7 bad=['single-file: no receipt case violates it', 'python-run: no receipt case violates it', 'c-build: no receipt case violates it', "unparsed row '| instruction.md:7 | both-print | not exercised | '", 'fib-kth: no receipt case violates it', 'stdout-only: no receipt case violates it', "unparsed row '| instruction.md:9 | toolchain | not exercised | n'", "tags missing=['both-print', 'toolchain'] duplicated=0"]
V9 DEFECT case_rows=18/0 bad=['case table rows=18 receipt cases=0 equal=False']
```

Exact mechanics of the refusal (committed code, `round46_c3_verify.py`):

- `receipt_cases` (line 307) accepts only `CASE <id> predicted=(pass|fail) observed=(pass|fail) …
  violates=…`. Dry rows carry `predicted=`, `tests=`, `regrade=`, `violates=` — **no `observed=`** — so a
  verbatim dry table yields `parsed_cases=0` while `ids` still lists the 18 case ids.
- `v4` (lines 313-344): `ids != frozen_ids or len(parsed) != len(ids)` fires (`0 != 18`) →
  `case ids differ from the frozen table`; the dry trailer `cases=18 predicted_pass=7 predicted_fail=11`
  does not match `SUMMARY` (`cases=… observed_pass=… observed_fail=… mismatches=…`) →
  `summary line count != 1`.
- `v7` (lines 374-413): zero parsed receipt cases → every mapped tag reports `no receipt case violates it`.
- `v9` (lines 423-453): receipt contributes 0 `observed=` case rows → `case_rows=18/0 equal=False`.

### 2e. Echo against the wave-1 amended dry table (the stage-2 shape)

The sibling executor's amended table (`.ufo/waves/round-49/w1/R49C2ExecCases/polyglot-c-py-dry-cases.txt`,
20 cases, adds `both-print-c-silent` and `toolchain-c23-bool`) keeps the **same row shape**
(`predicted=… tests=… regrade=… violates=…`, trailer `cases=20 predicted_pass=8 predicted_fail=12`). Copied
verbatim into the receipt it is refused identically: `receipt_cases` parses 0 rows, the trailer is not a
receipt summary, and the new `violates=both-print`/`violates=toolchain` **declarations are not receipt
violations** — v4's delta (a) V7P leg counts a tag as covered only by a committed receipt case citing it.
So the echo class survives the amendment verbatim: `parsed_cases=0`, `cited=0/7`.

### 2f. `--dry` reproduction (permitted leg)

`python3 ctl-echo/plans/polyglot_c_py_probe.py --lane . --dry` → exit 0, output **byte-equal** to
`corpus/evidence/round46/polyglot-c-py-dry-cases-freeze.txt` (cmp-clean, `99adfea6…`). This is exactly what
V5's `dry_byte_equal=True` clause measures, and it confirms the dry artifact is reproducible without any
graded run.

## 3. Could any echo variant satisfy the v4 counter? (strongest counterexample search)

The v4 counter = `round46_c3_verify.py` (digest-pinned, imported) + frozen deltas (a)–(f)
(`plans/round-49-claims.md` §C2). Against the echo transform, the refusal is **redundant** — every layer
independently refuses it:

| layer | echo outcome | mechanism |
|---|---|---|
| gate P1–P9, frozen spec | `defects=1` (P2 digest) | stale `receipt_sha256` pin |
| gate P1–P9, effective spec | `defects=0` — accepts | receipt digest is self-computed; see §4 finding |
| gate P10 (scored mode only) | would DEFECT | fresh probe stdout ≠ dry bytes |
| V4 | DEFECT | `observed=` absent → 0 parsed cases; dry trailer ≠ `SUMMARY` |
| V7 / V7P (delta a) | DEFECT | 0 violating receipt cases → all tags uncovered; dry `violates=` tokens don't count |
| V8 ordering (delta b) | DEFECT | echo first-commit is a stage-2 control commit, **not** the stage-3 commit descendant-of-stage-2; and the receipt lacks `CASE … observed=` lines |
| V9 | DEFECT | `case_rows=N/0 equal=False` |
| V13/V14/V15 | unaffected/inapplicable | filler battery, mutants and preconditions don't read receipt *content* this way |

The only theoretically live escape would be a probe whose `--dry` output already carried receipt-shaped
`observed=` rows plus an `observed_pass/observed_fail` trailer — at which point the "dry table" *is* a receipt
and the echo transform reduces to a path copy. That attack is blocked three ways in the frozen contract:
(i) V8 delta (b) requires the receipt's first-commit to be **the stage-3 commit** carrying `CASE … observed=`
lines — an echo committed at stage 2 on a control tree cannot be that commit, on any tree; (ii) the stage-2
`--stage-check` gate plus the probe's own docstring fix `--dry` as the *predicted*-only table, so emitting
`observed=` in `--dry` would falsify the probe control, not the counter; (iii) the claims freeze prohibits any
full probe run before stage 3, so the observed values needed to fabricate receipt-shaped dry rows cannot be
produced by the probe itself pre-receipt. No committed byte and no frozen delta provides an echo path to
`PREDICATE R49-C2 pass`.

## 4. Findings for the L1 (fixable now, cheap)

1. **P2 is structurally toothless inside the counter.** `v2` recomputes `receipt_sha256` from the tree's own
   receipt bytes; the spec's committed value is masked out of `SPEC_SHA256` and never compared to bytes
   (`round46_c3_verify.py:200-203,255-257`). Measured: committed spec → `P2 DEFECT …`, effective spec →
   `P2 ok receipt_sha256=pinned`, `defects=0`. The r49 spec candidate already fixes the shape —
   `receipt_sha256: "<PIN:stage-3>"` — but the counter should *also* fail a package whose receipt digest
   cannot be pinned at stage 2, i.e. V15 should require the `<PIN:stage-3>` slot to be filled by the stage-3
   commit's receipt digest at landing, not silently recomputed.
2. **Guard the row-shape invariant in the amended probe.** The whole echo class is dead only while
   `--dry` output cannot parse as a receipt. Add to the stage-2 `--stage-check` (or V15) a positive check:
   no `--dry` line may match the `CASE … observed=` receipt regex. That converts today's *incidental*
   discrimination into a stated one and closes the residual escape in §3 before it exists.
3. **Unparseable requirement-map rows confirmed present at the freeze.** The committed entry's
   `| instruction.md:7 | both-print | not exercised |` and `| instruction.md:9 | toolchain | …` rows do not
   match `MAP_ROW`'s `enforced|unenforced|partly` label set — re-observed live in §2d. Stage 2 must repair
   the entry rows *and* cite the two new cases (`both-print-c-silent`, `toolchain-c23-bool`), or V7/V7P
   cannot go green even with violating cases present.

## 5. Commands run (all inside `/fast/scratch/hyaku/kengaku-r49/R49C2Echo`, `TMPDIR` exported there)

- `git clone --shared --quiet <lane> ctl-echo`; `git -C ctl-echo checkout --quiet 9d2900af…`;
  `git -C ctl-echo rev-parse --show-toplevel` (asserted == `ctl-echo` before writes);
  `git -C ctl-echo add … && git -C ctl-echo -c user.name=… -c user.email=… commit`; `rev-parse HEAD` →
  `496140a090fb6a3e6900f812715588cd4e1f1d20`; `status --porcelain` → empty.
- `python3 ctl-echo/plans/pkg_gate.py package --root ctl-echo --spec ctl-echo/plans/pkg-spec-r46.json
  --require-clean-tree` → §2a, exit 1.
- `python3 ctl-echo/plans/pkg_gate.py package --root ctl-echo --spec eff-spec.json --require-clean-tree`
  (`eff-spec.json` = committed spec with `receipt_sha256` := echo digest `99adfea6…`) → §2b, exit 0.
- `python3 ctl-echo/plans/order_check.py --lane ctl-echo --claims plans/round-49-claims.md --receipt
  corpus/evidence/round46/polyglot-c-py-probe.txt` → `ORDER RESULT FAIL`, exit 1; same with
  `corpus/evidence/round49/polyglot-c-py-probe.txt` → `ORDER RESULT ERROR`, exit 2.
- `python3 ctl-echo/plans/polyglot_c_py_probe.py --lane . --dry` → exit 0, byte-equal to the frozen dry table.
- Python replay of committed legs `v4`, `v7`, `v9`, `receipt_cases` from `ctl-echo/plans/round46_c3_verify.py`
  → §2d.
- Read-only on the lane: `git show`/`git ls-tree`/`git log` at `9d2900af…` and tip `af88aab1…`; reads of
  `plans/round-49-claims.md`, `corpus/lessons/round-48-verifier-spotcheck.md`,
  `.ufo/waves/round-48/w1/R48C2{Echo,ExecControls}.md`,
  `.ufo/waves/round-49/w1/R49C2Exec{Cases,Spec}*`, `.ufo/waves/round-46/claims/control-c3-echo.txt`.

No `--rerun`, no full probe execution, no `--filler` run, no commit outside the scratch clone, no lane write.

## 6. Limits

- `plans/round49_c2_verify.py` does not exist; nothing above executes it. The v4 verdict is established from
  committed gate/order outputs plus the committed leg functions the v4 contract digest-pins, on the same
  transform the frozen echo control names; it is not a scored counter run and must be re-confirmed when the
  stage-2 counter lands.
- The amended dry table measured is the wave-1 candidate (`R49C2ExecCases`), not the stage-2 pin; its row
  shape (the only property the echo attack cares about) is what the claims freeze mandates.
- The echo transform targeted the round-46 receipt path (the only committed receipt slot). The r49 path
  (`corpus/evidence/round49/polyglot-c-py-probe.txt`) is the sibling spec's field; the analysis carries over
  unchanged — echo at that path is still missing `observed=` rows and cannot be a stage-3 first-commit.
- Sources: only lane files opened; no external URL fetched. The claims file records S166's pinned URL —
  `https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/polyglot-c-py/tests/test_outputs.py`,
  accessed by the lane 2026-10-28 (located quote ≤25 words:
  `test_cases = [(42, "267914296"), (10, "55"), (0, "0")]`) — cited here for provenance only, not re-opened.

## 7. Scratch

`/fast/scratch/hyaku/kengaku-r49/R49C2Echo` (clone + extracted instruments + `dry-out.txt`, `eff-spec.json`)
removed before yield; every cited output is copied verbatim into this report.

VERDICT: No — copying dry-table output into the receipt cannot satisfy the v4 counter. The echo is refused
redundantly: committed gate P2 under the frozen spec (measured `defects=1`, exit 1); committed ordering gate
(`ORDER RESULT FAIL`, freeze-contains-receipt + receipt-before-claims); and every receipt-content leg the v4
counter inherits (`V4` 0 parsed cases + wrong summary, `V7`/`V7P` all-tags-uncovered, `V9` case-rows 18/0),
plus v4's own V8 ordering (`first-commit` must be the stage-3 commit) and P10 byte-equality in scored mode.
The live finding is structural, not echo-shaped: with P10 disabled the committed gate *accepts* the echo tree
under the counter's self-computed `receipt_sha256` (measured `defects=0`, exit 0) — the refusal lives entirely
in the counter's content and ordering legs, so the stage-2 pin discipline in §4 items 1–2 is what keeps the
echo class permanently dead.
