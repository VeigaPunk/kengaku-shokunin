# C7IndexParity — corpus README index parity, both directions, at landing time

Seat: C7IndexParity · kengaku round 55, wave 1 · measured 2026-10-30T15:41Z
Lane: `/home/vgpnk/Projects/shokunin/kengaku-shokunin` working tree (tip `80afa613` + in-flight round-55 landing)
Instrument: `.ufo/waves/round-55/w1/C7IndexParity/parity_check.py` (read-only; full JSON: `landing.json`, baseline `t0b.json`)
Wait: bounded-wait for `corpus/knowledge/tb2-chess-best-move-grader.md`, 60 s steps × 25 max — **found at step 1, 15:41:28Z** (log: `wait.log`)

## The four parity numbers (README table-row index vs disk)

| # | Index | Files/dirs on disk | README table rows | files → rows (orphans) | rows → files (stale/dangling) | Duplicate rows |
|---|---|---|---|---|---|---|
| 1 | `corpus/knowledge/*.md` | **59** | **59** | 0 | 0 | 0 |
| 2 | `corpus/lessons/*.md` | **83** | **71** | 12 | 0 | 0 |
| 3 | `corpus/evidence/` dirs | **46** | **23** | 23 (see F3) | 0 | 0 |

Any-mention variant (table rows + bullets/headings/prose `` `code` `` tokens, house-style sections included):

| Index | Files/dirs | Mentioned | gap |
|---|---|---|---|
| knowledge | 59 | 59 | none |
| lessons | 83 | 72 | 11 files with no README mention of any form |
| evidence dirs | 46 | 39 | 7 dirs with no top-level mention (F3) |

Secondary (not a seat-spec count, checked for completeness): evidence root receipt logs — **28 files vs 28 table rows, exact parity, zero diff** (`rootfiles.txt` vs `rootrows.txt`).

## R55-C3 landing confirmations (E9-owned surfaces — observed state)

- **New knowledge entry:** `knowledge/tb2-chess-best-move-grader.md` EXISTS (13,170 bytes, S201/S202/S109 source pins, verified-at, 180 d recheck block) and its README row EXISTS — "What's here" line **84**; Frontier partial-discharge note at line 445. Row↔file both directions close.
- **Round-55 evidence:** `corpus/evidence/round55/` EXISTS containing `chess-best-move-probe.txt`; README section "### Round-55 evidence (2026-10-30)" (line 696) with top-level bullet `` `corpus/evidence/round55/` `` (line 698). Dir→index direction closes.
- **Round-55 lesson:** `corpus/lessons/round-55.md` EXISTS (4,573 bytes) but has **no index row** — see finding F2.

## Old-row staleness sample (spec item 4): 5 rows per index, spread-sampled

- knowledge rows (lines 29, 43, 58, 73, 554): benchmark-selection, bench-arena-round7-scaffold-ablation, benchmark-saturation-and-lifecycle, tb2-db-wal-recovery-grader, served-endpoint-identity-pin — **all exist**.
- lessons rows (lines 85, 103, 134, 151, 541): round-54, round-9-aggregator-corpus-verdict, round-30-verifier-spotcheck, round-39, round-52 — **all exist**.
- evidence rows (lines 176, 182, 187, 461, 578): round8-horizon, round12-ladder, round18-kimi-routing, round26-sources, round34 — **all exist**.
- Exhaustive backstop: `rows_without_files` = 0 in all three indices — **no stale row of any age** in the table-row index.

## Findings

- **F1 — knowledge index parity closed at landing (the R55-C3 no-harm check PASSES).** At t0 (15:39Z) the count was 58 files / 59 rows, the single `rows_wo_files` entry being exactly the pending `tb2-chess-best-move-grader.md` row. Two minutes later the entry landed and the count closed to 59/59 with zero orphans, zero dangling rows, zero duplicates, both directions.
- **F2 — `lessons/round-55.md` has no README index row (E9 owns the index; not fixed by this seat).** The gap is **carried debt, not round-55 harm**: HEAD's README (commit `80afa613`, pre-round-55 data) already has 71 lessons rows against the same 83 files on disk, and the working tree did not change that count (71 → 71). The 12 unindexed lesson files: round-44-verifier-spotcheck, round-46-verifier-spotcheck, round-47-verifier-spotcheck, round-48-verifier-spotcheck, round-49, round-50, round-50-verifier-spotcheck, round-51-verifier-spotcheck, round-52-verifier-spotcheck, round-53-verifier-spotcheck, round-54-verifier-spotcheck, round-55. (Round-50 has a prose bullet in its evidence section, so any-mention gap is 11.)
- **F3 — evidence index is structurally two-tier, pre-existing.** Only 23 of 46 evidence dirs carry formal `| Dir | Contents |` table rows (rounds 8–34 pattern); rounds 44+ switched to prose bullets naming subpaths/files, never the top-level dir token. Dirs with no top-level mention of any form: round44, round46, round50, round51, round52, round53, round54 — each *is* content-indexed via its round-N evidence section. `evidence/round55` **is** top-level-mentioned (line 698), so R55-C3's own evidence surface is indexed at least as well as rounds 44–54. Zero `mentions_without_dirs` — no dangling evidence rows in either direction.
- **F4 — no new harm detected anywhere in scope.** Knowledge 59/59 both directions; no stale old rows (exhaustive); no duplicate index rows in any index; round55 evidence + knowledge-entry rows present and matching landed bytes.

## Method notes / limits

- "Table rows" = README lines matching `^\| \`(knowledge\|lessons)/<name>.md\` \|` and `^\| \`evidence/<dir>/\` \|`; the three webarena/served-endpoint knowledge rows at lines 519/553/554 and the lessons rows at 505/534–541 count as index rows (they sit in round supporting-artifact tables of identical shape).
- Disk counts use all `*.md` (knowledge/lessons) and immediate subdirectories (evidence); evidence root files checked separately (28/28).
- Working tree was live during measurement (seats landing round-55 artifacts); counts are point-in-time at 15:41Z and reproducible from `parity_check.py <lane> <prefix>`.
