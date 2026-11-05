# MutTesterGate — mutation test of `plans/round93_freeze_integrity.py` through `plans/round93_c2_counter.py`

Seat: MutTesterGate (leaf, mutation-tester). Item: byte-level mutants of the freeze-integrity gate, each run through the
frozen C2 counter at the measured tip T, tabulated killed/survived with the killing leg.

## Setup and controls

- Measured tip T: `22972a317185216596b3dfe1c189e98d1eb86787`. Scratch clone `$S/lane` = `git clone --shared` of the lane, detached at T, status clean.
- Frozen bytes re-checked at T: gate `18b01b42fb54…` and counter `ac0e26a57b75…` match the frozen-instruments table (F = `d8d0a4b8`). The gate's last commit is `17cb9337` (P1), before F. Copies: `scripts/gate-at-T.py.txt`, `scripts/counter-at-T.py.txt`.
- **Null control, real tool at T** (`receipts/baseline-real-tool.txt`): W1 pass (4,1,3), W2 pass (5/5 fixtures), W3 pass, W4 pass (9,9,0), `TARGET legs_passed=4 of 4`, `PREDICATE R93-C2 pass`, rc 0. The counter is green at T with the real tool.
- **Null mutant** `m01-null` (byte-identical copy, run via `--tool-file`): same result, rc 0, battery 10/10. The `--tool-file` path does not perturb the verdict.
- Mutant generation: `mutants/generate.py` applies exact-substring substitutions to the gate at T. Every `old` string must occur exactly once or generation aborts. `mutants/manifest.json` records substitution counts and sha256 of each mutant. 26 files: 1 null + 25 mutants. Every non-null mutant differs from the source.
- Run: `python3 plans/round93_c2_counter.py --lane $S/lane --rev 22972a31… --work $S/w-<id> --tool-file mutants/<id>.py` (receipts `receipts/<id>.txt`, each ends with `rc=`).
- Battery per mutant: the same mutant run directly on the lane at T in claims mode (`receipts/battery-<id>.txt`) to see which in-path battery cases go RED. This is the attribution aid below.
- Tooling: none installed. Python 3 stdlib and git only. Nothing installed or updated.

## Kill matrix (`receipts/summary.tsv`)

Legs: W1 history, W2 five fixtures, W3 battery line, W4 self-table. "battery RED" = in-path SELFTEST cases RED when the mutant runs on the lane.

