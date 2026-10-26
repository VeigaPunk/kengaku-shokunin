# R41RevC2Counter — review of `plans/round41_c2_verify.py` (C2 counter, wave 1)

Seat: R41RevC2Counter, 2026-10-26. Lane tip reviewed: `fc79f2a49be0221e138b3885fa0d83bc43b31a42` (clean clone at `/fast/scratch/hyaku/kengaku-r41/R41RevC2Counter/lane`, since deleted; every command below was run inside the mandated bwrap envelope unless marked host-side read-only). No tools installed. No lane file edited; scratch removed (`SCRATCH_CLEANED=yes`).

## 1. Is the re-pointing faithful? — YES, verified

Whole-file `diff -u plans/round40_c2_verify.py plans/round41_c2_verify.py` (run host-side, read-only) shows:

- V1–V7 bodies are byte-identical to round-40 except one line in V2: scratch filename `pkg-spec-r40-effective.json` → `pkg-spec-r41-effective.json`. No check is relaxed, weakened, or dropped.
- All changes are: docstring (r41 package, `checks=8`, V8 description, `--work` note), re-pointed constants (`CAP`, `CAPTURES` 8→10 files, `SPEC_REL/SPEC_SHA256`, `PROBE_REL/PROBE_SHA256`, `DRY_REL/DRY_SHA256`; `GATE_SHA256` unchanged `ea638822…` — same frozen gate, correct), new `ORDER_REL`/`CLAIMS_REL`, new `v8()`, and the `--work` mkdir.
- Every re-pointed digest was exercised green in the healthy run: `V1 ok listed=10 bad=0 extra=0` (all ten capture digests), gate `P1 ok pinned=2 mismatched=0` (probe+gate per spec), `V5 ok probe=frozen dry_byte_equal=True`, and `spec()`/V2's `SPEC_SHA256`/`GATE_SHA256` guards raised nothing (V3 parsed rows through `spec()`).
- Cross-check host-side: `sha256sum` on the lane worktree gives spec `8e96421d91080d220cd8976abf62a1499b8a1bc92eb5d36eb0f55179b065d0dd`, probe `8c471fbd0d83450793271d75fe3735a735226a725a73e0f16e02034e9d3c7242`, dry `a656ce9b9adb4e88bb49b6a8a45064a8c4f459cffbbf76d70cca7f43a0c77a03` — all equal the counter's pins.

## 2. Runs in my clone (pasted output)

Command (both runs): `bwrap … python3 plans/round41_c2_verify.py --lane <clone> --work <dir>`.

Run 1 (`--work "$S/w"`) and Run 2 (`--work "$S/absent/x"`) printed byte-identical output:

```
V1 ok listed=10 bad=0 extra=0
    gate: P1 ok pinned=2 mismatched=0
    gate: P2 ok receipt_sha256=pinned
    gate: P3 DEFECT no '## Located quotes' section
    gate: P4 DEFECT no parsed quote
    gate: P5 ok manifest_entries=10 bad=0 first=0
    gate: P6 DEFECT rows=2 bad=2 first=S122: rows=0
    gate: P7 DEFECT entry unreadable
    gate: P8 DEFECT index_rows=47 knowledge_files=47 bad=2 first=index rows for knowledge/tb2-constraints-scheduling-grader.md=0
    gate: P9 ok untracked=0 first=0
    gate: P10 ok probe_rerun=byte-equal bytes=5775
    gate: defects=5
V2 DEFECT spec=frozen gate=frozen gate_exit=1
V3 DEFECT rows=2 bad=['S122:row', 'S123:row']
V4 DEFECT receipt or entry absent
V5 ok probe=frozen dry_byte_equal=True
V6 ok census_exit=0
V7 DEFECT receipt or entry absent
V8 ok order_exit=0 result=PASS
checks=8 defects=4
PREDICATE C2 fail
RUN_EXIT=1
```

Reading: the four defects are exactly the wave-1 work not yet landed (entry file, S122/S123 SOURCES rows, README index rows) — the same shape the do-nothing control predicts, minus V8, which now passes because the receipt exists and is ordered. Gate `P10 ok probe_rerun=byte-equal bytes=5775` is the strongest honesty signal: a fresh in-counter run of the frozen probe reproduces the receipt byte-for-byte.

## 3. The `--work` fix — CORRECT

`plans/round41_c2_verify.py:288-289`: `if a.work: pathlib.Path(a.work).mkdir(parents=True, exist_ok=True)` before `TemporaryDirectory(prefix="k41-c2-", dir=a.work)`.

- Run 2 with `--work "$S/absent/x"` (both levels absent) ran to completion and created the dir (`ABSENT_DIR_CREATED=yes`).
- Contrast, same lane, round-40 counter: `python3 plans/round40_c2_verify.py --lane <clone> --work "$S/absent2/x"` → rc=1 with `FileNotFoundError: … '/fast/scratch/…/absent2/x/k40-c2-oc9fy26t'` — the D10(b) defect the fix names.
- Residual edges (not defects, fail closed): `--work ""` or `--work <existing file>` raise an uncaught `mkdir` exception before any check runs.

## 4. V8 soundness — two defects

