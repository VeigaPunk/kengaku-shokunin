# RefGroup2 — frozen13 reference map for the six bench-arena baseline knowledge files

Writer/seat: `KengakuR28.RefGroup2-2` (read-only member, RefGroup2, round 28 author-side wave).
Date: 2026-10-21. Lane root: `/home/vgpnk/Projects/shokunin/kengaku-shokunin` (all paths below relative to it).
Assignment: independently map standalone reference IDs among the frozen13 (`S038`, `S049`–`S060`) in exactly six knowledge files, reconstruct each literal citing-file→source status/used-by link from actual sources (historical/code/supersession mentions included, per declared literal contract), and compare with the registry cells in `corpus/SOURCES.md`.

## Scoped result (machine-readable map)

```json
{
  "seat": "KengakuR28.RefGroup2-2",
  "frozen13_ids": ["S038","S049","S050","S051","S052","S053","S054","S055","S056","S057","S058","S059","S060"],
  "reference_pattern": "(?<![A-Za-z0-9_])S[0-9]{3,}(?![A-Za-z0-9_])",
  "scanned_files": {
    "corpus/knowledge/bench-arena-round11-power.md": 102,
    "corpus/knowledge/bench-arena-round12-ladder.md": 284,
    "corpus/knowledge/bench-arena-round5-battery.md": 111,
    "corpus/knowledge/bench-arena-round6-stability.md": 103,
    "corpus/knowledge/bench-arena-round7-noise-n25.md": 107,
    "corpus/knowledge/bench-arena-round7-scaffold-ablation.md": 135
  },
  "scanned_lines_total": 842,
  "standalone_frozen13_mentions": [],
  "mentions_by_file": {
    "corpus/knowledge/bench-arena-round11-power.md": {"frozen13_standalone": 0, "any_uppercase_S_digit_token": 0},
    "corpus/knowledge/bench-arena-round12-ladder.md": {"frozen13_standalone": 0, "any_uppercase_S_digit_token": 0},
    "corpus/knowledge/bench-arena-round5-battery.md": {"frozen13_standalone": 0, "any_uppercase_S_digit_token": 0},
    "corpus/knowledge/bench-arena-round6-stability.md": {"frozen13_standalone": 0, "any_uppercase_S_digit_token": 0},
    "corpus/knowledge/bench-arena-round7-noise-n25.md": {"frozen13_standalone": 0, "any_uppercase_S_digit_token": 0},
    "corpus/knowledge/bench-arena-round7-scaffold-ablation.md": {"frozen13_standalone": 0, "any_uppercase_S_digit_token": 0}
  },
  "citing_file_to_source_links_from_my_slice": [],
  "registry_cells_observed": {
    "S038": {"sources_md_line": 60, "status": "queued", "used_by": "-", "used_by_lists_my_files": false},
    "S049": {"status": "mined", "used_by": ["corpus/lessons/round-27.md", "corpus/knowledge/extraction-policy-comparison.md"]},
    "S050": {"status": "mined", "used_by": ["corpus/lessons/round-27.md"]},
    "S051": {"status": "mined", "used_by": ["corpus/lessons/round-27.md", "corpus/knowledge/extraction-policy-comparison.md"]},
    "S052": {"status": "mined", "used_by": ["corpus/lessons/round-27.md", "corpus/knowledge/extraction-policy-comparison.md"]},
    "S053": {"status": "mined", "used_by": ["corpus/lessons/round-27.md", "corpus/knowledge/extraction-policy-comparison.md"]},
    "S054": {"status": "mined", "used_by": ["corpus/lessons/round-27.md", "corpus/knowledge/extraction-policy-comparison.md"]},
    "S055": {"status": "mined", "used_by": ["corpus/lessons/round-27.md", "corpus/knowledge/extraction-policy-comparison.md"]},
    "S056": {"status": "mined", "used_by": ["corpus/lessons/round-27.md", "corpus/knowledge/extraction-policy-comparison.md"]},
    "S057": {"status": "mined", "used_by": ["corpus/lessons/round-27.md", "corpus/knowledge/extraction-policy-comparison.md"]},
    "S058": {"status": "mined", "used_by": ["corpus/lessons/round-27.md", "corpus/knowledge/extraction-policy-comparison.md"]},
    "S059": {"status": "mined", "used_by": ["corpus/lessons/round-27.md", "corpus/knowledge/extraction-policy-comparison.md"]},
    "S060": {"status": "rejected", "used_by": ["corpus/lessons/round-27.md"]}
  },
  "missing_used_by_links_in_my_slice": [],
  "missing_frozen_files_in_my_slice": [],
  "cited_but_queued_in_my_slice": [],
  "s038_known_drift": {
    "disclosed": "round27 (M65 lead; corpus/lessons/round-27.md:18 'S038's cited-but-queued drift was independently found by RevengeMistakeMine')",
    "citing_frozen_knowledge_path": "corpus/knowledge/attribution-interval-calibration.md",
    "citing_location": "corpus/knowledge/attribution-interval-calibration.md:144",
    "exact_registry_cell": "corpus/SOURCES.md:60 used-by cell is '-' (em dash placeholder) and status cell is 'queued'",
    "defects": [
      "status drift: cited by a frozen knowledge path yet status=queued (contract requires mined)",
      "used-by drift: citing frozen path absent from used-by cell ('-')"
    ],
    "outside_my_slice": true,
    "corpus_wide_S038_citation_check": "grep of standalone S038 across corpus/ finds it cited in exactly one knowledge file (attribution-interval-calibration.md:144); all other hits are SOURCES.md itself, corpus/evidence/round25-sources/gate.md, corpus/evidence/round26-calibration/preservation-and-source-census.json, and lessons (round-25, round-25-verifier-spotcheck, round-27) - none of which are frozen knowledge paths or my six files",
    "suffices_for_my_slice": true
  },
  "slice_verdict": "PASS",
  "slice_verdict_meaning": "Within the six assigned files: zero standalone frozen13 references exist, so no missing used-by links, no cited-but-queued rows, and no drift beyond the already-disclosed S038 drift are attributable to this slice. No file edit is owed from this seat."
}
```

