# R25 / EvidenceIndexScout — evidence-root index inventory (read-only)

Scope: `corpus/evidence/` top level vs the evidence tables in `corpus/README.md` and `PROVINCE.md`'s
"Own probe artifacts" rows (`:18` historical, `:109` current). Base: lane HEAD `3f371d2` (pre-reg on
`6180e4f`). Focus: loose root logs. No lane byte, git/jj state, or endpoint touched.

## Name-level parity — complete
- Disk 28 root `.log` + 14 dirs; README first-cell rows 28 unique log + 14 unique dir → **unindexed 0, dead-by-name 0**.
- All 28 logs committed, none untracked (`git ls-files corpus/evidence | grep -cE '^corpus/evidence/[^/]+\.log$'` → 28; `--others` empty).
- Dir rows name 62 concrete files; all resolve (5 regex artifacts: `.sha256`, `.sha256.repo`, `.py`, `.out`, external `SOURCES.md`).
- `PROVINCE:109` "plus 28 root receipt logs indexed" → true (`README:124-151`).

## Dead / misleading rows (semantic; name-level census cannot see these)
1. `README:143` `attrib-r21-ds-trials.log` "score appended after all trials" is dead: 0 GT blocks; `:128` "journal GT intentionally NOT read", `:174` score phase not run; only score is `attrib-r21-impl-ds-trials.log:268` (20/20 PASS, marker `:316`) → P1 trial-only.
2. `README:119-120` "each carries its freeze sha, seat, and blind rule in-file": `grep -ci blind corpus/evidence/probe-r19-*.log` → 0 on all 19; only the 9 attrib logs carry one (freeze-sha part holds 28/28).
3. `README:147` `attrib-r22-legs.log` names table `3d7861f8…` only; file carries freeze-2 (`:8`) and freeze-3 `77b8d4a0…` (`:134`,`:137`); authoritative `:312` is scored under `77b8d4a0…` (`:315`).
4. `README:149` `attrib-r22-opencode-trials.log` names instrument `34c4fa67…` = pre-repair header (`:5`); scored run is `05da8927…` (`:76`,`:208`); `:204` row-identical to `attrib-r22-legs.log:312` → one dedup sample (P2 fires).
5. `README:151` `attrib-r23-stream.log` names instrument `cce53a16…` = block 1 (`:3`); authoritative `:258` re-pins `489f938a…` (`:262`); `:194`≡`:258` yet stored verdicts disagree (`:256` PASS vs `:320` FAIL, target clause folded in later).
6. `README:150` `attrib-r23-stream-trials.log`: only prediction pointer `/tmp/kengaku-tmp/r23-stream/predictions.md` (`:4`), absent; `:7` DEVIATION (frozen plan/stream subcommand absent at run); its 30 stream trials 13:46:18–13:49:00 are a different execution from `stream.log`'s 13:46:41–13:49:24.
7. `README:157` `round24-sources` says "S001–S019 registry"; `gate.md` holds S001–S026 (26 rows) and `corpus/SOURCES.md` has 26 S-rows; `PROVINCE:112` still says "25 rows".
8. `README:145` `attrib-r21-impl-ds-trials.log` "seat copy" is wrong: `attrib-r21-ds-trials.log:136-137` gives impl 10:21:04–10:22:20 vs runner-A 10:23:45–10:25:01; impl-ds has 4 GT blocks (`:130,:176,:222,:268`, three debugging), marker only `:316`.
9. `PROVINCE:18` lists 10 dirs, omitting 4 that exist (round13-coverage, round18-kimi-routing, round24-census, round24-sources); `:109` checks 12/14; every listed path exists — no dead paths.

## C1 population map (P1 = 9 files, last-block rule)
| file | trials | GT blocks (line) | authoritative |
|---|---|---|---|
| attrib-r21-ds-trials | 20 | none | trial-only |
| attrib-r21-glm-trials | 22 | none | trial-only |
| attrib-r21-impl-ds-trials | 20 | 130,176,222,268 | `:268` 20/20 PASS |
| attrib-r21-impl-glm-trials | 22 | 142 | `:142` 22/22 PASS |
| attrib-r22-legs-hyper | 20 | none | trial-only |
| attrib-r22-legs | 40 / 2 runs | 260,312 | `:312` 20/20 PASS (hyper 10/10) |
| attrib-r22-opencode-trials | 20 | 204 | `:204` 20/20 ≡ r22-legs:312 |
| attrib-r23-stream-trials | 44 (14 survey+30) | none | trial-only |
| attrib-r23-stream | 30 | 194,258 | `:258` 30/30 acc; composite FAIL |

10 GT blocks, 7 distinct tables; authoritative set 5 → **4 distinct samples** (r22-legs:312≡opencode:204;
r23 :194≡:258; impl-ds :130≡:176). All 4 have n ≥ 17 (20, 22, 20, 30) → overall accuracy is
interval-testable; r22 TARGET hyper n=10 is below the power ask, so P1's INDETERMINATE is structural.

## Checked and NOT defects
- `README:85` "15 receipts" is the r19 window (lesson `:5`: 15 files, 07:43–08:04Z); the 4 r20 completions first-request 09:14:49–09:18:22. Glob now matches 19 — scoped history.
- 15/28 logs cite `/tmp` scratch; only the r23 predictions pointer is load-bearing and disclosed.
- `plans/probe-battery-r19.md:415` resolves to the FROZEN line `e1a86777…`; `README:126` holds.

## Calibration caveats for C1/C2
- Scored blocks are not seat-isolated: recorded `request-lines` 37–160 for 20–30 trials (`r22-legs:314`=37, `opencode:206`=68, `r23:260`=160, `impl-glm:144`=99); three r22 seats ran concurrently 11:50:06–11:52:27. GT is assigned by time window — record as a limit, don't re-adjudicate.
- P2e blindness: `plans/round24_census.sh:17` certifies root logs by basename substring and `:20` only mines dead rows from `knowledge|lessons|evidence` tokens; rows `README:124-151` carry bare filenames, so both pass 28/28 and 0 dead while findings 1–8 stand. `plans/state_check.py` is absent at base.

VERDICT: name-level index is complete (28/28 logs, 14/14 dirs, 0 unindexed, 0 dead-by-name), but
8 README rows and 2 PROVINCE counts misstate their bytes; P1 yields 4 distinct scored samples, all
n≥17, plus 4 trial-only files and 3 duplicate/rewritten blocks.

Installs: none (stdlib python3 + coreutils/git reads only).
