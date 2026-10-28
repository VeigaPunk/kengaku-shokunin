# R49C2MutVerdict — predicate output/exit mapping mutation probe

## Scope and axes

- **Axis:** coverage (R49-C2).
- **Item:** challenge the predicate output/exit mapping for false success and false failure against frozen negative controls.
- **Freeze check:** before measurement, `git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin cat-file -t 9d2900af41e4d1fc6022eff99010436fde6dbd93` returned `commit`; `git log -1 --format='%H %ci %s' <freeze>` returned `9d2900af41e4d1fc6022eff99010436fde6dbd93 2026-10-28 09:14:40 -0300 round-49: stage-1 freeze of C1 (fence over-refusal, v3 counter + mutant floor) and C2 (TB2 grader admission, Q40 counter, receipt ordering) claims`. HEAD of frozen scratch clone was that commit. Freeze therefore existed in committed tree before these measurements.
- **Measured revision:** `REV 9d2900af41e4d1fc6022eff99010436fde6dbd93` (C3 contract base, clean shared clone at start). R49's `plans/round49_c2_verify.py` and stage-2 controls were not present in this frozen tree; this is a proxy probe of imported `plans/round46_c3_verify.py`, not a claim that R49 counter was tested or admitted.

## Mutants and detector

The behavior-bearing aggregation is `plans/round46_c3_verify.py` `main()` lines 905–909: sum failed legs into `defects`, print `PREDICATE C3 pass|fail`, return 0 iff `defects == 0`. The bounded detector ran the counter on the committed r46 filler control, a scratch control with the package spec removed, and a scratch control with probe bytes replaced by a fast nonzero-exit stub. A positive oracle used an otherwise byte-identical counter copy with `which=("V6",)` to exercise the same mapping when a leg passes. The probe-truncated lane is thus positive specifically for V6, which does not read the probe; it remains negative for the full counter.

Detector semantics: pass requires the pass line and exit 0; fail requires the fail line and nonzero exit; a mismatch is SPLIT. Expected control outcome is fail; expected V6-only oracle outcome is pass.

- **M-A (false success):** replace `defects = sum(1 for _n, ok, _note in res if not ok)` with `defects = 0`.
  - SHA-256: pristine `a971c24dd5d0cb880e97ad4dd80315fcf58afaa02f8cffb5cc2e803aa292a8d4`; mutant `42aa92a897cba63e0b9d7f81d587b0fcf216eb21a02ca8fc523ab723264139f7`.
  - Filler output (verbatim): `checks=7 defects=0\nPREDICATE C3 pass`, exit 0 — **killed** by the false-success detector.
  - Probe-truncated full-counter output (verbatim): `checks=13 defects=0\nPREDICATE C3 pass`, exit 0 — **killed**.
  - Spec-removed input follows the earlier `PACKAGE unreadable` branch; it still printed `PREDICATE C3 fail`, exit 1, because this mutation does not touch that branch.
- **M-B (false failure):** replace the same aggregation with `defects = len(res)`.
  - SHA-256: `759b5d2ff6e13169d8d6b258b7d14da42a9cbd660e083d36046bfe6f70d88cff`.
  - All three negative controls still printed `PREDICATE C3 fail`, exit 1 — **survived the negative controls**.
  - V6-only positive oracle printed `checks=1 defects=1\nPREDICATE C3 fail`, exit 1 instead of its pristine `checks=1 defects=0\nPREDICATE C3 pass`, exit 0 — **killed by positive oracle**. Negative-only controls cannot detect false failure.

## Pristine and restored observations

Pristine full counter:
- Filler: exit 1; `checks=7 defects=6`; `PREDICATE C3 fail`.
- Spec removed: exit 1; `PACKAGE unreadable: [Errno 2] No such file or directory: '/fast/scratch/hyaku/kengaku-r49/R49C2MutVerdict/lane-specgone/plans/pkg-spec-r46.json'`; `checks=13 defects=12`; `PREDICATE C3 fail`.
- Probe truncated: exit 1; `checks=13 defects=4`; `PREDICATE C3 fail`.
- V6-only positive oracle: exit 0; `checks=1 defects=0`; `PREDICATE C3 pass`.

After restoration, the same full-counter inputs reproduced the same outputs and exit statuses. Restored counter SHA-256 equals pristine: `a971c24dd5d0cb880e97ad4dd80315fcf58afaa02f8cffb5cc2e803aa292a8d4`. The V6-only oracle copy hash was `ea793c9632f49a5ebd480b980492a4c7102a6c4f1d211c221eb3aaa93cd8560c` before and after; its source differs only in the selected leg tuple, not the mapping lines.

## Exact commands and evidence limits

Commands included:
- `git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin cat-file -t 9d2900af41e4d1fc6022eff99010436fde6dbd93`
- `git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin log -1 --format='%H %ci %s' 9d2900af41e4d1fc6022eff99010436fde6dbd93`
- Scratch clones at the frozen revision, `python3 <counter> --lane <scratch-lane> [--filler] --work <scratch-workdir>`, and the same command with `c3_oracle_v6only.py` for the positive oracle. The outputs and hashes above are the observed detector evidence.

No external source was opened; consequently no external URL/access-date/quote applies. The full real-package counter path was not run: r46 V2 uses the gate's `--rerun` and would execute the full probe, while this R49 stage-1 freeze explicitly restricts pre-receipt runs to `--dry`/`--stage-check`. This probe never claims R49 C2 admission. No tool was installed or upgraded.

**VERDICT: M-A killed by frozen negative controls; M-B survives negative controls but is killed by the positive V6 oracle. Coverage finding: negative controls alone do not test false-failure mapping. The R49-specific mapping remains unmeasured until its counter exists.**