| mutant | description | W1 | W2 | W3 | W4 | predicate | rc | battery RED | result |
|---|---|---|---|---|---|---|---|---|---|
| m01-null | unchanged copy | pass | pass | pass | pass | pass | 0 | – | null passes |
| m02-drop-touched | touched-after-freeze check removed | pass | fail | fail | fail | fail | 1 | B02,B03 | killed (W2 edit-revert summary (1,1,0)≠(1,0,1); + battery) |
| m03-rev-compared-to-freeze | rev bytes compared to freeze bytes | pass | fail | fail | fail | fail | 1 | B02 | killed (battery-only: W2 rc on intact/unrelated) |
| m04-drop-touched-and-rev | touched check AND rev comparison removed | fail | fail | fail | fail | fail | 1 | B02,B03,B09 | killed (W1 summary (4,4,0); W2) |
| m05-absent-at-rev-intact | absent-at-rev treated as intact | pass | fail | fail | fail | fail | 1 | B05 | killed (battery-only) |
| m06-cne-exit0-pass | could-not-evaluate printed PREDICATE pass, rc 0 | pass | pass | pass | pass | pass | 0 | – | **survived, not equivalent** |
| m07-battery-skipped | in-path battery emptied | pass | pass | fail | pass | fail | 1 | 0/0 | killed (W3) |
| m08-battery-nonfatal | battery red no longer fatal (alone) | pass | pass | pass | pass | pass | 0 | – | **survived, latent: unreachable with a green battery** |
| m09-battery-b02-weakened | battery case B02 made always-true | pass | pass | pass | pass | pass | 0 | – | **survived, not equivalent in source; verdict-equivalent for all counter inputs** |
| m10-range-freeze-included | `f^..t` (freeze commit included) | pass | fail | fail | fail | fail | 1 | B02,B03 | killed (W2 edit-revert summary) |
| m11-range-reversed | `t..f` (touched always 0) | pass | fail | fail | fail | fail | 1 | B02,B03 | killed (W2 edit-revert summary) |
| m12-range-three-dot | `f...t` symmetric range | pass | pass | pass | pass | pass | 0 | – | survived, **equivalent** (f ancestor of t, enforced by m19-killed check) |
| m13-table-read-at-rev | frozen table parsed at --rev | pass | pass | pass | pass | pass | 0 | – | **survived, not equivalent** (demo A) |
| m14-table-row-prefix | last table row dropped | fail | fail | fail | fail | fail | 1 | 7 cases | killed (W1 summary (3,1,2)) |
| m15-freeze-bytes-unchecked | freeze-bytes vs table comparison removed | pass | fail | fail | fail | fail | 1 | B04 | killed (battery-only) |
| m16-touched-pathspec-dropped | touched counts every commit | fail | fail | fail | fail | fail | 1 | B01,B06,B09 | killed (W1 summary (4,0,4)) |
| m17-verdict-always-intact | verdict forced intact | fail | fail | fail | fail | fail | 1 | 5 cases | killed (W1 summary (4,4,0)) |
| m18-verdict-always-broken | verdict forced broken | fail | fail | fail | fail | fail | 1 | 7 cases | killed (W1 summary (4,0,4)) |
| m19-ancestry-check-removed | freeze-is-ancestor check disabled | pass | fail | fail | fail | fail | 1 | B07 | killed (battery-only) |
| m20-reason-text-only | absent-at-rev reason text renamed | pass | pass | pass | pass | pass | 0 | – | survived, **equivalent** (verdict still broken; text only) |
| m21-comment-only | trailing comment appended | pass | pass | pass | pass | pass | 0 | – | survived, **equivalent** |
| m22-ancestry-args-swapped | is-ancestor arguments swapped | fail | fail | fail | fail | fail | 2 | 6 cases | killed (CNE rc 2 on every leg) |
| m23-broken-filter-inverted | broken list counts intact rows | fail | fail | pass | fail | fail | 1 | – | killed (W1 summary (4,3,1); W2; W4 (9,0,9)); the only kill with a green battery |
| m24-empty-table-accepted | empty table accepted (no CNE) | pass | fail | fail | fail | fail | 1 | B08 | killed (battery-only; W1 is paths-mode and does not read a claims table) |
| m25-battery-b02-forced-red | B02 forced red, fatal (kill control) | pass | fail | fail | fail | fail | 1 | B02 | killed (battery-only) |
| m26-battery-b02-red-nonfatal | B02 forced red AND non-fatal | pass | pass | fail | pass | fail | 1 | B02 | killed (W3 only) |

Tally: 25 non-null mutants. **18 killed, 7 survived.** Of the 7 survivors, 3 are semantically equivalent (m12, m20, m21), 4 are not (m06, m08 latent, m09, m13).