`v8()` (`plans/round41_c2_verify.py:276-281`) runs the lane's `plans/order_check.py` with `--claims plans/round-41-claims.md --receipt <spec receipt>` and passes iff rc=0 and the exact line `ORDER RESULT PASS`. Both resolution paths (`repo_path`, `plans/order_check.py:83-90`) anchor relative paths at the lane root, so cwd cannot skew the check. `order_check` exits non-zero on every failure mode (fail-closed; SetupError → 2), so `v8` inherits that. Honest history verified: direct run printed `freeze=8ef8b4fc…`, `receipt_commit=f774a87ad0…`, `scanned commits=1 file_entries=16 distinct_blobs=16`, `ORDER RESULT PASS` — none of the 16 freeze-time claims/ blobs (incl. `c2-stage-check.txt`, the control outputs) shows an executed probe, so the disclosed pre-freeze `--dry`/`--stage-check` activity is correctly excused.

### D1 (main): V8 executes an unpinned instrument

`ORDER_REL` (`plans/round41_c2_verify.py:79`) carries no digest — unlike `GATE_SHA256`, `PROBE_SHA256`, `SPEC_SHA256`, `DRY_SHA256` — and `plans/order_check.py` (worktree digest `948d5e1d2b3429d76a598fd11c4b22856d9f43ec093efd2c6aa0025aa0fc6ecc`) is not on the frozen-paths list. Any edit of `order_check.py` between freeze and landing changes what V8 proves without tripping any check. Demonstrated in my clone (host-side import of the counter module, working tree only, restored after):

```
stub: printf '#!/usr/bin/env python3\nprint("ORDER RESULT PASS")\n' > plans/order_check.py
V8_ON_STUBBED_ORDER_CHECK = (True, 'order_exit=0 result=PASS')
restored: sha256 948d5e1d2b3429d7…
```

The same stub applied to the gate or probe is caught by V2/V5 pins; order_check is the one executed file with no pin. Fix: pin `ORDER_SHA256` in the counter (and list `plans/order_check.py` in the freeze).

### D2: clause-2 bypass — a receipt committed before the claims can pass via side-branch merge

`order_check` clause 2 (`# (2) pre-registration order…`, `plans/order_check.py`) only rejects when the receipt's first commit is an **ancestor of** the freeze commit. A receipt committed pre-freeze on a side branch is not an ancestor after a post-freeze merge, and clause 3's scan (`rev-list <receipt_commit> -- claims_dir`) sees no claims commits on the side history. Fixture (bwrap, scratch repo, all git calls `-C`):

- commit A `base` (10:00) → branch `side`; main: commit `freeze` adds `round-41-claims.md` (11:00); side: commit `receipt` adds the receipt (10:30, earlier author+committer dates); main: `merge --no-ff side` (12:00).
- Result: `ORDER RESULT PASS` (exit 0). A receipt committed before the freeze — with timestamps proving it — passes V8. Control fixtures behaved correctly: linear receipt-before-claims → `ORDER RESULT FAIL`; receipt+claims in one commit → `ORDER RESULT FAIL`; claims-then-receipt → PASS; pre-freeze claims/ blob containing `P10 ok …` + `CASE x … observed=…` → `ORDER RESULT FAIL` (clause 3 works when the history is reachable).

The gate's docstring names authorship-order as out of scope, but clause 2 exists precisely to catch provable pre-registration, and the merge vector defeats it while the DAG+dates prove it. Direction (L1's call, not edited by me): when not ancestor, compare `receipt_commit` against the merge-base with the freeze (receipt forked before freeze ⇒ reject), or require the receipt's first commit on the first-parent line after the freeze.

## 5. Robustness observations (no action)

- Fail-closed under missing inputs: my first run raced an external mid-run deletion of the scratch lane; every affected check DEFECTed (`sha256()` → `None` on `OSError`), `V6 census_exit=2`, gate P10 crashed → `gate_exit=1`, `PREDICATE C2 fail`, exit 1. No false green path found.
- `v8`'s `timeout=300` and all exceptions inside checks become DEFECTs via the generic `except` (counter `main()`), never passes.

## Findings summary

- D1 (main): V8 runs unpinned `plans/order_check.py`; stubbed file ⇒ `V8 = (True, PASS)` while all other instruments are digest-pinned. Pin it.
- D2 (medium): pre-freeze receipt on a side branch, merged post-freeze, passes clause 2 and clause 3 (fixture D PASS). Ancestor-only test is insufficient.
- Not defects: `--work` fix correct (proven both directions); re-pointing faithful and digest-verified; V2/V3/V4/V7 defects today are exactly the pending wave-1 entry/SOURCES/README work, with `P10 probe_rerun=byte-equal bytes=5775` confirming receipt honesty.

Residual risk: clause 3 is a token heuristic over claims/ blobs only (probe output committed outside `claims/` before the receipt is undetectable — named gate limit); `--work` edge inputs raise uncaught exceptions (fail closed). Verification gaps: I did not exercise the gate's P1–P10 internals beyond the counter's output, and fixture exit codes were observed via the printed `ORDER RESULT` lines plus code reading (the `tail` pipe masked rc; `v8` requires rc=0, so FAIL lines cannot pass).

VERDICT: c2-counter-defects-2
