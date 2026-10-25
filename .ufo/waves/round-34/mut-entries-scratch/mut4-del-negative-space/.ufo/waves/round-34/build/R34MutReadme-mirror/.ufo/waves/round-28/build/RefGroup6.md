# RefGroup6 — frozen13 literal reference map for the five assigned knowledge paths

- **Writer/seat:** KengakuR28.RefGroup6-2 (read-only seat; author-side advice, not outside closure)
- **Round/role:** round28, author-side wave, RefGroup6 revenger slice — reference mapping for exactly:
  `corpus/knowledge/local-model-index.md`, `corpus/knowledge/open-model-catalogs.md`,
  `corpus/knowledge/paired-eval-uncertainty-reporting.md`, `corpus/knowledge/probe-battery-r19.md`,
  `corpus/knowledge/telemetry-run-design.md`
- **Audited tree:** working tree at `f0ba09be0f3066daba2134b943d973ad1588f34a` (prereg "round-28: freeze benchmark and registry claim populations"; round baseline declared `b9b24796277020d1b9b01923b45313d6a565e664`). Read-only `git rev-parse HEAD` was the only git call.
- **Machine-readable map:** `.ufo/waves/round-28/scratch/KengakuR28.RefGroup6-2/refmap.json` (this report's §Map is a copy).
- **Observed commands:** read/grep only (patterns logged in scratch JSON); no installs, no builds, no checker runs, no mutations, no external network.

## Contract applied

Frozen13 IDs = `S038`, `S049`–`S060` (`plans/fixtures/r28/registry/population.json:4-16`). Literal standalone pattern `(?<![A-Za-z0-9_])S[0-9]{3,}(?![A-Za-z0-9_])` counts every mention in the frozen paths — quotes, code fences, historical and supersession mentions included; no semantic Markdown interpretation.

## Map (frozen13 mentions per scope file)

| scope file | standalone frozen13 mentions | any `S[0-9]{3,}` tokens at all |
|---|---|---|
| corpus/knowledge/local-model-index.md | **0** | 0 (cites absent local `~/.bailian` paths only) |
| corpus/knowledge/open-model-catalogs.md | **0** | 0 (cites public HF/OpenRouter API endpoints + host inventory) |
| corpus/knowledge/paired-eval-uncertainty-reporting.md | **0** | S015–S019 only — all OUTSIDE frozen13 (lines 1, 3, 13–20, 25, 30, 48, 49) |
| corpus/knowledge/probe-battery-r19.md | **0** | 0 (S1–S8/D1–D5/G1–G8/H1–H10/P1–P9 are probe/seat component IDs; <3 digits, never match the literal pattern) |
| corpus/knowledge/telemetry-run-design.md | **0** | 0 (cites absent local llm-wiki root only) |

Non-frozen context (outside the frozen population, recorded for calibration only): the five S-tokens in the paired-eval file (e.g. line 1 "source: S015 — https://arxiv.org/html/2411.00640") correspond to registry rows SOURCES.md:37–41, all `mined`, all used-by = `corpus/knowledge/paired-eval-uncertainty-reporting.md` — source-side consistent, no drift.

## Registry cells compared (corpus/SOURCES.md rows)

| ID | line | status | used-by cell | names a scope file? |
|---|---|---|---|---|
| S038 | 60 | `queued` | `—` | no |
| S049 | 71 | `mined` | lessons/round-27.md, knowledge/extraction-policy-comparison.md | no |
| S050 | 72 | `mined` | lessons/round-27.md | no |
| S051 | 73 | `mined` | lessons/round-27.md, extraction-policy-comparison.md | no |
| S052 | 74 | `mined` | lessons/round-27.md, extraction-policy-comparison.md | no |
| S053 | 75 | `mined` | lessons/round-27.md, extraction-policy-comparison.md | no |
| S054 | 76 | `mined` | lessons/round-27.md, extraction-policy-comparison.md | no |
| S055 | 77 | `mined` | lessons/round-27.md, extraction-policy-comparison.md | no |
| S056 | 78 | `mined` | lessons/round-27.md, extraction-policy-comparison.md | no |
| S057 | 79 | `mined` | lessons/round-27.md, extraction-policy-comparison.md | no |
| S058 | 80 | `mined` | lessons/round-27.md, extraction-policy-comparison.md | no |
| S059 | 81 | `mined` | lessons/round-27.md, extraction-policy-comparison.md | no |
| S060 | 82 | `rejected` | lessons/round-27.md | no |

Note on S060: status `rejected` while cited in `corpus/lessons/round-27.md` is NOT a contract violation — round-27.md is a lesson path, not one of the 35 frozen knowledge paths, and the frozen contract allows additional lesson used-by paths and does not treat uncited rejected/queued rows as errors.

## Missing links / extra links

- **Missing used-by links attributable to my 5 files: none.** Zero frozen13 standalone mentions exist in the five files, so zero used-by entries are owed by their rows.
- **Extra/incorrect used-by links touching my 5 files: none.** No frozen13 used-by cell names any of the five paths.
- Empty-citing-file ↔ empty-used-by relationship is fully consistent on this surface.

## S038 drift sufficiency

The disclosed S038 drift does not involve any of my 5 files. Its actual location is `corpus/knowledge/attribution-interval-calibration.md:144` — a frozen path outside this slice — which standalone-cites S038: "S038 (Reiczigel et al. 2010, Introduction) warns the naive adjusted interval can cover 60% at nominal 95%." (18 words), while SOURCES.md:60 holds S038 at status `queued` with used-by `—` (the `—` cell was written pre-citation: SOURCES.md:102 "included as S038 (queued, not cited by any entry this round)"). That is a two-part literal violation (cited-by-frozen-path row not `mined`; citing frozen path absent from used-by) — exactly the drift round 27 disclosed (`corpus/lessons/round-27.md:18`: "S038's cited-but-queued drift was independently found by RevengeMistakeMine").

**Sufficiency verdict for my scope: sufficient, vacuously.** My 5-file surface contains zero frozen13 citations and is named in zero frozen13 used-by cells; there is no divergence on my surface for the S038 drift (or anything else) to explain, and my surface contributes none of the ≥1 expected baseline C2 mismatches (F4). I make no population-wide sufficiency claim: the other 30 frozen knowledge paths are sibling slices I did not scan, and only a full-population scan can confirm S038-drift-explains-everything (forecast F5 p=.55 already marks that as uncertain).

## Limitations

- Literal-reference reconstruction only; no semantic citation-support claim (Q13-style structural finding, not endorsement).
- Scope limited to the 5 named files' frozen13 mapping; extraction-policy-comparison.md / round-27.md used-by correctness belongs to sibling RefGroups.
- `registry_check.py` was not executed; registry cells were read directly from SOURCES.md at the audited tree. L1 owns the delivered-checker counts.
- No external source openings (none required: all mapped evidence is in-repo); access-date/quote discipline applied to in-repo located quotes above.

## Final scoped verdict

**PASS** for the assigned surface: the five knowledge paths contain **0 standalone frozen13 mentions**, their rows owe **0 missing used-by entries**, and carry **0 extra used-by links**; the only frozen-population drift observable from in-repo evidence touching this map is the pre-disclosed S038 drift, which lives entirely outside this slice and is not contradicted by anything on it.

---
trailer: .ufo/waves/round-28/build/RefGroup6.md
