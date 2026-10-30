# C7IndexParity — seat report (kengaku round 55, wave 1)

**Seat spec:** coverage no-harm data — index parity both directions at landing time.
**Lane:** `/home/vgpnk/Projects/shokunin/kengaku-shokunin` (cwd was fleet root; all commands used absolute paths or `cd` to my scratch dir).
**Scratch:** `/fast/scratch/hyaku/kengaku-r55/C7IndexParity/` — created, used, **deleted at end** (after copying receipts into the seat dir).
**Writes outside scratch/seat-dir:** none. Read-only on the lane; no git/jj mutation; no subagents; no `agent://all`.

## What I ran (commands + exit codes)

1. Read frozen claims: `plans/round-55-claims.md` (commit `80afa613`) — read-only. Exit 0.
2. `mkdir -p /fast/scratch/hyaku/kengaku-r55/C7IndexParity` — exit 0.
3. Survey: `ls corpus/{knowledge,lessons,evidence}` + `grep -n` of README index sections — exit 0.
4. Wrote `parity_check.py` (README table-row extraction, both-direction diff vs disk, any-mention variant, round55 spot block). Iterated once to fix an evidence trailing-slash normalization bug and to add any-mention checks for knowledge/lessons.
5. Baseline parity at 15:39:01Z: `python3 parity_check.py /home/vgpnk/Projects/shokunin/kengaku-shokunin t0b` → **exit 0**. Result: knowledge 58 files/59 rows (only gap = pending chess entry row), lessons 83/71, evidence 46 dirs/23 rows.
6. Bounded wait per spec (60 s steps, max 25 min): polling loop for `corpus/knowledge/tb2-chess-best-move-grader.md`, log `wait.log` → **FOUND at step 1, 2026-10-30T15:41:28Z, loop exit 0** (total wait ≈ 0 s; the E9 entry landed during my baseline measurement).
7. Landing parity: `python3 parity_check.py <lane> landing` → **exit 0** (full output in `landing.out`, JSON in `landing.json`). Knowledge closed to 59/59.
8. Stale-row sample: spread-sampled 5 table rows per index from `landing.json`, existence-checked against disk (inline Python heredoc) → all 15 exist; exhaustive `rows_without_files=0` in all three indices.
9. Carried-debt check: `git -C <lane> show HEAD:corpus/README.md | grep -c '^| \`lessons/'` → 71 (HEAD) vs 71 (working tree) → the lessons gap is pre-existing, not round-55 harm.
10. Secondary check: evidence root receipts `find corpus/evidence -maxdepth 1 -type f` (28) vs README root-receipt table rows (28) via `comm` → zero diff.
11. R55-C3 surface reads: confirmed landed bytes of `corpus/knowledge/tb2-chess-best-move-grader.md` (13,170 B, S201/S202/S109 pins), `corpus/lessons/round-55.md` (4,573 B), `corpus/evidence/round55/chess-best-move-probe.txt`, README row line 84 + Frontier note line 445 + Round-55 evidence section line 696.

## Files written

- Seat dir `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-55/w1/C7IndexParity/`: `parity.md` (four parity numbers + findings), `parity_check.py`, `t0b.json`, `t0b.out`, `landing.json`, `landing.out`, `wait.log`, `rootfiles.txt`, `rootrows.txt`.
- Scoped findings: `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-55/w1/C7IndexParity.md`.
- Scratch (deleted): `parity_check.py`, `t0/t0b/landing` artifacts, `wait.log`, README.HEAD.md snapshot, rootfiles/rootrows lists.

## Defects found (reported, not fixed — README is E9-owned)

1. **F2** — `lessons/round-55.md` has no README index row. Carried debt: HEAD already shows 71 lessons rows vs the same 83 files; the 12-file unindexed set (round-44v, round-46v, round-47v, round-48v, round-49, round-50, round-50v, round-51v, round-52v, round-53v, round-54v, round-55) predates round 55's landing edits. E9 should close it (add the round-55 row at minimum; ideally the other 11).
2. **F3** — Evidence index two-tier structure: 23/46 dirs have formal table rows; rounds 44+ index evidence only as prose bullets, so 7 dirs (round44/46/50/51/52/53/54) lack any top-level dir mention. Pre-existing pattern; R55-C3's own `evidence/round55` **is** top-level-mentioned (line 698), so no new harm.
3. No stale rows (exhaustive rows→files = 0 in all three indices), no duplicate rows, no orphan knowledge files.

## Dead ends / caveats

- First script version had a trailing-slash normalization defect for evidence paths (all dirs falsely reported unmentioned); caught on the t0 run against the known-good knowledge table and fixed before any output was written.
- The t0 baseline was taken while seats were mid-landing; it is kept as `t0b.*` for the timeline (58/59 → 59/59), not as the acceptance measurement — acceptance is the landing-time run.
- No installs/upgrades were needed; nothing added to PATH. No network calls.

## Verdict for the wave

R55-C3 knowledge-index no-harm: **PASS at landing time** — 59 files vs 59 rows, both directions, zero duplicates, zero stale rows; new entry row (line 84) ↔ landed file close; round55 evidence dir indexed. Open items for E9: the round-55 lessons row (F2) and the carried evidence-index two-tier gap (F3).
