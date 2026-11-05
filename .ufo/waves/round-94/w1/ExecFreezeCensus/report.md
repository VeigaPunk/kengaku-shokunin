# ExecFreezeCensus — freeze-integrity census, v1 → v2 (round 94, report-only, no claim leg)

Seat ExecFreezeCensus, kengaku round 94, 2026-11-05. Lane `kengaku-shokunin`, measured tip T `90c7677f0ba95d0930d93bda6a14aa50605ebe2e`.
Lane HEAD at the time of the run: `d04e6664` (two commits past T: `242b3669`, `d04e6664`). The lane was only read (clone + read-only git). No tool installed or upgraded. Host sysctls untouched.

## Inputs (verified before every run)

- Gate v2: `plans/round94_freeze_integrity.py`, sha256 `8574b4d5dca7f3817f1beb42c024c80791a0b958b04da94361e9e2a6cc4964de`, equal to the round-94 frozen-instruments row.
- Gate v1: `plans/round93_freeze_integrity.py`, sha256 `18b01b42fb54ce658dbb98ff3afd12d06600960fae46700fec9218e73bcefcb6`, equal to the round-93 table row.
- Both gates were run from a scratch clone (`git clone --shared`, detached at T). The lane itself was never mutated. The scratch clone is removed after the receipts were copied here.
- Rows: the seven rows of `.ufo/waves/round-93/w1/ExecFreezeCensus/census.tsv` (rounds 85–91), re-run with the same freeze, tip and `--paths` list. Also round 93 and round 94 in claims mode (`--claims plans/round-93-claims.md` and `--claims plans/round-94-claims.md`). Extra: the round-92 W1 window used by the C2 counter (`f0018773` → `1df76536`, `--paths` of its four instruments). Both gates were run on every row.
- Each invocation prints its in-process battery. v1 printed `SELFTEST cases=10 ok=10`. v2 printed `SELFTEST cases=15 ok=15` in every run.

Command shape (v2 paths mode; v1 identical except the gate path):
```
python3 plans/round94_freeze_integrity.py --lane <clone> --freeze <F> --rev <T> --paths <instruments...> --work <scratch>/w-v2-<N>
```

## Census table

Full table: `census-v2.tsv` (columns as requested). Summary:

| round | mode | freeze | tip | instruments | intact | broken | rc | v1 | v2 | differs |
|---|---|---|---|---|---|---|---|---|---|---|
| 85 | paths | `99a7cb3b` | `88651a72` | 4 | 1 | 3 | 1 | fail | fail | no |
| 86 | paths | `61b0e074` | `276abd46` | 4 | 2 | 2 | 1 | fail | fail | no |
| 87 | paths | `21da383b` | `10de494d` | 5 | 5 | 0 | 0 | pass | pass | no |
| 88 | paths | `1f267d4b` | `7fcc680b` | 4 | 4 | 0 | 0 | pass | pass | no |
| 89 | paths | `0e6bb05f` | `00462b59` | 4 | 3 | 1 | 1 | fail | fail | no |
| 90 | paths | `664435cf` | `9cf98d90` | 5 | 5 | 0 | 0 | pass | pass | no |
| 91 | paths | `386184a6` | `cefabd44` | 6 | 5 | 1 | 1 | fail | fail | no |
| 93 | claims | `d8d0a4b8` | `7b8719f3` | 9 | 9 | 0 | 0 | pass | pass | no |
| 94 | claims | `844c504e` | `90c7677f` | 11 | 11 | 0 | 0 | pass | pass | no |
| 92 (extra, W1 leg) | paths | `f0018773` | `1df76536` | 4 | 1 | 3 | 1 | fail | fail | no |

The v1 column re-runs reproduce the round-93 census counts exactly (rows 85–91: broken 3, 2, 0, 0, 1, 0, 1). Rows 85, 86, 89 and 91 have the same broken instruments as the round-93 census receipts: `round85_c1_replay.py` (touched 5), `round85_c2_debt.py` (4), `round85_sqlite_truncate_probe.py` (1); `round86_c1_replay.py` (3), `round86_c2_repin.py` (2); `round89_claim_figures.py` (1); `round91_counter_pin.py` (1). Each is `rev-bytes-differ` plus `touched-after-freeze=N`.

## Does --full-history or the table rules change any historical verdict?

**No.** No verdict, count, or instrument-level reason differs between v1 and v2 in any row (`differs=no` in all nine rows of `census-v2.tsv`, and in the extra round-92 row).

Why --full-history changes nothing here: the difference between the default `rev-list` walk and `--full-history` appears only when a merge in the window lets a side-branch edit be discarded as TREESAME. Merges per window (`git rev-list --merges F..T | wc -l`):

| window | merges | commits F..T | first-parent walk = full walk |
|---|---|---|---|
| r85 `99a7cb3b`→`88651a72` | 0 | 16 | yes |
| r86 `61b0e074`→`276abd46` | 0 | 13 | yes |
| r87 `21da383b`→`10de494d` | 0 | 1 | yes |
| r88 `1f267d4b`→`7fcc680b` | 0 | 2 | yes |
| r89 `0e6bb05f`→`00462b59` | 0 | 5 | yes |
| r90 `664435cf`→`9cf98d90` | 0 | 2 | yes |
| r91 `386184a6`→`cefabd44` | 0 | 3 | yes |
| r92 W1 `f0018773`→`1df76536` | 0 | 13 | yes |
| r93 claims `d8d0a4b8`→`7b8719f3` | 0 | 4 | yes |
| r94 claims `844c504e`→`90c7677f` | 0 | 1 | yes |

