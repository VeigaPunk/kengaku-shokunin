# F39OrderGateMut — mutation probe of `plans/order_check.py` (round-39 wave 2, falsify)

Seat: `F39OrderGateMut` (mutation-tester, leaf). 2026-10-26.
Report: .ufo/waves/round-39/falsify/F39OrderGateMut.md

Target: `plans/order_check.py` at lane tip `a6832f53c1a94bb092a6cfd79fb4e449f2d4054c`, pristine
sha256 `948d5e1d2b3429d76a598fd11c4b22856d9f43ec093efd2c6aa0025aa0fc6ecc` — byte-identical to the
digest the wave-1 builder shipped (`.ufo/waves/round-39/build/R39OrderGate.md:28`). Attack: the
wave-1 real-repo calibration leg — "shown red on rounds 37 and 38, green on 39"
(`.ufo/waves/round-39/build/R39OrderGate.md:197`) — i.e. does that leg alone discriminate a
defective gate?

## 1. Method

Scratch fixture (operator directive 2026-10-25): `S=/fast/scratch/hyaku/kengaku-r39/F39OrderGateMut`,
`TMPDIR=$S`, `git clone -q --no-local` of the lane, `checkout -q a6832f5…`;
`git -C "$S/lane" rev-parse --show-toplevel` = `$S/lane`, `rev-parse HEAD` = tip, `status --porcelain`
empty. Pristine bytes saved to `$S/pristine_order_check.py`. Scratch removed before finishing; no lane
file written; no git-mutating command anywhere (clone/checkout only inside scratch; every restore was
a file copy, never git).

Detector (bounded, per assignment) — the three landed recheck commands, run from the clone root:

```
python3 plans/order_check.py --lane . --claims plans/round-39-claims.md --receipt corpus/evidence/round39/git-leak-probe.txt   # expect PASS / rc=0
python3 plans/order_check.py --lane . --claims plans/round-38-claims.md --receipt corpus/evidence/round38/build-pmars-probe.txt # expect FAIL / rc=1
python3 plans/order_check.py --lane . --claims plans/round-37-claims.md --receipt corpus/evidence/round37/git-webserver-probe.txt # expect FAIL / rc=1
```

Kill rule: a mutant is **KILLED** iff any of the three exit codes flips from the pristine verdicts
(red pair / green no longer discriminates); **SURVIVED** if all three are unchanged (coverage finding);
**INVALID** if the anchor string does not apply to landed bytes. Each mutant is one exact-string
replacement asserted `count==1` in landed bytes; mutated sha256 recorded; after each probe the file was
restored from the saved pristine copy and re-hashed.

## 2. Baseline (pristine bytes)

| run | rc | verdict |
|---|---|---|
| r39 | 0 | `ORDER RESULT PASS` |
| r38 | 1 | `ORDER FAIL probe-executed-before-receipt hits=1` — HIT `control-c2-skip.txt@e0a378539a45:11 kind=gate-p10` |
| r37 | 1 | `ORDER FAIL probe-executed-before-receipt hits=1` — HIT `control-c2-skip.txt@ca790460e9b7:12 kind=gate-p10` |

Matches the landed registry row's expected `PASS/0`, `FAIL/1`, `FAIL/1`. Receipt: `baseline.txt`.

## 3. Matrix (6 one-line mutants)

