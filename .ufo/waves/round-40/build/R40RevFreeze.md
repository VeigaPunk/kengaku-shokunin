# R40RevFreeze — freeze-order audit (round 40 wave 1, 2026-10-26)

Seat: reviewer, leaf. Audit of the round-40 freeze order against lane
`/home/vgpnk/Projects/shokunin/kengaku-shokunin`. Scratch (deleted after run):
`/fast/scratch/hyaku/kengaku-r40/R40RevFreeze` with shared clones `$S/lane` (tip `3077adb…`) and
`$S/freeze` (checked out at `bbb1095…`). Re-run receipts kept at
`.ufo/waves/round-40/build/R40RevFreeze/{c1-rerun.txt,c2-rerun.txt}`.

## 1. Commit window `d3a6277f..master`

Command: `git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin log --format='%H %cI %s' d3a6277f..master`

```
3077adbc7145726519f60f01426a5d03381ad444 2026-10-26T13:25:37-03:00 round-40: wave-1 spec and dispatch (37 seats, policy v1)
055748f78a3335434f2a4070bb3fb1cf8d0eba1f 2026-10-26T13:22:18-03:00 round-40: first recorded db-wal probe run (28 cases, mismatches=0, byte-equal rerun)
bbb109505670192035ef63d7c8b37733e99fa1a3 2026-10-26T13:21:59-03:00 round-40: freeze — claims, C1 tripwire-mutant counter (21 mutants, witnesses), C2 db-wal probe/spec/counter, captures, dry table, controls
```

