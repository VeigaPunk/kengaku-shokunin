# R40MutC2Counter — mutation test of `plans/round40_c2_verify.py` (C2 counter)

Round 40 wave 1, 2026-10-26. Seat: mutation-tester, leaf. Scratch `/fast/scratch/hyaku/kengaku-r40/R40MutC2Counter` (deleted at end; receipts copied first).

## 1. Setup

`R40PkgEntry/` drafts were absent at start, so a minimal genuine package was built in a `git clone --shared` of the lane (`3077adb`): entry `corpus/knowledge/tb2-db-wal-recovery-grader.md` (16 located quotes over the two pinned captures, derived requirement map, negative space), SOURCES rows S119/S120 (11 cells each, single `sha256` anchor token at the spec pins), README index row + coverage bullet; the entry was staged index-only for the gate's P9. No frozen file was touched at build time.

Baseline on the pristine package clone (`python3 plans/round40_c2_verify.py --lane $S/lane`, runs/baseline.txt):

```
V1 ok … V7 ok rows=6 tags=6 bad=0
checks=7 defects=0
PREDICATE C2 pass        exit=0   (wall 4.1 s)
```

Every mutant below was applied to the clone (never to the lane, never to the frozen counter/gate/probe bytes), one at a time, and the counter run to completion. Expected detectors were derived from the counter source (plans/round40_c2_verify.py:54-248).

## 2. Mutants

| # | Mutant (file, change) | Expected | Observed (DEFECT lines) | Verdict | Restoration |
|---|---|---|---|---|---|
| M1 | entry: map label flipped, `json-at-path` `enforced`→`unenforced` | V7 | `V7 DEFECT … bad=['json-at-path: labelled unenforced, receipt derives enforced']`, `defects=1`, exit 1 | **caught** | entry sha256 `fe9ed1a8…` re-verified |
| M2 | entry: `json-at-path` row cites `oracle-solve-sh` (its `violates=` is empty) | V7 | `V7 DEFECT … bad=['json-at-path: cites no case or a case that does not violate it']`, exit 1 | **caught** | entry sha256 re-verified |
| M3 | entry: tag duplicated (`sorted-by-id` row twice) | V7 | `V7 DEFECT rows=7 tags=6 bad=["tags missing=0 duplicated=['sorted-by-id']"]`, exit 1 | **caught** | entry sha256 re-verified |
| M4 | entry: tag missing (`eleven-records` row deleted) | V7 | `V7 DEFECT rows=5 tags=6 bad=["tags missing=['eleven-records'] duplicated=0"]`, exit 1 | **caught** | entry sha256 re-verified |
| M5 | entry: map line number wrong (`instruction.md:9`→`:8` on json-at-path row) | V7 | `V7 DEFECT … bad=['json-at-path: line 8 is not the frozen instruction.md:9']`, exit 1 | **caught** | entry sha256 re-verified |
| M6 | SOURCES.md: S119 anchor token replaced by S120's digest (`88dc5c2a…`→`5a203751…`) | V3 | `V3 DEFECT rows=2 bad=['S119:anchor_digest']`, exit 1; V2 stays ok (gate P6 does not read the anchor cell) | **caught** | SOURCES sha256 `9aa4ae9c…` re-verified |
| M7 | receipt: one CASE line deleted (`truth-value-string-id4`) | V2 (gate P10) + V4 | `gate: P10 DEFECT fresh probe output is not byte-equal to the receipt`; `V2 DEFECT … gate_exit=1`; `V4 DEFECT cases=27 … bad=['case ids differ from the frozen table', 'summary disagrees with the CASE lines']`, `defects=2`, exit 1 | **caught (×2)** | receipt sha256 `c74c6b91…` re-verified |
| M8 | spec: one byte (`"min_quotes": 8`→`9`) | V2/V3/V7 (spec digest) | `V2/V3/V4/V7 DEFECT error ValueError: spec template not at its freeze digest`, `defects=4`, exit 1 | **caught (×4)** | spec sha256 `4af78f4f…` re-verified |
| M9 | dry table: one byte (`TAG fix-wal instruction.md:7`→`:8`) | V4/V5/V7 (digest) | `V4 DEFECT error ValueError: dry table not at its freeze digest`; `V5 DEFECT probe or dry table not at freeze digest`; `V7 DEFECT error ValueError: dry table not at its freeze digest`, `defects=3`, exit 1 | **caught (×3)** | dry sha256 `688f3475…` re-verified |
| M10 | probe: one docstring byte (`probe:`→`probE:`; behaviour-preserving) | V2 (gate P1) + V5 | `gate: P1 DEFECT pinned=2 mismatched=['plans/db_wal_probe.py']`; `V2 DEFECT … gate_exit=1`; `V5 DEFECT probe or dry table not at freeze digest`, `defects=2`, exit 1 | **caught (×2)** | probe sha256 `69af65df…` re-verified |
| M11 | capture: one byte in `task.toml` (`medium`→`medirum`) | V1 (+V2 via gate P5) | `V1 DEFECT listed=8 bad=['task.toml'] extra=0`; `gate: P5 DEFECT … task.toml: manifest digest does not match the bytes`; `V2 DEFECT … gate_exit=1`, `defects=2`, exit 1 | **caught (×2)** | task.toml sha256 `1cdc2c61…` re-verified |

