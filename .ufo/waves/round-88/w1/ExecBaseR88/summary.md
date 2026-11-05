# ExecBaseR88 — independent re-run summary (round 88, wave 1)

Read-only on the lane; scratch under `/fast/scratch/hyaku/kengaku-r88/ExecBaseR88/` (deleted before yield).
Full transcript: `replay.txt` in this directory (`$ command` / output / `rc=<n>` blocks).

## Check 1 — R88-C1 counter at BASE `801b903af6412cb424209a60b3a52e56c3532866`

- Output: `TARGET executed_rows=31 member=fix-git located=0 executed=0 cases=0 legs=0 mismatches=0 defects=3`, `PREDICATE R88-C1 fail`, rc=1.
- Defect lines: L4-table (case table absent), L1-receipt (receipt absent), L7-ledger (unexecuted row).
- **Verdict: match** — identical to the frozen do-nothing control in `plans/round-88-claims.md` and L1 `base-runs.txt`.

## Check 2 — R88-C1 counter at tip `7fcc680b86599eedd63e862a061848298428b3cc`

- Output: `TARGET executed_rows=32 member=fix-git located=1 executed=1 cases=8 legs=16 mismatches=0 defects=0`, `PREDICATE R88-C1 pass`, rc=0.
- The counter's own L6 leg extracted the measured tree and re-ran the probe inside the measurement.
- **Verdict: match** — identical to frozen after-figure and L1 `tip-runs.txt`.

## Check 3 — R88-C2 instrument at BASE

- `git cat-file -e 801b903a…:plans/round88_claim_figures.py` → `fatal: path 'plans/round88_claim_figures.py' exists on disk, but not in '801b903a…'`, rc=128.
- **Verdict: match** — instrument absent at BASE, predicate unreachable, as frozen.

## Check 4 — R88-C2 counter at tip

- Output: `MISMATCH KNOWN R87-C1 kv:defects claimed==7 defects claimed =7 measured 3`, `RECORDS claims=17 files=8 records=56 checked=56 matched=55 mismatches=1 prose=0`, `DEFECTS n=0`, `TARGET … defects=0`, `PREDICATE R88-C2 pass`, rc=0.
- Exactly one mismatch, classified KNOWN against the frozen set `{(R87-C1, kv:defects): 7→3}`.
- **Verdict: match**.

## Check 5 — R88-C2 `--selftest`

- Four `SELFTEST … pass` lines (T1 doctored-extract, T1 doctored-mismatch verdict=mismatch, T2 marker-negatives, T3 atbase-backward, T4 dedupe — five lines total across four test ids), `DEFECTS n=0`, `PREDICATE R88-C2-SELFTEST pass`, rc=0.
- **Verdict: match**.

## Check 6 — independent probe re-run from `git archive` of the tip tree

- Extracted `7fcc680b` to scratch, ran `tree/plans/round88_fixgit_probe.py --lane tree --work probe` → rc=0, all 8 CASE lines `observed == predicted`, `cases=8 legs=16 mismatches=0`, `PREDICATE R88-PROBE pass`.
- `diff` of the OBSERVATIONS block vs `corpus/evidence/round88/fix-git-probe.txt` → identical, rc=0.
- Note: stamp fields `LANE_TIP`/`WORKTREE` read `absent` because the extracted archive is not a git repo — expected for a lane-less tree; the observation block (the compared surface) is unaffected.
- **Verdict: match**.

## Check 7 — receipt pin verification

- `git show 7fcc680b:plans/round88_fixgit_probe.py | sha256sum` → `50ae36d6…66f8` = receipt TOOL_SHA. **match**
- `git show 0220c2f9:plans/round88-cases.json | sha256sum` → `72f8ea0c…3067` = receipt CASE_TABLE_SHA. **match**
- `git show 7fcc680b:corpus/evidence/round52/graders/fix-git/tests/test_outputs.py | sha256sum` → `a8a6f51e…43f3` = SUBJECT_SHA. **match**
- `git merge-base --is-ancestor da16ec39… 7fcc680b…` (receipt LANE_TIP vs measured tip) → rc=0. **match**
- `git merge-base --is-ancestor 7fcc680b… 7fcc680b…` → rc=0 (self-ancestor sanity).
- Note: receipt `LANE_TIP` is `da16ec39` (frontier commit at mint time), not the measured tip `7fcc680b`; both are ancestors of `7fcc680b`, consistent with the honest-limit note in the claims file.

## Check 8 — frozen bytes unchanged

- `git diff --stat 0220c2f9 7fcc680b -- plans/round-88-claims.md plans/round88-cases.json` → empty, rc=0. **match**
- `git diff --stat 1f267d4b 7fcc680b -- plans/round88_fixgit_probe.py plans/round88_c1_replay.py plans/round88_claim_figures.py` → empty, rc=0. Instrument bytes identical between instruments freeze and measured tip. **match**

## Findings

None. All eight checks reproduce the frozen claims exactly. The only anomaly in `replay.txt` is a first-pass quoting defect in my own capture harness (`"|"` passed as a literal git argument, rc=128); the corrected commands are recorded in the same file and all pins verify.

Tooling: none installed; no network use; no pacman transactions.
