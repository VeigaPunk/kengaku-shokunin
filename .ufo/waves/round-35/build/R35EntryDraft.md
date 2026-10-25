# R35EntryDraft — C1 knowledge-entry draft (scribe)

Seat: R35EntryDraft (leaf; no subagents). Draft path:
`.ufo/waves/round-35/build/R35EntryDraft/entry.md` (the lane's file at
`corpus/knowledge/tb2-protein-assembly-grader.md` is the L1's to integrate; not touched).

## Deliverable

The C1 entry draft for S105/S106/S107, built to satisfy counter V3/V5 exactly.

### Header (lines 1–5, as V3 requires)

1. `source: S105 — <bare pinned URL>/protein-assembly/tests/test_outputs.py — test_gblock, lines 10–73, commit 2fd12b88…, accessed 2026-10-25`
2. `source: S106 — <bare pinned URL>/protein-assembly/tests/test.sh — reward mapping, lines 18–30, same commit, accessed 2026-10-25`
3. `source: S107 — <bare pinned URL>/protein-assembly/instruction.md — requirement bullets, lines 9–34, same commit, accessed 2026-10-25`
4. `verified-at: 2026-10-25`
5. `recheck: 180d — re-fetch the three pinned URLs, `sha256sum -c corpus/evidence/round35/tb2-eval/SHA256SUMS`, and re-run `plans/tb2_grader_probe.py`; any digest or receipt change supersedes this entry`

URLs are the bare pinned raw URLs (no `/tasks/`, no fragment) — fixes R34Review finding 1.

### Sections

- Summary (binary reward; grader reads only `/app/gblock.txt`; five amino-acid literals; probe 18 cases).
- Source labels: S105–S107 are the benchmark maintainers' own task files — primary for what the grader checks, self-report for everything else (comments' PDB/FPbase claims are the authors' statements, not verified here); probe receipt is the lane's own re-runnable gate output. (Fixes critic finding 1; labels sources as maintainer task code, not independent.)
- Named extended coverage row: `corpus/README.md` §Frontier round-33 clause, quoted ("the clause stays open for the other benchmarks' scoring code (Terminal-Bench 2.0's …)"), discharged for this one task only. (Fixes review finding 5.)
- Load-bearing grader logic table (static reading) + instruction-requirement → assertion table (executed).
- Probe receipt summary verbatim: `cases=18 observed_pass=5 observed_fail=13 mismatches=0`, plus findings: G-only linker passes (`[GS]+`); 3000-nt cap never decides an otherwise-passing gBlock (`max_passing_nt=2766` = 3×(842+80)); one-residue donor substitution fails with the *order* message (`find` → −1); donor-repeated fails on length first (3378 nt); expected proteins are literals; environment files (`pdb_ids.txt`, `antibody.fasta`, plasmid, FPbase/PDB API) are never read.
- `## Negative space` with falsifier sentence: re-fetch yields different SHA-256 vs `tb2-eval/SHA256SUMS`, or fresh probe summary differs (e.g. `linker-g-only` observed `fail`). Also non-claims: literal correctness vs PDB/FPbase/antibody, biological correctness, Harbor runtime execution, models/trajectories, PROVINCE task validity, other 88 TB2 tasks.
- `## Located quotes`: 26 rows, exact form `| claim | “quote” | `file:NN` |`, all byte-exact (verified, below).

### R34 findings disposition

- R34CriticEntryTB2: no S092/S100 assertions without quotes (S100/S103/S104 named only as other entries covering other surfaces, nothing restated); no over-grounded "expected-artifact grounding" (negative space + source labels bound it); no "all the requirements" overclaim (scope explicitly delimited).
- R34ReviewEntryTB2: corrected URLs; quote coverage added for strip/lowercase (16/21), alphabet (22), length cap (23), find call (38), order message (43), conditional reward `if` (test.sh:26), pytest invocation (test.sh:23); falsifier present; extended coverage row named.

## Verification (all executed)

Fixture clone (sparse, `--shared`, `master`, toplevel verified): `mktemp -d /tmp/k35-XXXX`; lanes captures copied from the lane (`tb2-eval/*`, receipt); draft placed at the clone's `corpus/knowledge/tb2-protein-assembly-grader.md`.

1. **Quote self-check** (Python replicating V3's row regex + span substring + word count, per capture file):
   `quote rows parsed: 26` / `defects: 0`; every quote also grep-hit on its cited line
   (e.g. `test_outputs.py:43 hit=[43] words=16`, `instruction.md:33 hit=[33] words=19`,
   `test.sh:26 hit=[26] words=7`). Word counts all ≤25.
2. **Counter run** on the fixture (`python3 plans/round35_c1_verify.py --lane .`, uv 0.13.0,
   biopython via fallback `uv run --no-project --with biopython==1.85`):
   `V1 ok` / `V3 ok` / `V5 ok`; `V2 DEFECT S105 present 0 times`, `V4 DEFECT index row absent…`,
   `V6 DEFECT census exit 1` — all three depend on L1 integration (SOURCES.md rows
   S105–S107, README index/coverage merge, census post-rows) and are outside a leaf scribe's
   write scope. Exit 1, `checks=6 defects=3`.

## Out-of-scope (for L1)

- `corpus/SOURCES.md` rows S105/S106/S107 (11 cells, tier A, mined, opened 2026-10-25, pinned URL, used-by = entry path) — V2.
- `corpus/README.md` index row + coverage-map bullet for the entry (the live lane already carries them; clone-at-master does not) — V4.
- Final placement of the entry at `corpus/knowledge/tb2-protein-assembly-grader.md` and census validation — V6.
- Capture manifest (`tb2-eval/SHA256SUMS`) already lists the three grader files at the pinned digests (V1 ok).

VERDICT: entry-drafted-26-quotes