## Evidence chain (observed, exact locations)

1. Pattern scan, exact frozen pattern `(?<![A-Za-z0-9_])S[0-9]{3,}(?![A-Za-z0-9_])` (as persisted in `plans/fixtures/r28/registry/population.json`), over all six files: **no matches**. Grep scans raw file bytes including fenced code blocks, tables, and quotes, so the declared literal contract's fence/quote inclusivity is satisfied by construction (vacuously — zero hits of any kind).
2. Stronger loose scan `S[0-9]` (any uppercase S followed by a digit, standalone or not) over the same six files: **no matches**. The files therefore contain no S-prefixed source tokens at all, not merely no standalone ones. Line coverage: 842/842 lines (`wc -l` counts in the map above).
3. Registry cells read at exact bytes: `corpus/SOURCES.md:60` (S038: `| queued | 2026-10-20 | 180d | — |` — status queued, used-by placeholder `—`) and `corpus/SOURCES.md:71-82` (S049–S060 statuses/used-by as tabulated above; S050 and S060 list only `corpus/lessons/round-27.md`).
4. S038 drift reconstruction from actual sources: the sole citing frozen knowledge path is `corpus/knowledge/attribution-interval-calibration.md` (mention at line 144: "S038 (Reiczigel et al. 2010, Introduction) warns the naive adjusted interval can cover 60% at nominal 95%."). Registry used-by does not list it and status is `queued`. Both contract defects ("Cited rows must be `mined` and list every citing frozen path", plans/round-28-claims.md C2 bullet) are present in this one row and nowhere else that this slice can see.
5. Contract cross-check of the other 12 rows: none of S049–S060 is cited by any of my six files (obligation direction 1 vacuous), and none of their used-by cells lists any of my six files (obligation direction 2 vacuous). S060 is `rejected` yet listed by lesson `corpus/lessons/round-27.md`; under the declared contract this is not an error — lessons are "additional lesson used-by paths ... allowed and not required to match", and "Uncited rejected/queued rows are not errors" (cited = cited from a frozen knowledge path). Recorded as a scoped interpretation, not new doctrine.

## Comparison with registry cells — exact missing links

- Missing links attributable to my six files: **none** (the set is empty by the zero-mention result above).
- The only frozen13 mismatch visible in the C2 population remains the disclosed S038 drift at `corpus/knowledge/attribution-interval-calibration.md:144` vs `corpus/SOURCES.md:60` — a path this seat does not own and did not audit beyond locating the drift.
- **Does the known S038 drift suffice?** For this slice: yes. My six files contribute zero standalone frozen13 references, so within-slice consistency is complete and the corpus-level mismatch count attributable to this slice is exactly 0. Whether S038's repair suffices corpus-wide (forecast F5, p=.55) additionally depends on slices this seat does not own (`attribution-interval-calibration.md`, `extraction-policy-comparison.md`, other bench-arena files) — out of scope here, no claim made.

## Limitations

- Read-only seat: no files under the six paths, SOURCES.md, or population.json were modified; no builds/tests/checkers were run (production checks forbidden mid-flight). The map is an independent reconstruction from raw bytes, not a `plans/registry_check.py` run; that checker's own exit codes are separate evidence to be produced at integration.
- Mentions outside the six files (including whether `corpus/knowledge/extraction-policy-comparison.md` actually cites each of S049–S059 its used-by cells claim) were not audited — other seats own those paths; only the S038 locating grep crossed corpus/ and it was limited to one ID.
- No external sources were opened this round (no new source rows admitted or proposed); all evidence is lane-internal bytes read 2026-10-21.
- The zero-mention result is stated against the frozen uppercase pattern; lowercase or spacing-mangled forms (`s038`, `S 038`) are outside the declared literal contract and were not treated as references.

## Final scoped verdict

**PASS** — scoped strictly to the six assigned files (`bench-arena-round11-power.md`, `bench-arena-round12-ladder.md`, `bench-arena-round5-battery.md`, `bench-arena-round6-stability.md`, `bench-arena-round7-noise-n25.md`, `bench-arena-round7-scaffold-ablation.md`) and the frozen13 IDs: zero standalone references exist, no used-by links are missing from this slice, no cited-but-queued rows originate here, and the disclosed S038 drift is fully external to this slice (vacuously sufficient for it). This is not a blanket round PASS and makes no claim about the other 29 frozen knowledge paths.

— KengakuR28.RefGroup2-2, 2026-10-21
