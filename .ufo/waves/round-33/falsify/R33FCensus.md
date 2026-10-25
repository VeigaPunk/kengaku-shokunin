# R33FCensus — SOURCES census after C1 (round 33 falsify, hyaku run 7)

Seat: `KengakuR33.R33FCensus` (leaf). Target: SOURCES census after C1 and before/after row deltas.
Access date 2026-10-25. Lane: `/home/vgpnk/Projects/shokunin/kengaku-shokunin`.
Tree observed: lane HEAD `77ac8c1` (`77ac8c1307ba60e9572a7e2789b71ae31b133440`), working-tree `corpus/SOURCES.md`
equals HEAD (unmodified in `git status`); sibling waves' uncommitted paths present elsewhere in the tree.

## Command executed (verbatim)

```
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kengaku
```

Observed (stdout, 16 lines): 15 `W04` lines, then
`kengaku	ok	/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/SOURCES.md`.
Exit **0**. No `E` codes, no other `W` codes (`grep -cE '^kengaku\tE'` = 0).

## Comparison vs frozen `.ufo/waves/round-33/claims/census-before.txt`

`diff` on full outputs: **only lines 1 and 18 differ** — the frozen header
(`# census before (round 33 start, 2026-10-25)`) and the frozen `exit=0` trailer (the frozen control file
carries the trailer; the live runner prints it to the shell, not to stdout — exit captured separately as 0).
All 15 `W04` lines and the `kengaku ok` line are **byte-identical**.

W04 ids (both): S040 S048 S057 S058 S059 S064 S065 S066 S067 S068 S069 S071 S075 S076 S100.

**W04 delta = 0.** Errors: 0 both before and after.

## Independent counts (read-only; not derived from the script)

Per frozen claims: freeze baseline `112091c` had registry 95 rows, ids ≤ S102, S103+ unused,
40 knowledge files. Commits: `7895588` rows=95 → `b54feca` (C1 admission) rows=97 → HEAD `77ac8c1`
rows=97.

| metric | freeze (112091c) | now (HEAD + w.t.) |
|---|---|---|
| registry rows (`^\| *S[0-9]{3} *\|`) | 95 | **97** (+S103, +S104) |
| script census mode `rows` | — | **97** |
| tier A | 81 | **82** |
| tier B | 12 | **13** |
| tier C | 2 | 2 |
| status mined / queued / rejected | — | 81 / 8 / 8 |
| `corpus/knowledge/` files | 40 | **41** |
| knowledge index rows in `corpus/README.md` | 40 | 41 |

S103/S104 tiers (independent): **S103 = A (code)** — Toolathlon
`tasks/finalpool/ab-testing/evaluation/main.py` @ `9be8d8fe…`, `status=mined`,
`opened=2026-10-25`, `used-by=corpus/knowledge/benchmark-grader-semantics.md`.
**S104 = B (paper)** — arXiv 2412.05579v2, `status=mined`, `opened=2026-10-25`, same `used-by`.
S093 also `mined` / `2026-10-25` with `used-by` now naming both benchmark-verifier-execution-model.md and
benchmark-grader-semantics.md.

Entry `corpus/knowledge/benchmark-grader-semantics.md`: `source:` lines cite exactly S093, S103, S104,
with `verified-at: 2026-10-25`; exactly one index row in `corpus/README.md` (line 67).

`python3 plans/adoption_check.py --expect .ufo/waves/round-33/claims/adoption-expect.json --census` →
`entries=1 indexed=1 cited_rows=3 rows_present=3 rows_mined=3 usedby_ok=1 census=ok`, **exit 0**.

## Independent duplicate-URL audit (Python emulation of the script's rule)

Replicated `url_of` (scheme strip, lowercased host, fragment/trailing-slash removal) over the `## Registry`
section, 0–3-space rows. All 97 rows have the 11 content columns (script NF=13 check passes).

- 14 normalized first-URL duplicate groups. The script's W04 fires for each later occurrence whose `scope`
  differs from the first; the emitted set reproduces the 15 frozen W04 ids exactly (id-set identity).
- Same-scope duplicate pairs are suppressed exactly as the code prescribes: S042 `teaches` contains
  `supersedes S030`, S039 contains `supersedes S034`; S023/S026 are `rejected` (E04 suppresses on
  `status=rejected`). No E04 is emitted — consistent with exit 0.
- **S103 has a two-URL source cell** (`https://github.com/hkust-nlp/Toolathlon` + pinned blob URL).
  The census's `url_of` consumes only the first URL, so the pinned blob is invisible to dedupe. Independent
  check of *all* URL positions finds no other row sharing the blob (or the root), so no duplicate is missed
  in practice — but the multi-URL blind spot is real (also S041/S045 cells carry a second JSON URL).

## Coverage limitation observed (does not change verdict, worth routing)

- **Same-repo/same-commit family not flagged:** S080 (`https://raw.githubusercontent.com/hkust-nlp/Toolathlon/9be8d8fe…/README.md`)
  and S103 (repo root + blob @ the *same* commit `9be8d8fe07a497b18ee61e3f2ae694e9797f39eb`) are
  different URL strings, so the exact-URL W04 rule stays silent even though C1 opens a second Toolathlon row
  at the same pinned commit. Consistent with build report R33C1KillRule.md §"Census passing on duplicate
  URLs (W04 only)" (UNCAUGHT) — W04 is a warning by design and never affects clean-lane exit.
- 15 W04 previous → 15 after: S103/S104 introduced **no new normalized duplicate** (root URL appears in no
  other kengaku row; arXiv 2412.05579 appears in no other row).

## Verdict

Frozen claim **"census exit 0 with 15 W04"** (and the C1 post-append census property) **holds**:
after C1, registry rows 95 → 97 (S103/A, S104/B), knowledge files 40 → 41, W04 set unchanged (delta 0),
no E errors, exit 0, adoption census `ok`.
No caught defect in the census/falsification sense; two boundary limitations recorded above (multi-URL cell
visibility, same-repo URL-family silence) for the L1's post-integration gate.

## Evidence retained

- `/tmp/census-now.txt` — live validate output (16 lines, exit 0).
- `diff` frozen vs live: only header/trailer differ.
- Commit-row table: 7895588=95, b54feca=97, c1a520d=97, 77ac8c1=97.
- Script census mode: `rows 97, tier.A 82, tier.B 13, tier.C 2, status.mined 81, queued 8, rejected 8,
  missing 0`, exit 0.
- Emulation logs (W04 ids, groups, E04 suppression) computed by `/tmp/r33f-census-audit.py` (read-only).

`VERDICT: holds (delta 0, no errors; 2 boundary limitations recorded)`

## L1 integration correction

The frozen claim's `40` knowledge/index baseline is wrong: independent `git ls-tree` and README counts at `112091c2` are 41/41, and the final tree is 41/41 (no net file or index-row change). Registry rows still move 95→97, with S103 tier A and S104 tier B; W04 stays 15. The final S103 source cell is now blob-only, so the report's earlier multi-URL-cell observation for S103 no longer applies; the general fact that the census inspects only the first URL remains. This report was first written to the fleet root by mistake, then copied byte-exact into lane reportDir and the fleet copy removed.
