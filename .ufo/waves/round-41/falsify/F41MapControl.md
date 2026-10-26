# F41MapControl — red controls for C2's V7/V4/V3 on the landed TB2 `constraints-scheduling` entry

Round 41 wave 2 (falsify), 2026-10-26. Seat: mutation-tester, leaf. Detector under attack:
`plans/round41_c2_verify.py` (V1-V8) as landed at the round tip.

## Setup

- Frozen state: lane tip `3d0058fbde484c9d6c23fd997d9ee09a0663bcdb`. Note: the lane's `master` had already moved to
  `d7c77895752a2a5f317fa22f2362416ada50a04b` ("round-41: wave-2 (falsify) spec and dispatch"); the scratch clone was
  detached to the declared round tip before any run (`git -C "$S/lane" merge-base --is-ancestor 74513c06… 3d0058fb…`
  confirmed the wave-1 landing is an ancestor). `corpus/knowledge/tb2-constraints-scheduling-grader.md` and
  `corpus/SOURCES.md` are byte-identical at both commits, so the controls exercised the frozen bytes.
- Scratch: `S=/fast/scratch/hyaku/kengaku-r41/F41MapControl`; `TMPDIR=$S`; shared clone at `$S/lane`
  (`git rev-parse --show-toplevel` == `$S/lane` asserted before the one detached checkout); pristine snapshots at
  `$S/orig/`. No lane repo, index, or jj state touched; no commit/push anywhere; no git mutation in the lane itself.
- Host safety: every counter run (pristine and mutated) inside the mandated envelope
  `bwrap --dev-bind / / --ro-bind /home/vgpnk/.local/bin /home/vgpnk/.local/bin --tmpfs /run/user/1000 --proc /proc --unshare-pid --die-with-parent python3 …/round41_c2_verify.py --lane "$S/lane" --work "$S/work"`.
  No writes outside the report dir and scratch; nothing to timestamp.
- Restorations: `cp` from the pristine snapshot (never git checkout), verified by `cmp` + sha256 after every control.

## Pristine baseline

`plans/round41_c2_verify.py --lane $S/lane` → exit 0, `V1..V8 ok`, `checks=8 defects=0`, `PREDICATE C2 pass`;
gate `P10 ok probe_rerun=byte-equal bytes=5775`. Runs take ~12 s. Baseline green ⇒ all controls below are
conclusive kills/survivors. Receipts: `.ufo/waves/round-41/falsify/F41MapControl/receipt-*.txt` (9 files).

## Controls

Entry pristine sha256 `8612fb1c1c6a347c1ea0d222fa57b41b340cd451e2816d30044180cb6d8bffb0`;
`corpus/SOURCES.md` pristine sha256 `9e00981fbf97c2377365863189822a89eab0d8c42c183de4869a5ed170b434ee`.

