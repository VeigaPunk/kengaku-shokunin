# R38RevFreeze — freeze-order audit (kengaku round 38, hyaku run 8, wave 1)

Audited the frozen set at commit `e0a378539a45cc9388c66cfba22f44275131de23` and the receipt commit
`e95cf5500b6c13305cc41b8532ae07fb2c9dcd7b`. Method: a `git clone --shared` of the lane at
`/fast/scratch/hyaku/kengaku-r38/R38RevFreeze/lane`, detached at `e0a37853` (`git rev-parse HEAD` →
`e0a37853…`, `git status --porcelain` → 0 lines), `TMPDIR` pointed at the scratch. No lane file was
written except this report and `build/R38RevFreeze/` evidence. No tooling installed (bwrap and gcc
already present at `/usr/bin/`); nothing filed. Scratch deleted at the end; raw receipts preserved in
`build/R38RevFreeze/`.

## 1. Freeze order — OK

`git -C <lane> log --format='%H %cI %s' fc1174f5..HEAD`:

```
2c5f4e0ba8e2… 2026-10-26T02:42:21-03:00 round-38: wave-1 build spec and validated dispatch … against e95cf550
e95cf5500b6c… 2026-10-26T02:38:41-03:00 round-38: first recorded build-pmars probe run on a clean clone of e0a37853 …
e0a378539a45… 2026-10-26T02:38:28-03:00 round-38: freeze — claims C1 … and C2 …, counters, probe, captures, controls
21e6251bfebf… 2026-10-26T02:38:25-03:00 round-37: wave-2 reports and results (37/37) …
```

