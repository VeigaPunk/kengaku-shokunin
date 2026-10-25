# RefGroup3 — frozen-reference map

**Writer/seat:** KengakuR28.RefGroup3-2 (author-side, read-only mapping)
**Scope:** only the six assigned baseline knowledge paths and frozen IDs S038, S049–S060. This is not a C2-wide verdict.

```json
{
  "baseline_revision": "b9b24796277020d1b9b01923b45313d6a565e664",
  "population": "plans/fixtures/r28/registry/population.json",
  "reference_pattern": "(?<![A-Za-z0-9_])S[0-9]{3,}(?![A-Za-z0-9_])",
  "knowledge_file_frozen_id_mentions": {
    "corpus/knowledge/bench-arena-round8-horizon.md": [],
    "corpus/knowledge/bench-arena-round9-replication.md": [],
    "corpus/knowledge/bench-arena-task27-timeout-anatomy.md": [],
    "corpus/knowledge/benchmark-saturation-and-lifecycle.md": [],
    "corpus/knowledge/benchmark-selection.md": [],
    "corpus/knowledge/contamination-detection-and-transparency.md": []
  },
  "literal_reference_edges": [],
  "registry_cells": {
    "S038": {"status": "queued", "used_by": []},
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
  "missing_registry_used_by_links_for_scope": [],
  "s038_drift": {
    "registry_location": "corpus/SOURCES.md:60",
    "observed_cell": "queued; used-by —",
    "assigned_files_citing_s038": [],
    "assessment": "Not a mismatch in this six-file slice. It accounts for no missing link here; this slice cannot establish whether the known S038 drift suffices for the full 13-ID/35-file C2 population."
  },
  "non_population_ids_seen": {
    "corpus/knowledge/benchmark-saturation-and-lifecycle.md": ["S007", "S008"],
    "corpus/knowledge/contamination-detection-and-transparency.md": ["S001", "S002", "S003", "S004"]
  },
  "verdict": "PASS for the assigned six-file reference mapping only"
}
```

## Evidence and method

- `plans/fixtures/r28/registry/population.json` pins the 13 IDs, literal regex, 35-path population, and rule that historical/corrective mentions count. I scanned every line of each assigned path with that literal token rule (including the complete-file search, not only the displayed excerpts). There are no S038 or S049–S060 mentions; therefore there is no citing-file→source edge in this slice, including no historical, code, or supersession edge.
- `corpus/SOURCES.md:60` is the complete S038 row: status `queued`, used-by `—`. Rows `corpus/SOURCES.md:71-82` give S049–S060 statuses and used-by paths shown above. None of those used-by cells lists any of the six assigned files. This is consistent with their zero frozen-ID mentions; no missing link is indicated.
- Out-of-population IDs are retained in the map to make the boundary explicit: S007/S008 occur in `benchmark-saturation-and-lifecycle.md`; S001/S002/S004 occur in `contamination-detection-and-transparency.md`, and S003 occurs in its rejected-reference discussion. They are not in this frozen13 mapping.
- Baseline check: read-only `git diff --name-status b9b24796277020d1b9b01923b45313d6a565e664 -- <six assigned paths>` returned no output, so no path difference from the pinned baseline was observed.

**Commands/tools observed:** `read` on the claims, population, six assigned files, and relevant registry rows; literal-pattern `grep` on the six paths; the read-only baseline `git diff --name-status` above. No installs/updates, builds, tests, or source edits.

**Limitations:** this maps only the six assigned files. It does not inspect the other 29 frozen paths or decide semantic citation support, nor can it decide the C2-wide S038 sufficiency question. Registry statuses/usages are reported from the observed `corpus/SOURCES.md` cells.

**Final scoped verdict: PASS.** No frozen reference in the assigned paths is missing from registry used-by cells. The observed S038 queued row is outside this slice's cited references and cannot be used here as evidence that the known cross-population drift is—or is not—sufficient overall.