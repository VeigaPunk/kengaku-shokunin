# Round 31 falsify — registry rows and census

Scope: landed `dbb07364` registry additions S092, S093, S100; read-only review. No tools installed.

## Census results

- `cd /home/vgpnk/Projects/shokunin && ./scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kengaku` → exit 0, `kengaku ok`, and 15 W04 records. The added/15th warning is `kengaku W04 S100 duplicate url github.com/laude-institute/terminal-bench-2 across scopes`; source: `corpus/SOURCES.md:113` (S100) and `corpus/SOURCES.md:101` (S079).
- `./scripts/sources-census.sh census --root /home/vgpnk/Projects/shokunin kengaku` → exit 0; rows=91, tier A/B/C=81/8/2, mined/queued/rejected=79/8/4, invalid tiers/statuses=0, missing=0.
- Frozen manual census commands from `/home/vgpnk/Projects/shokunin/CORPUS.md:133-147`, run in `kengaku-shokunin`, yielded rows=91, malformed=0, tier A/B/C=81/8/2, status mined/queued/rejected=79/8/4, no duplicate IDs, no enum/tier-inflation output, and no missing mined used-by path. These registry-wide manual checks do not validate the opened/recheck cells; those were inspected separately below.

## New-row shape and cells

Command: Python split/check of rows in `corpus/SOURCES.md`, plus `awk` recheck-enum check and filesystem existence checks for each used-by path.

- `corpus/SOURCES.md:111` S092 — 11 cells; no pipe inside any cell (the only `|` bytes are the table delimiters); status `mined`, opened `2026-10-25`, recheck `180d`; used-by `corpus/knowledge/benchmark-verifier-execution-model.md` exists.
- `corpus/SOURCES.md:112` S093 — same checks pass; status `mined`, opened `2026-10-25`, recheck `180d`; used-by entry exists.
- `corpus/SOURCES.md:113` S100 — same checks pass; status `mined`, opened `2026-10-25`, recheck `180d`; used-by entry exists.
- Explicit internal-pipe probe: `grep -E '^\| S09[23] |^\| S100 ' corpus/SOURCES.md | grep -c '\\|'` printed `0`; cell counts were 11 each. Contract enums are defined at `/home/vgpnk/Projects/shokunin/CORPUS.md:89-108`; recheck accepted values at `CORPUS.md:105-106`.

## S100↔S079 disposition

Survived the discoverability check. The classification is stated in findable reader-facing corpus text: `corpus/lessons/round-31.md:112-121` calls this the 15th warning, identifies S079 as the same repository used for a different scope, says it is a warning rather than an E finding, and notes the row scope/report disclosure. S100's own scope cell at `corpus/SOURCES.md:113` also explicitly names S079 and distinguishes task-package schema from release identity/verifier execution. The scorecard independently says the 15th W04 is S100↔S079 and “disclosed below” at `SCORECARD.md:1061-1062`.

The exact `SOURCES.md` cell points to the other reading (S079), but the explicit “expected, not a defect” phrasing is in the round lesson's Census section, not in the registry row itself; a reader can find it by the lesson's `## Census` heading.

## VERDICT

VERDICT: The three new registry rows survived the 11-cell, no-internal-pipe, status/opened/recheck, and used-by-exists attacks; the census is clean with 15 W04, the 15th S100↔S079 duplicate is explicitly and findably disclosed, and no row-schema defect fell.