Attribution: 10 of the 18 kills are summary-level (a leg's freeze-evidence summary or CNE changed: m02, m04, m10, m11, m14, m16, m17, m18, m22, m23). 8 are battery/rc-only (m03, m05, m07, m15, m19, m24, m25, m26): the only failing legs are a red battery case or a skipped battery, which W2/W3/W4 read through rc. The counter's W2 leg checks rc together with the summary, so a red battery reaches W2 as an rc mismatch on intact fixtures.

## Survivors, one line each

- **m06 cne-exit0-pass — not equivalent.** No leg drives the gate into could-not-evaluate: W1–W4 expect rc 1 or 0 with a summary. Demo B: real gate rc 2 `PREDICATE could-not-evaluate`, mutant rc 0 `PREDICATE pass` on an absent claims file. Doesn't flip the R93 verdict at T (no CNE occurs at T).
- **m08 battery-nonfatal (alone) — latent.** The battery is green at T in every counter input, so the non-fatal branch is never reached. Combined with a red battery it is killed (m26, W3 only).
- **m09 battery-b02-weakened — not equivalent in text, verdict-equivalent for counter inputs.** The counter reads the battery only as the printed `SELFTEST cases=10 ok=10` line (W3); a weakened case still prints ok=10. Verdict logic is untouched, so no verdict flips. Structural note under F4.
- **m12 three-dot — equivalent.** `f...t` = `f..t` when f is an ancestor of t (enforced by the ancestry check, m19 killed).
- **m13 table-read-at-rev — not equivalent.** Demo A: a claims table repaired after freeze (lying at freeze, correct at rev) → real gate `broken:freeze-bytes-differ-from-table+rev-bytes-differ` rc 1; m13 `intact` rc 0. No counter fixture rewrites the table after freeze (W2 lying-table fixture never edits the table). At T the claims blob is identical at F and T (`9d19321b…`, no commits in F..T touching it), so no verdict flips.
- **m20 reason-text-only — equivalent.** Verdict is `broken` either way; only the text string changes.
- **m21 comment-only — equivalent.**

## Findings

**F1 major (coverage) — could-not-evaluate exit contract is not judged.** No counter leg drives the gate into the rc-2 path, so a gate that converts CNE into PREDICATE pass (m06) survives all four legs. Demo: `receipts/fixture-demos.txt` § DEMO B. Verdict at T unaffected. Route to round 94: add a leg whose claims file is absent at freeze and require rc 2 with `could-not-evaluate`.

**F2 major (coverage) — no fixture for a post-freeze rewrite of the frozen table.** The counter's lying-table fixture never edits the table after freeze, so a gate that reads the table at --rev (m13) is accepted. Demo A (`receipts/fixture-demos.txt`): real gate rc 1 broken; m13 rc 0 intact. Verdict at T unaffected (claims blob identical F/T, verified). Route to round 94: a repaired-table-at-rev fixture requiring rc 1.

**F3 major (gate defect, latent) — default history simplification hides a side-branch edit discarded by a merge.** `git rev-list F..M -- c.py` returns 0 commits when a side branch edits c.py and a `-s ours` merge discards it, while `--full-history` returns both commits. The real gate's `touched` check then reports `intact` for an instrument that a commit in the window edited — a breach of its own rule (c) (demo C). **At T this is not verdict-flipping:** F..T is one commit with no merges (`receipts/w4-window-merge-check.txt`), and the W1 window `f0018773..1df76536` has 0 merges. The counter has no merge fixture, so this is not judged. Route to round 94: use `--full-history` (or a per-commit diff check) and add a merge fixture.

**F4 minor (coverage) — gate text is invisible to the table under `--tool-file`.** The W4 row for the gate itself (`plans/round93_freeze_integrity.py`) is evaluated on the lane's bytes at T, not on the tool under test (verified: `receipts/verify-w4-row-and-claims.txt`, mutants m02 and m09 both show `rev=18b01b42fb54 verdict=intact`). So a mutant gate's text is never compared to the table through this protocol. [INFERENCE, not exercised] A gate edit committed to the lane would change the lane's own row and be caught by W4; the mutant-text survivors (m08, m09, m20, m21) are invisible to the counter by construction. Route to round 94: name this limit in the claim.

**F5 minor (calibration) — W2 rc checks inherit battery reds.** 8 of 18 kills are battery/rc-only (see attribution). W2 treats rc as part of the fixture verdict, so an intact fixture fails whenever any in-path battery case is red, even when the gate's verdict on that fixture is right. The counter's W1 leg does not detect removal of the touched check (m02 passes W1), so touched-check kills come from W2's edit-revert summary and the battery.

**F6 info — null control and counter reproducibility.** Baseline at T and the null mutant both pass 4/4 (rc 0); the counter's result is identical on both runs (`baseline-real-tool.txt`, `m01-null.txt`).

**Correction to my own pre-check.** An earlier merge count (`rev-list --merges d8d0a4b8 T` → 2) was a mis-specified command (two positional revs, not a range); the correct range `d8d0a4b8..T` has 0 merges (`receipts/w4-window-merge-check.txt`).

**Verdict impact at T:** none of F1–F5 flips the frozen R93-C2 predicate; the real tool passes W1–W4 at T. The defects are a counter coverage gap (F1, F2, F4, F5) and a gate rule violation (F3), routed to round 94. No instrument was edited, and no tabled instrument changed.

## Receipts and scripts (in this seat dir)

- `receipts/baseline-real-tool.txt` — real gate at T, PREDICATE pass.
- `receipts/m<NN>-*.txt` — counter output per mutant, with rc.
- `receipts/battery-m<NN>-*.txt` — battery RED map per mutant (claims mode at T).
- `receipts/summary.tsv` — kill matrix (generated).
- `receipts/fixture-demos.txt` — demos A (m13), B (m06), C (merge hole), and window merge counts.
- `receipts/w4-window-merge-check.txt`, `receipts/verify-w4-row-and-claims.txt` — F..T merges, per-instrument default vs full-history touches, W4 row evidence, claims blob identity.
- `mutants/` — 26 mutant files, `generate.py`, `manifest.json` (sha256 each).
- `scripts/` — `tabulate.py`, `demo.sh`, and copies of the gate and counter at T.
- Scratch `$S` (`/fast/scratch/hyaku/kengaku-r93/MutTesterGate`) removed on exit after copying the above; nothing cited lives in /tmp.

No subagents were spawned. No commit, push, or mutating git in the lane.
