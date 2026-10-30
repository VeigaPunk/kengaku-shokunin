# RV1EntryModeOk — seat report (round 55, wave 1, read-only revenger)

Target: reconstruct why the round-54 counter computed `entry_mode_ok` without binding it to the registry.
Result and evidence: `findings.md` (identical copy at `../RV1EntryModeOk.md`).

## Answer

Predicate-scope decision, inherited from the round-53 frozen argv contract (`plans/round-53-claims.md:198`) and
re-frozen in round 54 (LEDGER leg at `plans/round-54-claims.md:143–144`: "script matches the registry row's script").
Not a documented open window (no deferral text found). Not a wiring oversight: `entry_mode_ok` is consumed at
`plans/round54_c2_entrytruth.py` lines 229–231, 277–278, 358–359 (birth revision `17f90355`). What was missing is the
binding to the registry cell's full command and to the program the interpreter actually runs.

The round-55 claim's phrase "computed but unwired" is inaccurate and should be corrected by dated amendment.

## Commands run and exit codes

| command | exit |
|---|---|
| `git -C <lane> log --oneline / --format / --diff-filter=A -- plans/round54_c2_entrytruth.py` | 0 |
| `git -C <lane> show 17f90355:plans/round54_c2_entrytruth.py` (read, numbered) | 0 |
| `git -C <lane> show 6c919180:plans/round53_c2_tipstate.py` (read, numbered) | 0 |
| `git -C <lane> show 798f5e9e:SKILL.md`, `show 6e0a1915|9a0746be:plans/round54-entrytruth.json` (to scratch) | 0 |
| `git -C <lane> show 17f90355:plans/round54_c2_entrytruth.py > <scratch>/mod/r54_birth.py` (sha256 `44c3f412…`) | 0 |
| `python3 receipts/probe_wiring.py <scratch>/mod/r54_birth.py <scratch>` → `receipts/probe-wiring-r54-birth.txt` | 0 |
| python import of r53 `argv_ok` / `kind_ok` on abbreviated argv (scratch, inline; output in findings E5) | 0 |
| `python3 receipts/measure_l1.py SKILL.base.md ledger-r54-9a0746be.json` → `receipts/measure-l1-projection.txt` | 0 |
| grep / read of round-54/53/55 claims, lessons, SCORECARD, QUALITY Q44, build spec, w1 receipts | 0 |
| `git -C <lane> rev-parse 798f5e9e^{commit}` | 0 |

No `git` mutation (no add/commit/checkout/reset/stash). Lane clone not created; all probes ran on scratch copies
or imported modules from `git show` output.

## Files written

- `.ufo/waves/round-55/w1/RV1EntryModeOk/findings.md`
- `.ufo/waves/round-55/w1/RV1EntryModeOk.md` (copy, per the Report trailer)
- `.ufo/waves/round-55/w1/RV1EntryModeOk/report.md` (this file)
- `.ufo/waves/round-55/w1/RV1EntryModeOk/receipts/{probe_wiring.py, probe-wiring-r54-birth.txt, measure_l1.py, measure-l1-projection.txt}`

Scratch: `/fast/scratch/hyaku/kengaku-r55/RV1EntryModeOk/` (deleted before yield).

## Defects and risks found (routed to L1, not fixed here)

1. **Round-55 L1 and L2 conflict on `tb2-grader-probe`.** Its registry cell is a `uv run … python3 …` command; L2 makes
   `argv[0] == uv` a WRAPPER-DEFECT; L1 requires token-equality with the cell. As frozen, this row cannot pass both.
   Dated amendment needed before the after-run.
2. **Round-55 L1 "token-equal" is undefined for 16 of 78 rows** (placeholders, `DIR`/`REV`, bracketed optional flags).
   Measured projection: 62/78 first-cell-command token-equal to the r54 ledger argv. Normalisation rule needed by amendment.
3. **Round-55 claim text says "entry_mode_ok computed but unwired"** — inaccurate (see findings E3). Correct by amendment.
4. **Round-54 abbreviation and combined-`-c` laundering** is reproduced in the r54 review; the same exact-token scope exists
   in the r53 counter (`argv_ok`/`kind_ok`), so the hole is inherited, not introduced in r54.

## Dead ends

- `xd://lsp` unavailable: reference reconstruction by file read and `git show`/grep only; no semantic reference proof claimed.
- Did not run the full r54 counter on a clean clone (not requested for this seat; intent question did not need it).
- `plans/round55_c2_entryargv.py` is not present at base; not examined.

## Installs

None. No tool installed, upgraded or updated. No pacman. No `~/.local/bin` writes.

## Verification status

Claims in findings are backed by source reads (commit-pinned `git show`), the dry wiring probe (exit 0), the r53 import
probe, and the L1 projection script (exit 0). The L1 numbers are pre-run projections on the r54 ledger, not scored results
of the round-55 instrument. Nothing was verified against the round-55 after-run; that is the L1's integration duty.
