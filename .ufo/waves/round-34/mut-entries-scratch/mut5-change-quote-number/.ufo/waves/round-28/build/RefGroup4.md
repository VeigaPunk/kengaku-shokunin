# RefGroup4 — round28 C2 reference map, files: eval-design-digest-2/3, eval-prior-art-calibration, eval-theory-notes, extraction-policy-comparison, gemini-benchmark-suite

- **Writer/seat:** KengakuR28.RefGroup4-2 (read-only leaf member; no subagents dispatched)
- **Date:** 2026-10-21
- **Assignment:** Independently map standalone reference IDs among frozen13 (S038, S049–S060) in the 6 assigned knowledge files; reconstruct each literal citing-file→source status/used-by link from actual sources (historical/code/supersession mentions included, per declared literal contract); compare with registry cells; state whether known S038 drift suffices.
- **Report trailer path (lane-relative):** `.ufo/waves/round-28/build/RefGroup4.md`
- **Scratch evidence:** `.ufo/waves/round-28/scratch/RefGroup4-2/mentions-census.txt`

## Method and observed commands

- Population/pattern taken from `plans/fixtures/r28/registry/population.json` (`reference_pattern`: `(?<![A-Za-z0-9_])S[0-9]{3,}(?![A-Za-z0-9_])`; base_revision b9b24796277020d1b9b01923b45313d6a565e664).
- Mentions enumerated with the `grep` tool over the 6 files using exactly the population pattern; independently re-counted with `grep -oP '(?<![A-Za-z0-9_])S[0-9]{3,}(?![A-Za-z0-9_])' <file> | sort | uniq -c` (counts identical; raw output in scratch file).
- Registry cells read from `corpus/SOURCES.md` Registry section: S038 row line 60, S049 line 71, S050 line 72, S051 line 73, S052–S060 lines 74–82 (read `:raw` for lines 60, 71–73 to avoid cell truncation; S052–S060 rows read whole, untruncated, in the full-file read).
- Working-tree revision anchor: `git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin rev-parse HEAD` (read-only; recorded below).
- No external source opened; no upstream code executed; no registry/checker run (registry_check.py execution belongs to the executor seats, not this seat). No tool installed (none needed).

## Mention census (standalone, literal, quoting/code-fence context ignored per contract)

| file | standalone mentions among frozen13 |
|---|---|
| `corpus/knowledge/eval-design-digest-2.md` | none |
| `corpus/knowledge/eval-design-digest-3.md` | none |
| `corpus/knowledge/eval-prior-art-calibration.md` | none |
| `corpus/knowledge/eval-theory-notes.md` | none |
| `corpus/knowledge/gemini-benchmark-suite.md` | none |
| `corpus/knowledge/extraction-policy-comparison.md` | 21 mentions / 11 distinct IDs (S049×2, S050×1, S051×2, S052×2, S053×2, S054×2, S055×2, S056×1, S057×3, S058×2, S059×2) |

Mention lines in `extraction-policy-comparison.md`: S049 [1,17], S050 [18], S051 [1,21], S052 [1,49], S053 [1,51], S054 [1,51], S055 [1,20], S056 [1], S057 [1,16,24], S058 [1,18], S059 [1,53]. Line 1 is the file's `source:` header; per the literal contract those mentions count like any other. S038 and S060 are **not** mentioned in any of the 6 files (S060 appears only in `corpus/lessons/round-27.md`, which is not one of my files).

## Machine-readable map (citing file → source status / used-by reconstruction vs registry)

Registry = `corpus/SOURCES.md` rows at the line numbers above; "expected used-by" = the set of frozen files literally citing the ID.

