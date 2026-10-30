# C7IndexParity — scoped findings (round 55, wave 1)

Coverage no-harm check: corpus README index parity, both directions, measured at landing time
(2026-10-30T15:41Z on the working tree at tip `80afa613` + round-55 landing edits).
Full data: `.ufo/waves/round-55/w1/C7IndexParity/parity.md` (+ `parity_check.py`, `landing.json`, `t0b.json`, `wait.log`).

## Four parity numbers (README table-row index ↔ disk)

| Index | Disk | Rows | orphans (file→row) | stale (row→file) | dupes |
|---|---|---|---|---|---|
| knowledge `*.md` | 59 | 59 | 0 | 0 | 0 |
| lessons `*.md` | 83 | 71 | 12 | 0 | 0 |
| evidence dirs | 46 | 23 | 23 (F3) | 0 | 0 |

Secondary: evidence root receipt logs 28 files vs 28 rows — exact parity.

## Landing confirmations (R55-C3 surfaces, E9-owned)

- `knowledge/tb2-chess-best-move-grader.md` — file landed 15:41Z; index row present (README line 84); Frontier note line 445. Both directions close.
- `evidence/round55/` — dir + `chess-best-move-probe.txt` present; top-level bullet at README line 698 under "### Round-55 evidence (2026-10-30)".
- Old-row staleness: 5-row spread sample per index (15 rows) all exist; exhaustive `rows_without_files=0` in all three indices. **No old row went stale.**

## Findings

- **F1 (pass):** knowledge index parity closed at landing — 59/59 both directions; the only t0 gap was the pre-written row for the pending entry, closed when the file landed.
- **F2 (E9 to fix):** `lessons/round-55.md` (4,573 B, on disk 12:22Z) has **no index row**. Carried debt, not new harm: HEAD README already has 71 lessons rows vs 83 files, unchanged by round-55 edits (71→71). Full 12-file unindexed list in `parity.md`.
- **F3 (structural, pre-existing):** evidence index is two-tier — 23/46 dirs carry formal table rows; rounds 44+ index evidence only via prose bullets, leaving 7 dirs (round44/46/50/51/52/53/54) without a top-level mention. `evidence/round55` **is** mentioned (line 698), so R55-C3's own evidence is indexed at parity with recent rounds. Zero dangling evidence rows (`mentions_without_dirs=0`).

**No new harm detected.** Verdict: R55-C3 knowledge/evidence index no-harm **PASS** at landing time.