- Freeze (02:38:28) precedes the first recorded run (02:38:41, +13 s); dispatch (02:42:21) names
  `e95cf550` in its subject. Consistent with `plans/round-38-claims.md` ("written and frozen before …
  the first recorded run").
- Baseline check: `git show -s --format='%H %cI %s' fc1174f5` → `fc1174f52b15… 2026-10-26T02:25:17-03:00
  round-37 verifier spot-check (integrator, hyaku): non-author admit/reject` — matches the claims' first
  line ("the round-37 non-author spot-check").
- Mid-audit landings: `git log e95cf550..d93b7d6` shows `dc0cdb5` (02:53:40, battery38 + C2 package) and
  `d93b7d6` (02:56:10, frontier). `git diff --name-only e95cf550 d93b7d6 | grep -E
  '^(plans/(pkg_gate|round38_c[12]_verify|build_pmars_probe|pkg-spec-r38|round-38-claims)|corpus/evidence/round38/)'`
  → **NONE**. The frozen set is intact at the current tip `d93b7d6`.

## 2. `e0a37853` carries the whole frozen set — OK

`git show --stat e0a37853`: 18 files, +1588 — `plans/round-38-claims.md`, `plans/round38_c1_verify.py`,
`plans/round38_c2_verify.py`, `plans/build_pmars_probe.py`, `plans/pkg-spec-r38.json`,
`corpus/evidence/round38/build-pmars-dry-cases-freeze.txt`, `corpus/evidence/round38/tb2-build-pmars/`
(5 captures + `SHA256SUMS`), and controls `.ufo/waves/round-38/claims/{census-before,control-c1-gate-edited,
control-c1-nothing,control-c2-nothing,control-c2-skip,frozen-digests}.txt`. Claims, counters, probe, spec,
dry table, captures, controls: all present. `git ls-tree e0a37853 --name-only plans/battery38 | wc -l` →
`0` — no battery38 at freeze, matching "written … before any battery38 fixture exists".

## 3. Receipt landed later, alone — OK

`git diff --stat e0a37853 e95cf550` → exactly one file:
`corpus/evidence/round38/build-pmars-probe.txt | 26 +++++++++++++` — no frozen path touched. The receipt
is absent at the freeze (`git show e0a37853:<receipt>` fails) and unchanged since:
`sha256sum` of the working-tree file == `git show e95cf550:<receipt> | sha256sum` ==
`2408b477b0299e1339064b4b3df968a00174b3a5999016073b5fe4fd8cbb4ef9`.

## 4. `frozen-digests.txt` matches the freeze tree — OK (8/8)

Command: for each `dig path` line of `.ufo/waves/round-38/claims/frozen-digests.txt`,
`git show e0a37853:<path> | sha256sum` compared to `dig` → `frozen-digests vs e0a37853: ok=8 bad=0`:

| path | digest prefix |
|---|---|
| plans/pkg_gate.py | `ea638822…` |
| plans/round38_c1_verify.py | `80697399…` |
| plans/round38_c2_verify.py | `d906d55f…` |
| plans/build_pmars_probe.py | `32f0771c…` |
| plans/pkg-spec-r38.json | `bd9bfe71…` |
| corpus/evidence/round38/build-pmars-dry-cases-freeze.txt | `93b4b60c…` |
| plans/round37_c1_verify.py | `dbc9f719…` |
| plans/round37_c2_verify.py | `b8cba11a…` |

Beyond the ledger, every counter pin matches the freeze blobs: all 14 `PINS` of `round38_c1_verify.py`
(gate, r37/r36 counters, r35 spec, attribution audit, nine battery37 modules) plus the C2 pins (5
captures, spec, gate, probe, dry) → `counter pins vs e0a37853: ok=21 bad=0 (of 21)` distinct paths.
Working tree today: every frozen path digest == freeze digest (checked individually; the 5 captures and
`SHA256SUMS` additionally `sha256sum -c SHA256SUMS` inside the freeze clone → 5× `OK`).

## 5. Controls are reproducible — OK (C1 byte-exact; C2 exact at check level)

### 5.1 control-c1-nothing — byte-identical modulo `time`

`cd <clone> && python3 plans/round38_c1_verify.py --lane .` (TMPDIR=scratch), wrapped in bash `time`.
`diff` recorded control vs rerun after stripping the `real/user/sys` lines → **empty**
(`build/R38RevFreeze/diff-c1-clean.txt`, 0 bytes). Identical on both: `PINS total=14 mismatched=0`;
`BATTERY fixtures=64 wrong=0 renamed_disagree=0 sidechannel=0`; all 22 `MUTANT … SURVIVED` lines;
`MUTANTS total=22 killed=0 survived=22 invalid=0 null_detected=0`; `PREDICATE C1 fail`; `exit=1`.
Wall ≈47 s in both the recording and my rerun. The claims' "at freeze the round-36+37 battery kills
0/22 under the ATTRIBUTED kill rule" is reproduced exactly.

### 5.2 control-c2-nothing — one explained line

Same command on the clean clone. `diff` (`build/R38RevFreeze/diff-c2-clean.txt`) shows exactly two
changed regions, both inside V2's gate block:

```
<     gate: P9 DEFECT untracked=11 first=corpus/evidence/round38/build-pmars-dry-cases-freeze.txt
>     gate: P9 ok untracked=0 first=0
<     gate: defects=8
>     gate: defects=7
```

Everything else is byte-equal: V1 ok, V2 DEFECT, V3 DEFECT `bad=['S115:row', 'S116:row']`, V4 DEFECT
(receipt absent), V5 ok, V6 ok, V7 DEFECT, `checks=7 defects=4`, `PREDICATE C2 fail`, `exit=1` — the
claims' "→ `checks=7 defects=4` (V2, V3, V4, V7), exit 1" reproduces exactly.

Cause, verified by reconstruction: the recorded control ran on the freeze **working tree**, where the
12 not-yet-committed round-38 files were untracked; a clean clone tracks everything. Rebuilt that tree
(clone at parent `21e6251b`, then `git archive e0a37853` of the 12 freeze-added paths extracted as
untracked) and reran → `gate: P9 DEFECT untracked=12 first=corpus/evidence/round38/
build-pmars-dry-cases-freeze.txt` (`diff-c2-recon.txt`): same DEFECT line, count 12 vs the recorded 11
(see §8.1). C1 on the reconstructed tree: identical to the recorded control too
(`diff-c1-recon.txt`, 0 bytes) — C1 is lane-cleanliness-insensitive, as its output suggests.

### 5.3 The other two controls corroborate the freeze design

- `control-c1-gate-edited.txt` line 1: `PINS total=14 mismatched=1 first=plans/pkg_gate.py`, and its
  tail `MUTANTS total=22 killed=0 survived=0 invalid=22` — editing the gate goes red on pins and
  invalidates every mutant. Freeze protection demonstrated, not merely asserted.
- `control-c2-skip.txt`: gate `P10 DEFECT fresh probe output is not byte-equal to the receipt` (11 words)
  and `V7 ok rows=7 tags=7` — both disclosure sentences about it check out ("keeps only `P10 DEFECT …`";
  "V7 alone is satisfiable by a hand-typed receipt … V2's P10 fresh-run byte compare is what makes such
  a receipt red").
- `census-before.txt` ends `kengaku ok … exit=0`, matching the nothing-control's `V6 ok census_exit=0`.

## 6. Live probe reproduces the receipt (beyond the named checks)

`cd <clone> && python3 plans/build_pmars_probe.py --lane .` → **byte-equal** to
`corpus/evidence/round38/build-pmars-probe.txt`; both sha256 `2408b477b029…`;
`cases=22 observed_pass=7 observed_fail=15 mismatches=0`; exit 0; `real 0m0.971s`
(`build/R38RevFreeze/probe-rerun.body`, `probe-rerun.time`). A third recorded run consistent with the
receipt commit's "second run byte-equal". Cross-checks of receipt content: header capture digests ==
the counter's `CAPTURES` values for `instruction.md`/`test_outputs.py`; every CASE line `match=yes`
(22/22); summary agrees with the lines; the 7 observed passes are exactly the claims' headline
observations — `canned-shape`, `canned-x11-dlopen`, `results-trailing-text`, `canned-exit-nonzero`,
`path-split`, `debian-is-file`, `c-is-dir`. The dry table carries the 7 `TAG` lines and
`cases=22 predicted_pass=7 predicted_fail=15` as claimed.

## 7. Disclosure accuracy — every checked sentence holds

1. Baseline tip is the round-37 non-author spot-check: §1 ✓.
2. Freeze precedes first recorded run; battery38 absent at freeze; only `--dry`/`--smoke` plus the
   disclosed discarded control-time run before it: consistent with §2/§3 (the unrecordable part is
   inherently unverifiable; the disclosure itself declares it, `plans/round-38-claims.md` ¶2).
3. "The probe was already at its frozen digest" at control time: `32f0771c…` in `frozen-digests.txt` ==
   probe blob at `e0a37853` ✓ (§4).
4. Controls "committed with this file under `.ufo/waves/round-38/claims/`": 6 files there in `e0a37853` ✓.
5. Digest shorthand in the claims (`ea638822…`, `32f0771c…`, `93b4b60c…`) == full digests ✓.
6. Captures "(5 files + `SHA256SUMS`)" ✓; manifest verifies ✓ (§4).
7. "the gate digest is shared and frozen for both": both counters pin `ea638822…` ✓.
8. 22 mutants, each one byte-level `old -> new` of the pinned gate: `MUTANTS` table read in full,
   `TOTAL = 22`, every entry a single replacement pair ✓.
9. Nothing frozen changed after the freeze: `e95cf550` adds the receipt only (§3); later wave commits
   touch no frozen path (§1) ✓.

## 8. Residual risks and verification gaps

1. **`untracked=11` vs reconstructed `12`** (`control-c2-nothing.txt` line 10 vs my reconstruction):
   the recorded count is one below a fully-untracked pre-freeze tree. Most consistent hypothesis: one
   freeze-added file was already staged (index) at recording time — e.g. claims git-added while drafting
   the freeze commit — which the committed bytes cannot settle. The DEFECT line, all seven V-outcomes,
   and `checks=7 defects=4` are unaffected; classified benign, not a defect.
2. **13 s freeze→receipt window**: measured clone ≈1.1 s + probe run ≈1.0 s makes it unremarkable. Still,
   that the receipt's runs were the *first* runs is not provable from git alone; the disclosure's own
   discarded-run confession is the honest handling of exactly that gap.
3. **Upstream byte-equality** ("upstream `main` byte-equal at freeze" for S115/S116, and TB2 pin
   `2fd12b88…`): not re-verified — offline audit, no fetch attempted.
4. **Mutant-list rightness** (are N01–N22 the correct/complete advertised behaviours?) is the
   calibration seats' question; this audit covers freeze integrity only (frozen, single-replacement,
   0/22 baseline kill reproduced).
5. The recorded C2 nothing-control is by construction not byte-reproducible on a clean clone (it embeds
   freeze-tree dirt in one P9 line); any later harness diffing controls against clean-clone reruns must
   expect that line, or it will look like a defect that is not.

Evidence receipts: `build/R38RevFreeze/{c1-clean-clone,c1-recon,c2-clean-clone,c2-recon}.out`,
`probe-rerun.{body,time}`, `diff-c1-clean.txt`, `diff-c1-recon.txt`, `diff-c2-clean.txt`,
`diff-c2-recon.txt`.

VERDICT: freeze-audit-ok