```json
{
  "seat": "KengakuR28.RefGroup4-2",
  "scope_files": [
    "corpus/knowledge/eval-design-digest-2.md",
    "corpus/knowledge/eval-design-digest-3.md",
    "corpus/knowledge/eval-prior-art-calibration.md",
    "corpus/knowledge/eval-theory-notes.md",
    "corpus/knowledge/extraction-policy-comparison.md",
    "corpus/knowledge/gemini-benchmark-suite.md"
  ],
  "mentions": {
    "corpus/knowledge/eval-design-digest-2.md": {},
    "corpus/knowledge/eval-design-digest-3.md": {},
    "corpus/knowledge/eval-prior-art-calibration.md": {},
    "corpus/knowledge/eval-theory-notes.md": {},
    "corpus/knowledge/gemini-benchmark-suite.md": {},
    "corpus/knowledge/extraction-policy-comparison.md": {
      "S049": [1, 17], "S050": [18], "S051": [1, 21], "S052": [1, 49],
      "S053": [1, 51], "S054": [1, 51], "S055": [1, 20], "S056": [1],
      "S057": [1, 16, 24], "S058": [1, 18], "S059": [1, 53]
    }
  },
  "links": {
    "S038": {"status": "queued", "registry_used_by": [], "cited_in_scope": false, "finding": "none-in-scope"},
    "S049": {"status": "mined", "registry_used_by": ["corpus/lessons/round-27.md", "corpus/knowledge/extraction-policy-comparison.md"], "missing_used_by": []},
    "S050": {"status": "mined", "registry_used_by": ["corpus/lessons/round-27.md"], "missing_used_by": ["corpus/knowledge/extraction-policy-comparison.md"]},
    "S051": {"status": "mined", "registry_used_by": ["corpus/lessons/round-27.md", "corpus/knowledge/extraction-policy-comparison.md"], "missing_used_by": []},
    "S052": {"status": "mined", "registry_used_by": ["corpus/lessons/round-27.md", "corpus/knowledge/extraction-policy-comparison.md"], "missing_used_by": []},
    "S053": {"status": "mined", "registry_used_by": ["corpus/lessons/round-27.md", "corpus/knowledge/extraction-policy-comparison.md"], "missing_used_by": []},
    "S054": {"status": "mined", "registry_used_by": ["corpus/lessons/round-27.md", "corpus/knowledge/extraction-policy-comparison.md"], "missing_used_by": []},
    "S055": {"status": "mined", "registry_used_by": ["corpus/lessons/round-27.md", "corpus/knowledge/extraction-policy-comparison.md"], "missing_used_by": []},
    "S056": {"status": "mined", "registry_used_by": ["corpus/lessons/round-27.md", "corpus/knowledge/extraction-policy-comparison.md"], "missing_used_by": []},
    "S057": {"status": "mined", "registry_used_by": ["corpus/lessons/round-27.md", "corpus/knowledge/extraction-policy-comparison.md"], "missing_used_by": []},
    "S058": {"status": "mined", "registry_used_by": ["corpus/lessons/round-27.md", "corpus/knowledge/extraction-policy-comparison.md"], "missing_used_by": []},
    "S059": {"status": "mined", "registry_used_by": ["corpus/lessons/round-27.md", "corpus/knowledge/extraction-policy-comparison.md"], "missing_used_by": []},
    "S060": {"status": "rejected", "registry_used_by": ["corpus/lessons/round-27.md"], "cited_in_scope": false, "finding": "none-in-scope"}
  }
}
```

## Exact missing links and the S038-drift question

1. **MISSING USED-BY (the only mismatch in this scope):** `corpus/knowledge/extraction-policy-comparison.md:18` cites S050 — quote (8 words, accessed 2026-10-21 from the lane working tree): "(`S058`, correcting `S050`) takes a first regex hit". This is a supersession mention of a superseded row; the declared contract counts it literally. But `corpus/SOURCES.md:72` (S050, status `mined`) ends its used-by cell with exactly `corpus/lessons/round-27.md` — `corpus/knowledge/extraction-policy-comparison.md` is absent. Contract clause violated: "Cited rows must be `mined` and list every citing frozen path." S050's status is fine (`mined`); only the used-by cell is short by one path.
2. **Known S038 drift does NOT suffice for this scope.** S038 (`corpus/SOURCES.md:60`) is status `queued` with used-by `—`; the disclosed round27 drift is cited-but-queued in attribution-side files. In my 6 files S038 has **zero** mentions, so an S038-only allowed-cell repair leaves the S050 gap unresolved. This realizes the F5 uncertainty ("other rows uninspected", p=.55): at least one non-S038 drift exists inside the frozen population. Conversely, no cited row in my scope is non-`mined` (the S050 row is mined), so there is no cited-queued/rejected violation here.
3. All other cited IDs (S049, S051–S059) are `mined` and their used-by cells already list `corpus/knowledge/extraction-policy-comparison.md` → clean. S060 (`rejected`) and S038 (`queued`) are uncited in this scope → "uncited rejected/queued rows are not errors" holds.

Repair note (for the integrating seat, not an edit by me): the S050 fix is a used-by cell append — a column the round already treats as mutable for the S038 repair; status/recheck/opened/teaching cells stay untouched. Whether it belongs to the same allowed-cell amendment is an L1 decision.

## Limitations

- Literal scan only; no semantic citation-support judgment (per declared contract). Quoting and code-fence contexts are not exempted, and none occur here (the 21 mentions are all plain prose/header text).
- Coverage is exactly the 6 assigned files; the other 29 baseline35 paths belong to sibling RefGroup seats. No claim about them.
- Registry read at the lane working tree, revision recorded below; I did not diff it against base b9b2479 byte-for-byte (read-only seat, no VCS state inspection beyond rev-parse).
- `registry_check.py` was not run and its implementation not read (not assigned; independent-oracle hygiene). Executor seats own the before/after counts.

## Scoped verdict

**Mapping: PASS** — complete mention census and per-ID status/used-by reconstruction for all 6 assigned files. **Scoped registry consistency for these 6 files: FAIL (1 finding)** — S050 used-by omits its citing frozen path `corpus/knowledge/extraction-policy-comparison.md`; the known S038 drift does not cover it. This is author-side advice on one slice of C2, not a blanket round verdict.

## Trailer

- Report: `.ufo/waves/round-28/build/RefGroup4.md` (this file)
- Scratch: `.ufo/waves/round-28/scratch/RefGroup4-2/mentions-census.txt`
- Working-tree HEAD at read time: `f0ba09be0f3066daba2134b943d973ad1588f34a` (the round-28 preregistration commit; see scratch `revision.txt`).