| id | site (plans/order_check.py) | mutation | flips | verdict |
|---|---|---|---|---|
| M1 drop-p10-exemption | :60 | `EXECUTED_EXCUSE` regex → never-match (author's `m1` string) | r39 0→1 | **KILLED** |
| M2 skip-freeze-contains-receipt | :183 | `if git.rc("cat-file", "-e", f"{freeze}:{receipt}") == 0:` → `if False:` (author's `m3`) | none | **SURVIVED** |
| M3 scan-only-freeze-commit | :193 | `scan_claims(git, claims_dir, receipt_commit)` → `…, freeze)` (landed-bytes shape of author's `m5`) | none | **SURVIVED** |
| M4 accept-any-p10 | :107 | `if not (m.group(1) == "DEFECT" and EXECUTED_EXCUSE.match(detail)):` → `if False:` | r38 1→0, r37 1→0 | **KILLED** |
| M5 read-work-tree | :132 | `cat-file blob sha` → `cat` of the work-tree path | none | **SURVIVED** |
| M6 swallow-git-errors | :73 | `if r.returncode != 0:` → `if False:` in `Git.run` | none | **SURVIVED** |

Per-mutant evidence (full stdout + rc + before/after hashes in each receipt):

* **M1** — r39 flips to `ORDER FAIL probe-executed-before-receipt hits=1`, HIT
  `control-c2-nothing.txt@088f7c36e94c:11 kind=gate-p10 \`gate: P10 DEFECT receipt unreadable\``.
  The excused line is what keeps round 39 green; r38/r37 also gain a second hit each (hits=2) but were
  already red. Killed by the green leg.
* **M2** — byte-for-byte the baseline verdicts. Neither red reaches clause 1 (both fail via clause 3
  only, `hits=1`), and round 39's freeze tree does not carry the receipt, so removing the
  freeze-contains-receipt leg is invisible to this pair.
* **M3** — byte-for-byte the baseline verdicts. The offending controls are committed *in* the freeze
  commits themselves (HIT lines `@e0a378539a45` / `@ca790460e9b7`), so capping the scan window at the
  freeze commit keeps both reds; round 39's freeze tree holds only the excused line, so green holds.
* **M4** — all three rounds print `ORDER RESULT PASS` (r38 and r37 1→0). The only hits in both red
  windows are `kind=gate-p10`; with the P10 arm disabled the CASE arm has nothing to catch. Killed by
  both red legs.
* **M5** — byte-for-byte the baseline verdicts. At the tip the work tree contains every windowed
  claims file (`ls-tree -r HEAD`: 13 / 6 / 7 entries for rounds 37/38/39), so reading work-tree bytes
  reproduces the committed verdicts exactly. The gate's contract — "The rule, over commits only
  (working tree and index are ignored)" (`plans/order_check.py:12`) — is violated with no signal from
  this pair.
* **M6** — byte-for-byte the baseline verdicts. In a healthy clone no `Git.run` call fails, so
  swallowing the `SetupError` raise changes nothing here. Direction is fail-open: a swallowed
  `rev-list`/`ls-tree`/`cat-file` failure yields empty data and a possible silent PASS. Whether any
  reachable lane state triggers a mid-scan git failure (corrupt object) was not tested — recorded as
  analysis, not output.

## 4. Findings (coverage, not contract changes)

1. **The real-repo leg alone would admit 4 of 6 defective gates** (M2, M3, M5, M6). It is load-bearing
   only together with the fixture harness: the author's `kill_map` shows fixture `f6` kills the M2
   shape and `f7` kills the M3 shape (`build/R39OrderGate/calibrate.py`, `kill_map`), while the M5
   (work-tree) and M6 (swallow) shapes are in no fixture set — the author's six mutants do not include
   them. Cited from the committed harness, not re-measured (out of my bounded detector).
2. **Both kills sit on the P10 arm.** M1 and M4 are the two directions of the same sensor, and the
   red pair's only teeth are P10 lines. The pair has no power over the clause structure (clauses 1–2)
   or the window's upper bound — exactly the parts a pre-registration gate exists for.
3. **M6 is the dangerous direction** (fail-open under mid-scan git failure) and is unsensed by both
   the real-repo pair and the author's fixtures (none of f1–f12 corrupts a git call mid-scan; f9/f10
   fail in `main`'s own checks, not `Git.run`).

## 5. Restoration evidence

* Pristine sha256 `948d5e1d2b34…fc6ecc`; every receipt header carries its mutated sha256 and
  `restored_sha256 … restore_ok: True` (M1 `ba878cf4…`, M2 `f3d1b361…`, M3 `3e851ad3…`, M4 `312b7cfb…`,
  M5 `22582cb9…`, M6 `0cb91cbe…`).
* Final restored triple-run (`restored.txt`): sha256 == pristine, r39 `PASS/0`, r38 `FAIL/1`,
  r37 `FAIL/1` — discrimination intact on restored bytes.
* Scratch `/fast/scratch/hyaku/kengaku-r39/F39OrderGateMut` removed at the end (verified absent);
  no process left running (all probes synchronous).

## 6. Receipts (this dir)

`baseline.txt`, `mut_M1-drop-p10-exemption.txt`, `mut_M2-skip-freeze-contains-receipt.txt`,
`mut_M3-scan-only-freeze-commit.txt`, `mut_M4-accept-any-p10.txt`, `mut_M5-read-work-tree.txt`,
`mut_M6-swallow-git-errors.txt`, `restored.txt`, `summary.json`.

## 7. Limits

* One implementation per named mutant; M3 uses the landed-bytes anchor (window capped at the freeze
  commit) because the author's draft anchor `hits = scan_claims(...)` does not exist in landed bytes
  (landed line :193 also binds `commits, files, blobs`); both narrowings behave identically on this pair.
* Detector bounded to the red/green pair per assignment; the 13-fixture harness was not rerun.
* Tooling: nothing installed (python3 + git sufficient); pacman untouched.

VERDICT: order-gate-mutants-2/6