Exactly three commits, in the claimed order: freeze → first recorded run → dispatch. Freeze
parent check: `git log -1 'bbb1095^'` → `d3a6277f188434458e1d2ce04aff59392c6f0dc6 round-36: …
abandoned…` — the freeze sits directly on the stated baseline (`plans/round-40-claims.md`: "Baseline
lane tip `d3a6277f…`"). No stray commit in the window.

## 2. Freeze commit carries the frozen set, and no receipt

`git cat-file -e bbb1095:<path>` over every frozen path (in `$S/freeze`), all `PRESENT`:

`plans/round-40-claims.md`, `plans/round40_c1_verify.py`, `plans/round40_c2_verify.py`,
`plans/db_wal_probe.py`, `plans/pkg-spec-r40.json`, `plans/pkg_gate.py`,
`corpus/evidence/round40/db-wal-dry-cases-freeze.txt`,
`corpus/evidence/round40/tb2-db-wal-recovery/SHA256SUMS`, `.ufo/waves/round-40/claims`.

Captures at `bbb1095:corpus/evidence/round40/tb2-db-wal-recovery/` (`git ls-tree --name-only`):
the claimed 8 files + `SHA256SUMS` (Dockerfile, instruction.md, main.db, main.db-wal.encrypted,
solve.sh, task.toml, test.sh, test_outputs.py). Controls at `bbb1095:.ufo/waves/round-40/claims/`
(`ls-tree -r`): `c2-stage-check.txt`, `census-before.txt`, `control-c1-hostile-daemon-module.py`,
`control-c1-hostile-daemon.txt`, `control-c1-nothing.txt`, `control-c1-tool-edited.txt`,
`control-c2-nothing.txt`, `frozen-digests.txt`, `witness-run.txt`, `witness/{w_anchor,w_ledger,w_order}.py`.

Receipt absence, command + output:

```
git cat-file -e bbb1095:corpus/evidence/round40/db-wal-probe.txt
  → fatal: path 'corpus/evidence/round40/db-wal-probe.txt' does not exist in 'bbb1095…'  (rc=128)
```

Required failure confirmed: the receipt did NOT exist at the freeze.

## 3. Receipt landed in 055748f, additively

```
git cat-file -e 055748f:corpus/evidence/round40/db-wal-probe.txt → rc=0
git diff --stat bbb1095..055748f
  .ufo/waves/round-40/first-run/first-run.txt |  5 +++++
  .ufo/waves/round-40/first-run/run2.txt      | 35 +++++++++++++++++++++++++++++
  corpus/evidence/round40/db-wal-probe.txt    | 35 +++++++++++++++++++++++++++++
  3 files changed, 75 insertions(+)   — zero deletions; no frozen path touched
```

Receipt-commit → tip `055748f..3077adb` touches only `build-dispatch.json`, `build-spec.json`,
`make_build_spec.py`; `bbb1095..3077adb` name-only is the union of the above five paths — no frozen
path modified after the freeze. Receipt bytes at 055748f and at tip are identical:
`git show <c>:corpus/evidence/round40/db-wal-probe.txt | sha256sum` →
`c74c6b91c8c49b1788f2dd7aa0d66edce0db0b52b549baf89ce69cfa8e2a730e` for both.

## 4. Digest verification at the freeze

Command (cwd `$S/freeze`, the clean clone at bbb1095):
`sha256sum -c .ufo/waves/round-40/claims/frozen-digests.txt` → all 11 lines `OK`
(claims, c1 counter, c2 counter, probe, spec, dry table, captures SHA256SUMS, anchor tool, ledger
tool, order tool, gate). Identical result re-run in the live lane root — the frozen files are
unedited in the working tree too. Capture-internal manifest also verified:
`(cd corpus/evidence/round40/tb2-db-wal-recovery && sha256sum -c SHA256SUMS)` → 8/8 `OK`.

## 5. Do-nothing controls re-run on a clean clone of bbb1095

Both counters run from cwd `$S/freeze` with `TMPDIR=$S`.

**C1** — `python3 plans/round40_c1_verify.py --lane . --work "$S/w"`: exit `1`;
`PINS total=3 mismatched=0`; 21 × `SURVIVED exhibits=none`; `BATTERY fixtures=0 wrong=0
tampered=0 sidechannel=0`; `MUTANTS total=21 killed=0 survived=21 invalid=0 null_detected=0`;
`PINS-AFTER mismatched=0`; `PREDICATE C1 fail`.
Diff vs committed `.ufo/waves/round-40/claims/control-c1-nothing.txt`: byte-identical after
appending the recorder-style trailer `exit=1` (the committed file's last line `exit=1` is a
recorder annotation, not counter output; my run printed `exit=1` separately and it matches).
Full output kept at `.ufo/waves/round-40/build/R40RevFreeze/c1-rerun.txt`.

**C2** — `python3 plans/round40_c2_verify.py --lane .`: exit `1`; `V1 ok listed=8 bad=0 extra=0`,
P2/P3/P4/P6/P7/P8/P10 DEFECT (`receipt unreadable`, entry/rows absent), `V2 DEFECT spec=frozen
gate=frozen gate_exit=1`, `V3 DEFECT rows=2 bad=['S119:row','S120:row']`, `V4 DEFECT receipt or
entry absent`, `V5 ok probe=frozen dry_byte_equal=True`, `V6 ok census_exit=0`, `V7 DEFECT receipt
or entry absent`, `checks=7 defects=4`, `PREDICATE C2 fail`.
Diff vs committed `control-c2-nothing.txt`: byte-identical modulo the same recorder `exit=1`
trailer; exit code reproduced. Full output: `build/R40RevFreeze/c2-rerun.txt`.

C1 ran in ~1 s because `plans/battery40` does not exist at bbb1095 (`git cat-file -e
bbb1095:plans/battery40` → rc=128, `fatal: path … does not exist`; also absent at tip) — the
committed `fixtures=0` control is faithful.

## 6. order_check (QUALITY Q30)

Command (cwd `$S/lane`, clean shared clone of tip 3077adb):

```
python3 plans/order_check.py --lane /fast/scratch/hyaku/kengaku-r40/R40RevFreeze/lane \
  --claims plans/round-40-claims.md --receipt corpus/evidence/round40/db-wal-probe.txt
ORDER claims=plans/round-40-claims.md round=40 freeze=bbb109505670192035ef63d7c8b37733e99fa1a3
ORDER receipt=corpus/evidence/round40/db-wal-probe.txt receipt_commit=055748f… claims_dir=.ufo/waves/round-40/claims/
ORDER scanned commits=1 file_entries=12 distinct_blobs=12
ORDER ok no claims file committed at or before the receipt shows the frozen probe executed
ORDER RESULT PASS    exit=0
```

Q30 property holds: nothing committed at or before the receipt commit demonstrates the probe
executed; the freeze precedes the first recorded run.

## 7. Extra cross-checks

- Mutant census in the frozen counter (`grep -cE '^\s*\("[ALO][0-9]{2}",'` on
  `bbb1095:plans/round40_c1_verify.py`): **21** tuples — anchor 11, ledger 7, order 3 — equal to
  the claims file ("Total **21** (anchor 11, ledger 7, order 3)") and to the control's 21 SURVIVED
  lines. `O13` appears only in the docstring as the withdrawn EQUIVALENT limit, never as a table
  row (`grep -n 'O13'` → single docstring hit at line 65).
- Frozen-file stability: `sha256sum -c` OK in both the bbb1095 clone and the live lane ⇒ no
  post-freeze edit of any pinned file.

## Findings

No defect found. Every acceptance check reproduces: freeze commit precedes the receipt and is
additively followed by it; the receipt first exists at 055748f and is unchanged through tip; all
11 frozen digests verify at the freeze and in the live lane; both do-nothing controls re-run
byte-identically (exit 1) on a clean clone of bbb1095; order_check passes (exit 0).

Observation (non-defect): the committed control files end with a `exit=1` line that the counters
do not print — a recorder-added trailer. A byte-diff therefore needs the trailer appended, as
done in §5; exit codes were independently observed to be 1.

Residual risk / verification gaps: this audit verifies freeze ORDER and integrity, not claim
truth — mutant equivalence (e.g. whether all 21 are genuinely unkilled by real fixtures) is wave-1
executor work; the C1 hostile-daemon and tool-edited controls were read as present but not re-run
(out of scope); the C2 re-run inherits host sqlite3 3.54.0 as recorded in the claims' limits.

VERDICT: freeze-audit-ok