With zero merges, a window `F..T` is one linear chain from T back to F. The default walk and `--full-history` therefore enumerate the same commits. The per-instrument touched counts are identical in every window (`windows.tsv`, columns `touched_v1_default` and `touched_v2_full_history`).

Why the new table rules change nothing here: the single-block, duplicate-row, malformed-row and unterminated-block refusals are not exercised by any census row. Paths mode has no table. The two claims tables (round 93: 9 rows; round 94: 11 rows) are one block each, with unique paths, so both gates accept them. The v2 rules are exercised only by the 15-case battery (B11 TREESAME-merge side edit, B12 second block, B13 duplicate row, B14, B15), and that battery is not a census verdict.

So the W-2 / W-3 / W-6 closures change no historical verdict in the census. They can change a verdict only on a history with a merge in the window, or on a table with a second block or duplicate row. Neither occurs in the rows measured here. The v2 gate passes its own battery (15/15); v1 passes its battery (10/10).

## Byte facts (context; not a verdict on any round)

- r85: 3 broken (`c1_replay` touched 5, `c2_debt` touched 4, `sqlite_truncate_probe` touched 1), all `rev-bytes-differ`.
- r86: 2 broken (`c1_replay` touched 3, `c2_repin` touched 2).
- r89: 1 broken (`claim_figures` touched 1).
- r91: 1 broken (`counter_pin` touched 1).
- r87, r88, r90: 0 broken.
- r92 W1 window: 3 broken (`c2_conformance` touched 4, `burndown` touched 3, `round91_counter_pin` touched 1); `round92_c1_replay.py` intact. This matches the counter's W1a expectation `(4, 1, 3)` and `intact == {round92_c1_replay}`.
- r93 claims: 9/9 intact across its 4-commit window.
- r94 claims: 11/11 intact at T. **The window `844c504e`→`90c7677f` is one commit** (the measurement commit itself). The round-94 freeze pins the bytes for exactly that window, so the freeze-to-tip coverage is one commit by construction.
- Post-T: the lane's history past T is two commits (`242b3669`, `d04e6664`). None of the 11 round-94 tabled paths is touched in `844c504e..d04e6664` (`git rev-list --full-history` count 0 for each). No merges in `90c7677f..d04e6664`.

## Findings

FINDING CEN94-1 info Census v2 reproduces the round-93 census (rounds 85–91) and the round-93 and round-94 claims rows: every rc, count, and broken-instrument set matches v1; `differs=no` for all nine rows of `census-v2.tsv`.
FINDING CEN94-2 info No historical verdict changes under v2. `--full-history` cannot change a verdict in any window with zero merges, and every window measured here has zero merges (linear F..T). The new table rules are not exercised by any census table.
FINDING CEN94-3 minor (bytes; carried from r93) Round 85 (broken 3), 86 (broken 2), 89 (broken 1), 91 (broken 1) remain byte-breached in their windows. Unchanged by v2; the round-93 census disclosures still apply.
FINDING CEN94-4 info Round 94's claims-mode window is one commit. Freeze-integrity at T therefore covers only the measurement commit `90c7677f`. This is a property of the window, not a gate defect.
FINDING CEN94-5 info Post-T lane history (`242b3669`, `d04e6664`) does not touch any tabled round-94 instrument.
FINDING CEN94-6 info Pathspec edge (not a verdict-flipping defect): `rev-list -- <path>` treats `*`, `?` and `[` as glob metacharacters, so a tabled path containing one could be undercounted. Checked: none of the 55 unique tabled paths across rounds 85–94 contains `*`, `?`, `[`, or a space (`grep -c '[*?[]'` and `grep -c ' '` both 0 over the set). No instance; noted for round 95.
FINDING CEN94-7 info Freeze choice remains operator-supplied (the round-93 census assumption 2 is retained). Neither v1 nor v2 can verify that a supplied freeze is the true freeze; the census takes each round's freeze as given.

No defect found that flips a verdict in this census.

## Receipts (`receipts/`)

- `v1-85.txt` … `v1-91.txt`, `v1-92.txt`, `v1-claims-93.txt`, `v1-claims-94.txt`: v1 gate output, full, with the command line and `EXIT`.
- `v2-85.txt` … `v2-91.txt`, `v2-92.txt`, `v2-claims-93.txt`, `v2-claims-94.txt`: v2 gate output, same shape. Each includes the 15-case battery (`BATTERY` lines and `SELFTEST`).
- `census-r93-input.tsv`: the round-93 census input used for the row list.

Files: `census-v2.tsv` (the table), `windows.tsv` (per-window commit and merge counts, per-instrument touched counts v1 default vs `--full-history`), `receipts/`, `report.md` (this file).

Commands quoted in receipts reference the scratch clone path (`/fast/scratch/hyaku/kengaku-r94/ExecFreezeCensus/lane`). That clone is at T, its bytes are the same as the lane's `plans/` at T, and the gate sha256 values above were checked on that clone. The scratch path is not citable as evidence; the receipts and the census table are.
