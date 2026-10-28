# C2ExecLedgerMerge — merged routed-findings ledger (R51, wave 1)

Seat: `C2ExecLedgerMerge` (executor). Lane: `/home/vgpnk/Projects/shokunin/kengaku-shokunin`.
Scratch: `/fast/scratch/hyaku/kengaku-r51/C2ExecLedgerMerge` (removed before yield, §7).

## 0. Axes named

- **adjacency (8→9)** — the axis this seat serves (R51-C2). Moves kept: a ledger whose every
  row names its owner and disposition, verified against the frozen counter.
- **freshness (8→9)** — R51-C1, not touched: this seat read `PROVINCE.md` only through
  `source` pointers, wrote nothing under `plans/` or `corpus/`.
- **operability** — held, not improved: the merge rule is documented in §3 and reproducible
  from the eight fragments plus the base ledger; the predicate now measures `pass` on the
  artifact.

Moves rejected because they harmed an axis: clobbering the L1's `integrate_ledger.py` output
without measuring it first (destroys a sibling artifact), and writing the working-tree
instrument's numbers as the claim's after-measurement (the instrument is modified, §4).

## 1. Revision measured

```
REV 4090c3db79d11279ab5e5121ba25e74aa316e6e7   (lane tip, branch master, working tree as found)
REV e07f131cf7037e58a21db6e1f3986cf401ad257c   (stage-1 freeze commit; instrument blobs read from it)
```

Digests of every artifact this report measures:

```
39fdef1e3fe06c6b75e63d363bd4420c87a830546e0fb1f4571e56b2a3d1cd7d  corpus/routed-findings.jsonl (base, 71 rows)
7bf2d00ccf35ce3ca9a62f1f72aaf2bb0ecb7ea7880b093a05bb927cae6e9b03  plans/round51_routing.py @ HEAD  (frozen instrument)
6f084fdfa3caf003c9e8580d96c4eb63e434f90b7cd9c1bdd8ca70619ad472ba  plans/round51_routing.py worktree (MODIFIED, §4)
08a8d2b0f5c138b00b798d22b4a5eab0d26fa86443f644af5c52ad49b7411b09  .ufo/waves/round-51/w1/C2ExecLedgerMerge.jsonl (my merge as delivered, 71 rows)
cc5acda17ad89c3ab08120959864525dca74909aaab3571421be7544c158a350  corpus/routed-findings.jsonl (L1 landing write, 75 rows, measured in §5a)
```

## 2. Item executed

Base `corpus/routed-findings.jsonl` + the eight fragments `w1/C2Exec<A..H>.jsonl` (all eight
landed; none missing), merged by id, original field order and values preserved, extras appended.

Fragment census at merge time (15:38:01):

```
A lines=9 mtime=15:28:22   B lines=9 15:30:56   C lines=9 15:28:14   D lines=9 15:26:46
E lines=9 mtime=15:33:02   F lines=9 15:22:04   G lines=9 15:26:02   H lines=8 15:34:58
```

7×9 + 8 = 71 rows, matching the item ranges (A 0..8 … H 63..70). A bounded watcher recorded
the arrival order (`present=F` at 15:23:57 → `ALL PRESENT` at 15:30:37); `H` was rewritten
afterwards at 15:34:58, and the merge was re-run against that final content.

Merge verifier output, verbatim:

```
BASE rows=71 unique=71
FRAGMENTS present=8 A B C D E F G H
FRAGMENTS missing=0 -
FRAGMENT rows applied=71
MERGED rows=71 unique=True order_ok=True count_ok=True
MERGED jsonl_reparse_ok=True out=.../C2ExecLedgerMerge.jsonl
FIELD-DIFFS 71
FIELD-LOSSES 0
ATTRIBUTED owner=71/71
DISPOSITIONS accepted-risk=24 fixed-historical=3 fixed-verified=42 refused-out-of-scope=2
MERGE ok
```

## 3. Verification (every item clause)

| clause | measurement |
|---|---|
| JSONL parses | `jsonl_reparse_ok=True` on the written file; 71 lines re-parsed |
| 71 rows | `rows 71` |
| ids unique | `unique 71` |
| same order as base | `order==base True` (ids byte-equal to base sequence) |
| no original field value lost | **71 diffs, all on `check`; 0 losses** — every non-empty original value survives; `FIELD-LOSSES 0` |
| full field set | `fields complete True` (all 11 frozen fields on all 71 rows) |

Original-field diff summary (`diff every original field`, base → merged):

- `check`: 71 rows changed — **61 rewritten** (lane-anchored to `$LANE`, so the frozen counter's
  scratch cwd cannot change the result) and **10 authored** where the base had none
  (`R40-R5, R42-R3-09, R42-R3-33, R42-R3-34, R42-R3-35, R42-R3-37, R45-S5-7b..7e` — the ten
  `CHECKS absent=10` rows of the before receipt).
