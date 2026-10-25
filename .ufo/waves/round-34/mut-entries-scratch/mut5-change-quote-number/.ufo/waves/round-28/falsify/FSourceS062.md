# FSourceS062 — Q10 reread: S062 WebArena `evaluators.py` row, Gate quote and candidate source use

Identity: **KengakuR28.FSourceS062** (scout), not candidate writer `KengakuR28`. Author-side, read-only;
no production file, registry cell, fixture, candidate or instrument was edited. No outside/non-author
closure is claimed. Paths relative to lane root `/home/vgpnk/Projects/shokunin/kengaku-shokunin`.

## Candidate and source pins

- Candidate: `.ufo/waves/round-28/drafts/webarena-task-spec-audit.md`, writer `KengakuR28`,
  12405 bytes, 146 lines, sha256 `77e19d5b2683dbf36b87c8ca0ae36e5b19f281673c1c16e46abfb6ab08ac20a8`
  (matches `.ufo/waves/round-28/candidate-freeze.json:candidate_sha256`).
- Proposed canonical path `corpus/knowledge/webarena-task-spec-audit.md` is absent:
  `test -e corpus/knowledge/webarena-task-spec-audit.md` exit 1, consistent with deferred admission.
- S062 URL in `corpus/SOURCES.md:84` and `corpus/lessons/round-28.md:41`:
  `https://raw.githubusercontent.com/web-arena-x/webarena/dce04686a56253aefba7b18a4fa0937cf1dc987b/evaluation_harness/evaluators.py`.
  Revision matches `plans/fixtures/r28/webarena/manifest.json:upstream_revision`
  `dce04686a56253aefba7b18a4fa0937cf1dc987b`.
- Fresh opening 2026-10-21: `curl` → HTTP 200, 13264 bytes, sha256
  `e23edb390c4e39b3fff97dfd456fb04f7a59a0fb1ea30a4f2fa42bcb77e00c22`, 374 lines. This equals the
  local snapshot `plans/fixtures/r28/webarena/evaluation_harness/evaluators.py` and the manifest
  digest; fetched copy retained at
  `.ufo/waves/round-28/scratch/KengakuR28.FSourceS062/ev.py` (my scratch only).

## Gate quote and anchor

Gate row (`corpus/lessons/round-28.md:41`): `` `score *= cur_score` — EvaluatorComb:351; source's
composition rule only.``

- Verbatim: line 351 of both the remote fetch and the local snapshot is exactly
  `            score *= cur_score` (12-space indent + text + `\n`); `od -c` confirms no other bytes.
- Occurrences: exactly one (`grep -n "score \*= cur_score"` → 351:1).
- Word count: 3 whitespace tokens (`score`, `*=`, `cur_score`), therefore ≤25; the row's blanket
  "Every listed quote is ≤25 words" is satisfied for S062 without relying on the seat's claim.
- Anchor: `class EvaluatorComb` at 336, `__call__` at 341, line 351 is inside that method; return at
  352. `corpus/SOURCES.md:84` anchor `EvaluatorComb:336–352` and `router:356–374` are both exact
  (`evaluator_router` starts 356, ends 374). The class-name:line form matches the S063 convention
  (`llm_fuzzy_match:169`).
- Access date 2026-10-21 is reproducible; the pinned URL, revision, digest and byte count are exact.
  This is a static code source, not a benchmark site; no browser, auth state or upstream code was run.

## Row tier / scope / teaches vs candidate use