Total: **11 mutants, 11 caught, 0 survived**. Every run ended `PREDICATE C2 fail`, exit 1.

## 3. Reading (coverage findings, not contract changes)

- The six requirement-map defects (M1-M5) are all V7's alone; the gate never reads the map. The anchor-token defect (M6) is V3's alone — the gate's P6 ignores the anchor cell. This is the documented division of labor (counter docstring: V3 = round-37 D3, V7 = round-37 D2); it means a package could not pass the gate alone, which is why the counter, not the gate, is C2's instrument.
- The receipt is intentionally digest-free in the counter (P2 filled at run time) and its two detectors are independent: a fresh probe re-run (gate P10 byte-compare) and the frozen-table reconciliation (V4). M7 fires both, so deleting a CASE line cannot slip through either the frozen table or the re-run.
- One-byte mutants of any pinned instrument are fail-closed: the digest guard raises inside `spec()`/`dry()` and the counter's main() converts every raise into a DEFECT (`a check that cannot run is a defect, never a pass`), fanning M8 to 4 detectors and M9 to 3. No mutant turned a check green.
- Residual coverage gap (named, not fixed): all 11 mutants corrupt a value the counter reads; none exercises V4's `match=NO` naming clause (the frozen receipt has `mismatches=0`, so no fixture exists that could), nor V6's census failure path beyond what a SOURCES edit would cause. V1's `extra=` clause (an unlisted capture file) and the gate's P8 knowledge/index mismatch are likewise unexercised by this list — the task's 11 mutants are all caught, and these clauses stay untested by choice (no frozen artifact may be fabricated).

## 4. Restoration evidence

After M11, in the clone (`sha256sum -c` against the pre-mutation digest list):

```
corpus/knowledge/tb2-db-wal-recovery-grader.md: OK   corpus/SOURCES.md: OK   corpus/README.md: OK
corpus/evidence/round40/db-wal-probe.txt: OK   corpus/evidence/round40/db-wal-dry-cases-freeze.txt: OK
plans/pkg-spec-r40.json: OK   plans/db_wal_probe.py: OK   …/tb2-db-wal-recovery/task.toml: OK
```

`git status --short` identical to pre-mutation state (` M corpus/README.md`, ` M corpus/SOURCES.md`, `A  corpus/knowledge/tb2-db-wal-recovery-grader.md`), and the pristine re-run printed `checks=7 defects=0` / `PREDICATE C2 pass`, exit 0 (runs/post-restore-baseline.txt). The lane itself was never modified: every path written was under `/fast/scratch/hyaku/kengaku-r40/R40MutC2Counter/` plus this report and its receipts dir.

## 5. Receipts

Per-run full counter outputs: `.ufo/waves/round-40/build/R40MutC2Counter/runs/` — `baseline.txt`, `m01-label-flip.txt`, `m02-nonviolating-cite.txt`, `m03-tag-duplicated.txt`, `m04-tag-missing.txt`, `m05-line-wrong.txt`, `m06-anchor-swap.txt`, `m07-case-deleted.txt`, `m08-spec-byte.txt`, `m09-dry-byte.txt`, `m10-probe-byte.txt`, `m11-capture-byte.txt`, `post-restore-baseline.txt`.

Tools installed: none (none needed; no pacman touched).

VERDICT: c2-mutants-11/11