| # | Mutation (smallest behavior-bearing point) | Target | Expected | Actual detector output (grep `^(V|checks=|PREDICATE)`) | Verdict | mutated → restored sha256 |
|---|---|---|---|---|---|---|
| M1 | Requirement map: `output-file` label `enforced`→`unenforced` | V7 | red | `V7 DEFECT rows=11 tags=11 bad=['output-file: labelled unenforced, receipt derives enforced']`; `checks=8 defects=1`; `PREDICATE C2 fail` (exit 1); all other checks ok | killed | `a042f95d…` → `8612fb1c…` |
| M2 | Requirement map: `window` row cites `nop` (violates `output-file`, not `window`) | V7 | red | `V7 DEFECT rows=11 tags=11 bad=['window: cites no case or a case that does not violate it']`; `PREDICATE C2 fail`; others ok | killed | `39d07a90…` → `8612fb1c…` |
| M3 | Requirement map: delete the whole `` `window` `` row | V7 | red | `V7 DEFECT rows=10 tags=11 bad=["tags missing=['window'] duplicated=0"]`; `PREDICATE C2 fail`; others ok | killed | `4248903b…` → `8612fb1c…` |
| M4 | Requirement map: `window` row line `` `instruction.md:1` ``→`` `instruction.md:2` `` | V7 | red | `V7 DEFECT rows=11 tags=11 bad=['window: line 2 is not the frozen instruction.md:1']`; `PREDICATE C2 fail`; others ok | killed | `e8ee8382…` → `8612fb1c…` |
| M5 | Mismatch naming: drop `` `seconds-30` `` (a `match=NO` id) from all 9 entry mentions | V4 | red | `V4 DEFECT cases=25 mismatches_named=1/2 bad=["mismatch cases not named in the entry: ['seconds-30']"]`; `PREDICATE C2 fail`; V7 stayed green (remaining cited cases all violate their tags) | killed | `8afcde83…` → `8612fb1c…` |
| M6 | `SOURCES.md` S122 anchor `sha256 1422b345…5d1`→`…5d2` (last hex char; S122 is a spec row) | V3 | red | `V3 DEFECT rows=2 bad=['S122:anchor_digest']`; `PREDICATE C2 fail`; others ok (census/gate-P6 do not verify the digest cell) | killed | `fb4d377c…` → `9e00981f…` |
| M7 (calibration) | `SOURCES.md` S124 anchor `sha256 8f3b04c3…10f`→`…10e` (S124 = prior-art row, NOT in `plans/pkg-spec-r41.json` `rows`) | any of V1-V8 | survivor (coverage) | exit 0, `V3 ok rows=2 bad=0`, all checks ok, `checks=8 defects=0`, `PREDICATE C2 pass` on the mutated registry | **survived** | `85354cb1…` → `9e00981f…` |

## Answers to the assigned questions

- **Do V7/V4 go red on requirement-map and mismatch-naming mutations?** Yes, each assigned map defect is killed by
  exactly one targeted check with a pinpoint note (M1-M4 → V7; M5 → V4). Attribution was clean because the gate's
  clean-tree clause only lists untracked files (`pkg_gate.py` P9: `git ls-files --others --exclude-standard`), so a
  mutated tracked file does not mask the targeted red, and every other V stayed green in each run.
- **Does V3 go red on a wrong anchor digest?** Yes — M6: one flipped hex char in the S122 row's `sha256` token ⇒
  `V3 DEFECT rows=2 bad=['S122:anchor_digest']`, predicate fail. V3 re-derives the token from
  `corpus/SOURCES.md` and compares it with `plans/pkg-spec-r41.json` `rows[S122/S123]["sha256"]`, so it is a real
  cross-file re-derivation, not self-consistent tautology.
- **Calibration gap (M7 survivor):** V3 iterates `spec["rows"]` only — S122 and S123. The S124 (TB2.1 PR #245
  prior-art) registry row also carries an anchor `sha256 8f3b04c3…` (for `corpus/evidence/round41/pr245-body.md`),
  and corrupting it passes the whole counter (`PREDICATE C2 pass`, exit 0). Nothing in V1-V8 re-derives that digest
  (census V6 validates row shape, not digest truth; gate P6 iterates the spec rows too). Coverage finding, not a
  contract violation: the frozen claim texts anchor S124's *body quote* only in prose, so the C2 surface could pin
  `pr245-body.md`'s digest the same way S122/S123 are pinned. Reported for the L1; nothing frozen changed.
- Known wave-1 limitation (filler package passes V1-V8) is about prose *meaning*; these controls show the counter
  does bite on the *structural* map/mismatch/anchor surfaces it claims.

## Restoration evidence

After the last control, both files `cmp`-identical to the pre-run snapshots (hashes above equal the pristine
values); `git -C "$S/lane" status --porcelain` empty; clone still detached at `3d0058fbde484c9d6c23fd997d9ee09a0663bcdb`;
a full pristine re-run after restoration: exit 0, `checks=8 defects=0`, `PREDICATE C2 pass`
(`receipt-pristine-after-restore.txt`). No lane file outside the scratch clone was ever modified.

## Cleanup

Scratch `S=/fast/scratch/hyaku/kengaku-r41/F41MapControl` removed after receipt copy, guarded by
`case "$T" in "$S"|"$S"/*) ;; *) refuse;; esac`. Report dir keeps the 9 receipts.

VERDICT: map-controls-red-6/7