`corpus/SOURCES.md:84` S062 is `code`, tier `A`. Tier A is correct under SOURCES contract v1
(source code is primary for the row's own static scope). Scope ("its own static routing and
predicate composition, not WebArena-Verified or actual browser outcomes") is correct and is respected
by the candidate: the draft labels all S062 claims static and explicitly excludes runtime/browser and
WebArena-Verified conclusions (draft `:16-22`).

Every S062 citation in the frozen candidate was checked line-by-line against the pinned file:

| draft use | cited range | verified source content |
|---|---|---|
| header `:1` | StringEvaluator:71–170, URLEvaluator:173–241, HTMLContentEvaluator:244–333, combination/router:336–374 | class boundaries 71/170, 173/241, 244/333; EvaluatorComb 336–352; router 356–374 — exact |
| String exact `:30` | 80–94; 134 | `clean_answer` 80–86 (strip, one quote pair, lower); `exact_match` 90–94; routed pre-clean `pred = self.clean_answer(...)` 134 — exact; double normalization claim true |
| String includes `:31` | 98–111, 142–149 | `must_include` 98–111 (`clean_ref in clean_pred`; token branch 103–109); routed call 142–149 with `tokenize=(len(value) == 1)` 148 — exact |
| String fuzzy `:32` | 150–169 | `case "fuzzy_match"` 150 through the reference loop 167–169; non-N/A calls `self.fuzzy_match` → helper — exact |
| N/A `:33`, `:46-48` | 152–163; 159 | `if value == "N/A"` 152; `score *= exact_match` 155; `if score != 1` 158; `score = 1.0 * self.ua_match(...)` 159–163 — exact assignment (not multiplication) |
| URL `:34` | 187–239 | `clean_url` rstrip 187–190; `parse_url` netloc+path 192–197; `parse_urls` 199–210; base containment 220–227; query product 228–236 — exact |
| URL alternatives `:39` | 199–235 | query values pooled in `queries[k].update(v)` 204–209, not paired per base path — exact |
| Page content `:35` | 258–333 | targets 258; score 260; navigate/sleep 271–273; locator branches 276–301; unescape 303; exact_match before must_include 305–327; per-target product 310/327 — exact |
| HTML errors `:42` | 271–301 | JS evaluate exception → `""` 292–294; `func:` helper `eval` 296–299 without catch — exact |
| Composite `:36` | 348–352, 361–374 | `score=1.0` 348, loop 349, `cur_score=evaluator(...)` 350, `score *= cur_score` 351, return 352; router `eval_types` 361 through `return EvaluatorComb(evaluators)` 374 — exact |

No candidate line range is off by one and no cited branch is misdescribed. The draft's `:159` N/A
reading matches the independent build review (`build/RevStringFuzzy.md:22` "score is *reset*, not
multiplied"), and the draft correctly bounds it to the pinned population (all 36 N/A tasks have
`fuzzy_match` as the sole key per that report).

## Old-knowledge append-only correction

None is supported, and none is claimed by the Gate row. A corpus-wide search
(`grep -rn "WebArena" corpus/ --include=*.md` excluding round-28/SOURCES) finds only
`corpus/knowledge/benchmark-selection.md:18` (recommends *WebArena-Verified*, a distinct population
S062's scope explicitly excludes) and the `corpus/README.md:318` instrument index row. No existing
knowledge entry makes a claim about this snapshot's evaluator composition, so an errata/append-only
correction would be unsupported. S062 is new ground, not a correction of old knowledge.

## Findings

- **F1 (Low, registry wording only) — S062 `teaches` is overbroad if read branch-uniform.**
  `corpus/SOURCES.md:84` teaches "named string, URL and page-content predicates compose
  multiplicatively". At `evaluators.py:155–163` the string `fuzzy_match:"N/A"` branch first multiplies
  `exact_match` and then, when `score != 1`, **assigns** `score = 1.0 * self.ua_match(...)`, discarding
  the accumulated factors; a prior zero can be resurrected. So not every named string predicate composes
  multiplicatively in that branch. The frozen candidate already states the precise form at `:46-48`
  ("assigns its judge score rather than multiplying into an earlier accumulated approach score") and
  `:112` ("N/A assignment override"), so this is not a candidate defect. If the row's `teaches` is read
  at the EvaluatorComb level (the three evaluator scores multiply), it is accurate; as written it mixes
  the within-class and comb levels. L1's call: qualify the cell or rely on the candidate's narrower
  statement. No metric, quote, line or verdict depends on the wording.
- **F2 (observation, not a defect) — the Gate exemplar quote is narrower than the opener's own quote.**
  `build/OpenScorer.md` proposed a two-span quote (`:351` + `:365–370`) and offered `:350–351` as the
  contiguous alternative. The Gate chose `:351` only, which by itself does not show that `cur_score` is
  the per-evaluator score; the candidate's `348–352` does. Narrowing a quote is allowed, and the row's
  anchor range 336–352 supplies the context, so this is a completeness note, not an error.
- **F3 (provenance, not a defect) — "independently opened byte-equal source" is accurate, but it is not
  a second-seat Q10 reread.** S062 was opened byte-equal by `build/OpenScorer.md` (HTTP 200, digest) and
  independently by `build/OpenTasks.md:9`; my fresh fetch reproduces the same digest. `OpenScorer` is
  also the seat that proposed the row, so "independently" means independent of the draft, not an
  independent Q10 confirmation. Admission is correctly still deferred by the Gate's `deferred` reason.
- **No finding:** URL, revision, access date, byte count, digest, quote verbatimness, word count, anchor
  line, SOURCES anchor ranges, candidate hash and candidate S062 line references all pass. S062 is not
  in the frozen C2 population (`plans/fixtures/r28/registry/population.json` lists S038 and S049–S060),
  so the lesson-only `used-by` does not affect C2 counters.

## Remaining unknowns

- Runtime scoring values (judge calls, `func:` helpers, browser state) were not observed and are not
  claimed by S062; this reread is static source evidence only.
- Whether L1 reads the `teaches` cell at the comb level or qualifies it is a resolution decision, not a
  source uncertainty.

Installs: none. No LSP server applies to a pinned Python source file; the line/quote findings above are
direct byte/line reads, not text-search inference.

**Canonical proposed path:** `corpus/knowledge/webarena-task-spec-audit.md` (not admitted; candidate
sha256 `77e19d5b2683dbf36b87c8ca0ae36e5b19f281673c1c16e46abfb6ab08ac20a8`).

VERDICT: PARTIAL (scoped) — the S062 Gate quote, anchor, URL/date/revision/digest and every candidate
S062 line reference pass exactly; the single actionable item is the registry `teaches` cell's
branch-uniform multiplicative wording (F1), which the candidate itself already qualifies. No number,
quote or candidate claim is falsified. This is not an admission or an outside closure.

## v2 reread — S069 supersession and current candidate (appended 2026-10-21; v1 above preserved)

Candidate v2 is the same path at 163 lines, sha256
`3eb2afe5ddff41f322b7131bbc658583e5a8ee8e2dc8c68b974039fdc02ff182`; canonical
`corpus/knowledge/webarena-task-spec-audit.md` remains absent (`test -e` exit 1). V1
`77e19d5b…` is historical per `corpus/lessons/round-28.md:157`. S062/S069 source bytes are unchanged:
sha256 `e23edb390c4e39b3fff97dfd456fb04f7a59a0fb1ea30a4f2fa42bcb77e00c22`, 13264 bytes, 374 lines.

**S069 row and Gate record.** `corpus/SOURCES.md:91` and the corrective Gate record
`corpus/lessons/round-28.md:209` quote `` `score = 1.0 * self.ua_match(` ``. Line 159 is exactly
`                            score = 1.0 * self.ua_match(`; the quote is a verbatim substring, the only
occurrence in the file, and 5 whitespace tokens (`score`, `=`, `1.0`, `*`, `self.ua_match(`), matching
the Gate's "5 words" and ≤25. Anchor `StringEvaluator152–163, assignment159` is exact (branch opens
152, assignment 159, closes 163); `EvaluatorComb348–352` is exact (score 1.0 at 348, product at 351,
return 352). Tier A is correct for pinned source code. Scope and teaches are accurate: routed evaluator
return values multiply in the router's declared `eval_types` order at `EvaluatorComb.__call__:348–352`;
the N/A branch at `StringEvaluator:158–163` assigns `1.0 * ua_match(...)` instead of preserving earlier approach factors
(the check is `if score != 1`, so a prior zero can be overwritten); runtime state is not claimed. The
older S062 row is left unchanged and S069 records the append-only qualification, matching the
S064/S054 supersession convention; `round-28.md:217` states S062's composite product does not imply
uniform within-string multiplication. V1 finding F1 is resolved by S069 without rewriting S062.

**Candidate v2 source use.** S062/S069 are cited at `:1` (header, "S069 qualifies composition"), `:26`,
and `:41` (composite row `S062/S069:348–352,361–374`); the N/A sentence at `:52` still cites
`S062:159` (same bytes; see observation). Rechecked every S062 range against v2: 80–94 and 134,
98–111 and 142–149, 150–169, 152–163, 187–239, 199–235, 258–333, 271–301, 348–352 and 361–374, and
header spans 71–170/173–241/244–333/336–374 — all exact. V2's `:36` now includes the third tokenize
condition (`word_tokenize` returns one token) and `:40` says "exact_match if present, otherwise
must_include" for the exclusive `if`/`elif` at 305/312; both are source-accurate and improve v1.

**AST locations vs hand-read annotations.** A CLI probe of the delivered instrument
(`python3 plans/benchmark_spec_audit.py --json`) returns `scorer_contract.dispatch` as a
name mapping (`string_match→StringEvaluator`, `url_match→URLEvaluator`,
`program_html→HTMLContentEvaluator`), `composition.source_lines` `[351]`,
`na_fallback.source_lines` `[159]`, and literal `failure_phases`/`operation` strings; the separate
`contract_anchors` block (AST `ast.walk`) carries class/function `line`/`end_line` for both pinned
files. Candidate `:122-124` says exactly this: dispatch and product/N/A-override statement locations
are derived from AST; operation/error-phase descriptions are hand-read, source-hash-bound annotations,
not AST-proven semantics or an executable scorer port. Confirmed accurate against the instrument
output; the only compression is that `dispatch` is a name mapping, not a line list, so
"statement locations" correctly attaches to product/override (and `contract_anchors`). No residual
"AST-derived … distinct error phases" claim remains (grep finds none).

**Observations, not defects.** (a) `:52` cites `S062:159` rather than `S062/S069:159`; the sentence is
exactly S069's teaching, so a tighter citation would name S069, but the claim is byte-exact and S069 is
already cited at `:1`/`:41`. (b) V2 `3eb2afe5…` is not yet frozen: `candidate-freeze.json` still pins
v1 `77e19d5b…`, `round-28.md:150` still names v1, and no v2 pin exists outside scratch. Admission must
re-freeze these exact v2 bytes (and the repaired instrument digests) before the Q10/admission-commit
check; this reread is valid only for `3eb2afe5…`.

**Final verdict: PASS (scoped, source/row/quote/candidate use).** S069's quote, anchor, tier, scope and
teaches are supported by the unchanged pinned bytes; v2's S062/S069 citations and AST/hand-read labels
are accurate; v1 F1 is resolved append-only. Condition: bind `3eb2afe5…`, not the stale v1 freeze, at
admission. No production edits; no installs. This is not an admission or an outside closure.
