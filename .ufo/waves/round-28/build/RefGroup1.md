# RefGroup1 — frozen13 standalone-reference map, six baseline knowledge files

- **Writer/seat:** KengakuR28.RefGroup1-2 (read-only leaf member; no subagents dispatched)
- **Date:** 2026-10-21
- **Scope (exclusive):** literal citing-file→source reference mapping for exactly these six frozen knowledge paths, against the frozen13 source rows (S038, S049–S060) per `plans/fixtures/r28/registry/population.json` (base b9b24796277020d1b9b01923b45313d6a565e664):
  1. `corpus/knowledge/agent-time-horizon-and-task-validity.md` (62 lines)
  2. `corpus/knowledge/attrib-prior-art-r21.md`
  3. `corpus/knowledge/attrib-r21.md` (667 lines, read in full across 1–300/301–500/504–667)
  4. `corpus/knowledge/attribution-interval-calibration.md` (189 lines, line 1 read raw)
  5. `corpus/knowledge/bailian-cli-telemetry.md`
  6. `corpus/knowledge/bench-arena-fresh-run.md`
- **Registry read:** actual registry table under `## Registry` of `corpus/SOURCES.md` (rows S001–S060; S038 row re-read raw at SOURCES.md:60).

## Method (observed commands)

No installs, no network, no production writes. Only `read` (including raw line/row reads) and PCRE2 `grep` scans:

- Pattern A (population's own `reference_pattern`): `(?<![A-Za-z0-9_])S[0-9]{3,}(?![A-Za-z0-9_])` over all six files — full per-line match census.
- Pattern B (frozen13-only projection): `(?<![A-Za-z0-9_])S(038|049|05[0-9]|060)(?![A-Za-z0-9_])` over all six files — exactly one match in the whole slice.
- Zero-match confirmation: Pattern A over files 2/3/5/6 returned "No matches found" (files 2, 3, 5, 6 contain no standalone S-ID of any kind).
- `read corpus/SOURCES.md:60:raw` → full S038 row, untruncated.

## Machine-readable map

```json
{
  "frozen13_ids": ["S038", "S049", "S050", "S051", "S052", "S053", "S054", "S055", "S056", "S057", "S058", "S059", "S060"],
  "reference_pattern": "(?<![A-Za-z0-9_])S[0-9]{3,}(?![A-Za-z0-9_])",
  "files": {
    "corpus/knowledge/agent-time-horizon-and-task-validity.md": {
      "frozen13_mentions": [],
      "non_frozen_standalone_mentions": ["S013", "S014", "S005", "S006"],
      "non_frozen_lines": [1, 3, 13, 14, 15, 16, 17, 18, 19, 29, 45, 51, 53, 59]
    },
    "corpus/knowledge/attrib-prior-art-r21.md": {
      "frozen13_mentions": [],
      "non_frozen_standalone_mentions": [],
      "note": "zero standalone S-ID tokens of any kind (arXiv IDs like 2407.15847 do not match the pattern)"
    },
    "corpus/knowledge/attrib-r21.md": {
      "frozen13_mentions": [],
      "non_frozen_standalone_mentions": [],
      "note": "zero standalone S-ID tokens of any kind across all 667 lines"
    },
    "corpus/knowledge/attribution-interval-calibration.md": {
      "frozen13_mentions": [
        {
          "id": "S038",
          "line": 144,
          "context": "Corrections (round 25 falsify wave) — historical/corrective mention, counts literally per declared contract",
          "quote": "S038 (Reiczigel et al. 2010, Introduction) warns the naive adjusted interval can cover 60% at nominal 95%."
        }
      ],
      "non_frozen_standalone_mentions": ["S037", "S030", "S027", "S028", "S029", "S011", "S033", "S034", "S036", "S015", "S035", "S041", "S040", "S042"],
      "note": "line 1 (source-basis, read raw) lists S037/S030/S027/S028/S029/S011/S033/S034/S036 — no frozen13 ID; sole frozen13 occurrence in the file (and in the whole six-file slice) is line 144"
    },
    "corpus/knowledge/bailian-cli-telemetry.md": {
      "frozen13_mentions": [],
      "non_frozen_standalone_mentions": []
    },
    "corpus/knowledge/bench-arena-fresh-run.md": {
      "frozen13_mentions": [],
      "non_frozen_standalone_mentions": []
    }
  },
  "links": [
    {
      "citing_file": "corpus/knowledge/attribution-interval-calibration.md",
      "source_id": "S038",
      "registry_row": "corpus/SOURCES.md:60",
      "source": "Reiczigel, Földi & Ózsvári 2010, Epidemiology and Infection 138(11):1674–1678 — https://doi.org/10.1017/S0950268810000385",
      "kind": "paper", "tier": "A",
      "status_registry": "queued",
      "status_required_for_cited_row": "mined",
      "used_by_registry": "—",
      "used_by_required": "corpus/knowledge/attribution-interval-calibration.md must be listed",
      "link_ok": false,
      "drift_facets": [
        "status=queued but contract requires mined for a cited row",
        "used-by='—' does not list the citing frozen path corpus/knowledge/attribution-interval-calibration.md"
      ],
      "matches_disclosed_S038_drift": true
    }
  ],
  "uncited_frozen_ids_in_this_slice": ["S049", "S050", "S051", "S052", "S053", "S054", "S055", "S056", "S057", "S058", "S059", "S060"],
  "registry_cells_frozen13": {
    "S038": {"status": "queued", "used_by": "—"},
    "S049": {"status": "mined", "used_by": "corpus/lessons/round-27.md, corpus/knowledge/extraction-policy-comparison.md"},
    "S050": {"status": "mined", "used_by": "corpus/lessons/round-27.md"},
    "S051": {"status": "mined", "used_by": "corpus/lessons/round-27.md, corpus/knowledge/extraction-policy-comparison.md"},
    "S052": {"status": "mined", "used_by": "corpus/lessons/round-27.md, corpus/knowledge/extraction-policy-comparison.md"},
    "S053": {"status": "mined", "used_by": "corpus/lessons/round-27.md, corpus/knowledge/extraction-policy-comparison.md"},
    "S054": {"status": "mined", "used_by": "corpus/lessons/round-27.md, corpus/knowledge/extraction-policy-comparison.md"},
    "S055": {"status": "mined", "used_by": "corpus/lessons/round-27.md, corpus/knowledge/extraction-policy-comparison.md"},
    "S056": {"status": "mined", "used_by": "corpus/lessons/round-27.md, corpus/knowledge/extraction-policy-comparison.md"},
    "S057": {"status": "mined", "used_by": "corpus/lessons/round-27.md, corpus/knowledge/extraction-policy-comparison.md"},
    "S058": {"status": "mined", "used_by": "corpus/lessons/round-27.md, corpus/knowledge/extraction-policy-comparison.md"},
    "S059": {"status": "mined", "used_by": "corpus/lessons/round-27.md, corpus/knowledge/extraction-policy-comparison.md"},
    "S060": {"status": "rejected", "used_by": "corpus/lessons/round-27.md"}
  }
}
```

## Comparison with registry cells — exact missing links

1. **`attribution-interval-calibration.md` → S038 (SOURCES.md:60):** the slice's only frozen13 citation link, and it fails both cited-row requirements:
   - status cell is `queued` (contract: cited rows must be `mined`);
   - used-by cell is `—` (contract: cited row must list every citing frozen path; `corpus/knowledge/attribution-interval-calibration.md` is absent).
2. **No other missing link exists in this slice.** S049–S060 are cited by none of the six files, so their cells (mined/rejected, used-by limited to `corpus/lessons/round-27.md` ± `extraction-policy-comparison.md`) impose no obligation from these files; uncited rejected (S060) and queued rows are explicitly non-errors under the declared contract. Additional lesson used-by paths are allowed and need not match the frozen knowledge set.

## Does the known S038 drift suffice?

**Yes, for this slice — completely.** The disclosed round-27 cited-but-queued S038 drift (claims: "Expected S038 drift is already disclosed"; mine item M65) is the *entire* set of baseline mismatches attributable to these six files: one link, two drift facets, both facets of that one row. A baseline `registry_check` run restricted to these paths would report exactly this one mismatch and nothing else. Corollary for F5: an allowed-cell S038 repair (status→`mined`, used-by append of the citing path) would make all six files fully consistent with zero other deltas *within this slice*; this evidence cannot speak for the other 29 frozen knowledge paths (RefGroup2/3 scope). The mention at line 144 is an additive Corrections-section historical/corrective reference and still counts under the literal contract — the repair must cover it; no immutable cell needs to change for it.

## Limitations

- Read-only seat: no `registry_check.py` execution (assignment: "No implementation read needed"); comparison is against the registry cells as read, not against the checker's output.
- Literal contract only (pattern-scoped); no semantic citation-support judgment made. Q13-style structural observations are not endorsements.
- Non-frozen mention census for file 4 is from displayed match lines plus full-file frozen-only projection; the frozen13 projection is exhaustive by pattern over all 189 lines regardless of display truncation.
- Files 1/4 cite non-frozen rows (S005/S006/S011/S013/S014/S015/S027–S030/S033–S037/S040–S042); their cell health is outside the frozen13 diagnostic and outside my seat's write scope.

## Verdict

**PASS (scoped to the six assigned files).** The reference map is complete and mechanically grounded: exactly one frozen13 citing link exists in the slice (`attribution-interval-calibration.md:144` → S038), and its mismatch is precisely the disclosed S038 drift — no additional missing links, no surprise rows. This is author-side advice, not outside non-author closure.

---
report: .ufo/waves/round-28/build/RefGroup1.md
