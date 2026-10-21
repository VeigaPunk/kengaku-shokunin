# RefGroup5 — frozen13 literal reference map for six knowledge paths

- **Writer/seat:** KengakuR28.RefGroup5-2 (revenger, author-side, read-only seat; leaf member, no subagents)
- **Observed:** 2026-10-21, lane working tree HEAD `f0ba09be0f3066daba2134b943d973ad1588f34a` (round-28 preregistration atop baseline `b9b24796277020d1b9b01923b45313d6a565e664`)
- **Machine-readable map:** `.ufo/waves/round-28/scratch/KengakuR28.RefGroup5-2/frozen-ref-map.json`
- **Observed commands:** `read`/`grep` tools on lane files; one `python3` (stdlib `re`/`json`) census applying population.json's `reference_pattern` (`(?<![A-Za-z0-9_])S[0-9]{3,}(?![A-Za-z0-9_])`) to the 35 frozen knowledge paths plus a parse of the 11-column Registry table in `corpus/SOURCES.md`; one read-only `git rev-parse HEAD` for provenance. No builds/tests/linters; no installs (tooling directive: nothing installed, nothing to record); no external source openings (all evidence lane-internal; no URL/access-date obligations arise). No file outside my report and scratch was written.

## Scope and method

- Frozen13 IDs (population.json): S038, S049, S050, S051, S052, S053, S054, S055, S056, S057, S058, S059, S060. Declared contract is literal: every standalone mention counts, including historical, corrective and supersession mentions; quote/code-fence position does not exempt a mention.
- Assigned files (exact): `corpus/knowledge/godspeed-eval-findings.md`, `corpus/knowledge/grader-perturbation-audit.md`, `corpus/knowledge/kimi-model-routing-round18.md`, `corpus/knowledge/ledger-route-telemetry.md`, `corpus/knowledge/llm-judge-calibration.md`, `corpus/knowledge/local-bench-arena.md`.

## Machine-readable map (scoped)

```json
{
  "scoped_frozen_mentions": {
    "corpus/knowledge/godspeed-eval-findings.md": {},
    "corpus/knowledge/grader-perturbation-audit.md": {},
    "corpus/knowledge/kimi-model-routing-round18.md": {},
    "corpus/knowledge/ledger-route-telemetry.md": {},
    "corpus/knowledge/llm-judge-calibration.md": {},
    "corpus/knowledge/local-bench-arena.md": {}
  },
  "missing_links_in_scope": [],
  "scoped_out_of_contract_mentions": {
    "corpus/knowledge/grader-perturbation-audit.md": ["S043", "S044", "S045", "S046", "S048"],
    "corpus/knowledge/llm-judge-calibration.md": ["S009", "S010", "S011", "S012"]
  }
}
```

Zero standalone frozen13 mentions exist in any of my six files: no citing-file→source link is formed from these files, so no used-by or status obligation attaches to them and the in-scope missing-link set is empty. Out-of-contract hygiene observation (frozen13 contract covers exactly S038 + S049–S060, so these are not checked by the diagnostic): the non-frozen mentions that do occur are covered by their rows' used-by cells — S044 (`corpus/SOURCES.md` row S044), S045, S046, S048 each list `corpus/knowledge/grader-perturbation-audit.md`; S009–S012 each list `corpus/knowledge/llm-judge-calibration.md`; S043 (superseded by S048) lists only `corpus/lessons/round-26.md`, consistent with its superseded status.

## Registry comparison and exact missing links (frozen population, for the sufficiency question)

Census of all 35 frozen paths (beyond-scope check run solely to answer "does known S038 drift suffice"; the other 29 files' full mapping belongs to sibling RefGroups):

1. **S038 (known round-27 drift, confirmed exact):** `corpus/knowledge/attribution-interval-calibration.md:144` — "identified beyond the GT counts the receipts already print. S038 (Reiczigel et al. 2010, Introduction) warns the" — versus row S038 (`corpus/SOURCES.md:60`): `status=queued`, `used-by=—`. Cited-but-queued with an empty used-by cell: both failure modes named by C2.
2. **S050 (not covered by the disclosed drift):** `corpus/knowledge/extraction-policy-comparison.md:18` — "inspect_ai `pattern()` (S058, correcting S050) takes a first regex hit; on no hit it reports" — a standalone literal S050 mention (corrective/supersession class, which the contract explicitly includes). Row S050 (`corpus/SOURCES.md:72`): `status=mined`, `used-by=corpus/lessons/round-27.md` — the used-by cell does not list the citing frozen path. This is a missing used-by link independent of S038.

All other frozen IDs: S049, S051–S059 are cited by `extraction-policy-comparison.md` (lines 1, 16–24, 49–53) and each row is `mined` with used-by listing that file; S060 (`rejected`) is cited by no frozen knowledge path, only by the non-frozen lessons file, so its status is not a C2 violation.

## S038-sufficiency verdict

**No — S038 allowed-cell repair alone does not suffice for the 13 frozen rows on the observed tree.** The literal census shows a second missing link (S050 ← `extraction-policy-comparison.md:18`). Closing S038 (reopen source, flip mutable cells to `mined` and add the citing path to used-by, immutable cells untouched) still leaves the S050 used-by gap, so `registry_check.py` would keep reporting ≥1 mismatch. This disconfirms forecast F5 (p=.55) as literal evidence, and confirms F4's ≥1-mismatch expectation; it does not by itself change the C2 score, which anticipated S038 drift but not S050's.

## Limitations

- Literal-pattern matching per the declared contract only; no semantic citation-support judgment (C2 explicitly excludes it).
- Tree observed once at HEAD `f0ba09be`; concurrent wave seats may mutate `corpus/SOURCES.md` or knowledge files after my reads. Row/line citations are exact as of my reads (SOURCES.md lines 60 and 72; the two knowledge lines quoted above).
- The beyond-scope census covers all 35 paths for frozen-ID mentions, but per-file mapping detail for the other 29 files is left to their owning seats; my sufficiency conclusion rests only on the two cited mismatches and the complete absence of other frozen-ID citations in the 35 paths.
- No external source was opened; no claim here endorses any source (Q13: structural/literal evidence is not endorsement).

## Final scoped verdict

**PASS** for my assigned scope: the six assigned knowledge files contain zero standalone frozen13 references, produce no missing links, and require no repair. Sufficiency sub-verdict: **FAIL** — known S038 drift does not suffice; one additional literal missing link (S050 ← `corpus/knowledge/extraction-policy-comparison.md:18`) exists in the frozen population on the observed tree. This is author-side advice, not outside non-author closure.