- `status`: 0 changes. `close`: 0 changes. `blocker`, `note`, `class`, `source`,
  `opened_round`, `id`: 0 changes each.

Fields added (union over rows): `owner` 71/71, `disposition` 71/71, `next` 3,
`evidence` 9, `w1_check_note` 9.

## 4. Predicate measurements (frozen command, faithful copy)

The lane's working tree carries **untracked** files (`.ufo/waves/…`, `corpus/evidence/round51/`)
and **modified** tracked files that a plain `git clone --shared` lacks, so a bare clone
mis-measures `SOURCE`/`CLOSE_REF`. Measurement lane: shared clone at the tip, overlaid with
`rsync -a --exclude .git <lane>/ <clone>/`, ledger substituted, checks run with `TMPDIR` and
`--scratch` inside my scratch dir.

**A. frozen instrument (`git show HEAD:plans/round51_routing.py`), my 71-row merge — PASS**

```
LEDGER corpus/routed-findings.jsonl rows=71
FIELDS complete=71 incomplete=0
OWNERS attributed=71 unattributed=0
DISPOSITIONS set=71 bad=0
SOURCES resolved=71 missing=0
CHECKS present=71 absent=0
VERIFIED ran=42 passed=42 failed=0
CLOSE_REFS resolved=3 missing=0
NEXT violations=0
PREDICATE R51-C2 pass
```
exit 0. This is the artifact written to `w1/C2ExecLedgerMerge.jsonl` (sha `08a8d2b0…`).

**B. frozen instrument, the L1 integrator's 75-row file — FAIL**

```
LEDGER corpus/routed-findings.jsonl rows=75
VERIFIED ran=41 passed=36 failed=5
SOURCES resolved=74 missing=1
  DETAIL SOURCE R51-R2 source 'corpus/lessons/round-51.md' does not resolve
  DETAIL CHECK_FAILED R42-R2 fixed-verified but check exits nonzero
  DETAIL CHECK_FAILED R45-S5-4 fixed-verified but check exits nonzero
  DETAIL CHECK_FAILED R45-S5-5 fixed-verified but check exits nonzero
  DETAIL CHECK_FAILED R45-S5-6 fixed-verified but check exits nonzero
  DETAIL CHECK_FAILED R45-S5-7a fixed-verified but check exits nonzero
PREDICATE R51-C2 fail
```

**C. working-tree instrument, same 75-row file — FAIL with one failure masked**

```
VERIFIED ran=41 passed=40 failed=1
PREDICATE R51-C2 fail
```

**D. control 5 (do-nothing, base tip, frozen instrument) — FAIL, reproduces the recorded before**

Summary block byte-identical to `.ufo/waves/round-51/claims/c2-before.txt`
(`diff` reports only the DETAIL lines the committed receipt omits):

```
LEDGER corpus/routed-findings.jsonl rows=71
FIELDS complete=0 incomplete=71
OWNERS attributed=0 unattributed=71
DISPOSITIONS set=0 bad=71
SOURCES resolved=71 missing=0
CHECKS present=61 absent=10
VERIFIED ran=0 passed=0 failed=0
CLOSE_REFS resolved=0 missing=0
NEXT violations=0
PREDICATE R51-C2 fail
```

## 5. Findings for the L1 (measured, decision-relevant)

**F1 — the frozen counter is modified, uncommitted, in the lane working tree.**
`plans/round51_routing.py` differs from HEAD (`git diff HEAD -- plans/round51_routing.py`,
+13/−5, sha `6f084fdf…` vs `7bf2d00c…`):

1. `load_owners()` widened: `shokunin.conf` parsed as `id|repo|axes` rows instead of block
   headers, **plus every on-disk `*-shokunin` directory** — the owner universe now admits any
   directory name.
2. check runner `cwd` moved from the scratch dir to **the lane root**, timeout 60→90 s. The
   claims doc freezes "a 60 s timeout each in a scratch cwd"; this is the opposite.
3. `--ledger` now `.resolve()`d.

Effect measured: run C vs run B — the edit converts 4 of 5 failing checks to passing, i.e. it
masks exactly the `R45-S5-4/5/6/7a` rows whose checks are not lane-anchored. The before receipt
was produced with the frozen version; an after measured with the working-tree version would not
be comparable. **Revert or commit deliberately before landing.**

**F2 — the output path is shared with the L1 integrator; my file was superseded twice.**
`.ufo/waves/round-51/integrate_ledger.py` (written 15:33:50) writes the same path. Timeline
measured: L1 run 15:34:04 (75 rows) → my verified merge 15:38 (`08a8d2b0…`, 71 rows) → L1 re-run
15:38 (75 rows, `cc5acda1…`) → landed into `corpus/routed-findings.jsonl`. The first L1 run
dropped fragment fields (`evidence` 9, `w1_check_note` 9) and diverged on `check` 4; the current
integrator **carries them verbatim**. Against my merge the landed rows differ on exactly two
fields — `next` 25 (integrator fallback `kengaku round 52 backlog`) and `disposition` 7:

```
R42-R3-01  fixed-historical -> fixed-verified
R42-R3-03  fixed-historical -> fixed-verified
R42-R3-04  fixed-historical -> fixed-verified
R42-R3-33  fixed-verified   -> accepted-risk
R42-R3-34  fixed-verified   -> accepted-risk
R45-S5-7b  fixed-verified   -> accepted-risk
R45-S5-7d  fixed-verified   -> accepted-risk
```

`check`, `close`, `status`, `note`, `evidence`, `w1_check_note` are byte-identical to my merge on
all 71 rows. Both directions of the disposition delta are the L1's policy call, and they are the
conservative direction: nothing is upgraded to `fixed-verified` that the frozen run does not
re-derive (run E, §5a).

**F3 — the adjacency signal is carried only by the four appended R51 rows.**
The 71 base rows are attributed `owner=kengaku` on 71/71, with `routed`/`referral` = 0 — the
schema is complete but the axis's own signal ("cross-domain evidence is named with its owner and
routed, not absorbed") is not exercised by them. The four appended rows are the round's only
cross-domain attribution (`kama` ×2, `protocol`, `unowned:integrator`; `routed` 4). Landing them
prints `rows=75` against the claims' after target `rows=71`, so the L1 must either amend that
line of the claim or record the four rows elsewhere; the predicate itself does not count rows
(run E prints `pass` at 75).

**F4 — one unexplained read.** The first read of `corpus/routed-findings.jsonl` (15:22, mtime
15:22:02) returned 0 rows from a 48 957-byte file; an immediate re-read returned 71. Not
reproduced in any later read. Recorded as an observation, not a claim.

## 5a. Landed state, measured (15:39, frozen instrument)

The L1's landing write (`corpus/routed-findings.jsonl`, 75 rows, sha `cc5acda1…`), same
overlay lane, frozen instrument restored from HEAD, `--run-checks`:

```
LEDGER corpus/routed-findings.jsonl rows=75
FIELDS complete=75 incomplete=0
OWNERS attributed=75 unattributed=0
DISPOSITIONS set=75 bad=0
SOURCES resolved=75 missing=0
CHECKS present=75 absent=0
VERIFIED ran=41 passed=41 failed=0
CLOSE_REFS resolved=0 missing=0
NEXT violations=0
PREDICATE R51-C2 pass
```

`corpus/lessons/round-51.md` (5655 bytes, 15:37) now resolves, so the `R51-R2` source miss of
run B is closed. `routed` 4 rows each name a non-`kengaku` owner and a `next`. The five
`fixed-verified` failures of run B are gone because the landed rows use the fragments' checks
and the conservative dispositions above.

## 6. Limits

- Measured on a working-tree overlay of the lane, not on a committed landing tip; the predicate
  must be re-measured by the L1 in a clean clone after landing (the clone needs the untracked
  `.ufo/…` and `corpus/evidence/round51/` trees, or `SOURCE`/`CLOSE_REF` will under-report).
- Checks were executed as the fragments wrote them; this seat did not audit whether a green
  check re-derives its row's claim — `C2CritChecks`, `C2CritDisposition`, `C2CritSpotAttribution`
  own that.
- The `fixed-verified` results (42 in my merge, 41 in the landed ledger) are point-in-time at tip
  `4090c3d` with `TMPDIR` in my scratch.
- `evidence` / `w1_check_note` (9 rows each) are carried as fragment-authored prose; I did not
  verify their statements.
- No tool was installed or upgraded (no channel, version or reason to record).

## 7. Scratch

`/fast/scratch/hyaku/kengaku-r51/C2ExecLedgerMerge` (clone 613 MB, receipts, merge scripts) is
removed before yield; receipts are quoted verbatim above, so nothing citable lives only in
scratch. Free space seen: `/fast 804G total, 250G used, 555G avail (32%)`.

VERDICT: PASS — all eight fragments merged into a 71-row ledger with unique ids, base order
preserved, 71 `check`-only original-field diffs and 0 field losses, full 11-field set on every
row, JSONL re-parses; that merge printed `PREDICATE R51-C2 pass` (42/42 checks, 0 missing
sources, 0 close-ref misses, 0 NEXT violations) under the **frozen** instrument at `4090c3d`,
while the L1's then-current 75-row integrator output failed it (5 checks) and the lane's
working-tree instrument is modified in a way that masks 4 of those 5 (F1). The L1 has since
re-run the integrator on my rows (checks, close, status, note, evidence byte-identical) and
landed 75 rows that print `PREDICATE R51-C2 pass` with 41/41 checks (§5a); two items stay open
for the L1: revert or deliberately commit the modified `plans/round51_routing.py` (F1), and
reconcile the landed `rows=75` with the claim's after target `rows=71` (F3).
