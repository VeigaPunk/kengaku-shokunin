# FSourceS063 — S063 WebArena helper row, Gate quote/anchor, candidate source use

Seat: `KengakuR28.FSourceS063` (scout, leaf; author-side evidence, not outside/non-author closure).
Read-only over production; no registry cell, fixture, candidate, instrument or lesson was edited. Only
my scratch directory and this report were written. Paths are relative to the lane root
`/home/vgpnk/Projects/shokunin/kengaku-shokunin`. This is not an admission decision.

## Pins and identities

- Candidate: `.ufo/waves/round-28/drafts/webarena-task-spec-audit.md`, writer `KengakuR28`,
  12405 bytes / 146 lines, SHA256
  `77e19d5b2683dbf36b87c8ca0ae36e5b19f281673c1c16e46abfb6ab08ac20a8`. This equals
  `.ufo/waves/round-28/candidate-freeze.json:candidate_sha256`.
- Proposed canonical path `corpus/knowledge/webarena-task-spec-audit.md` is absent
  (`test -e` exit 1); the candidate is not admitted, consistent with the Gate.
- S063 URL in `corpus/lessons/round-28.md:42` and `corpus/SOURCES.md:85`:
  `https://raw.githubusercontent.com/web-arena-x/webarena/dce04686a56253aefba7b18a4fa0937cf1dc987b/evaluation_harness/helper_functions.py`.
  The revision equals `plans/fixtures/r28/webarena/manifest.json:upstream_revision`
  `dce04686a56253aefba7b18a4fa0937cf1dc987b`.
- Fresh opening 2026-10-21: `curl` to that exact URL returned HTTP 200, 7565 bytes,
  SHA256 `ec758da4f82e5659e95805ab23222cfd7c4a0f2a67f64a8f85bac9626997e275`. This equals the
  local snapshot `plans/fixtures/r28/webarena/evaluation_harness/helper_functions.py` and the
  manifest digest; `cmp` returned 0. My fetched copy is retained at
  `.ufo/waves/round-28/scratch/FSourceS063/helper_functions.upstream.py`.
- `build/OpenHelpers.md` independently fetched the same URL (its scratch copy has the same digest
  and also `cmp`-equals the snapshot), so the Gate's "independently opened byte-equal source" is
  supported for the opening, not merely asserted.

## Gate row: exact quote and anchor

Gate row `corpus/lessons/round-28.md:42`:

> `if "partially correct" in response or "incorrect" in response:` — llm_fuzzy_match:169; judge
> response parsing, not judge accuracy. build/OpenHelpers.md independently opened byte-equal source.

- The quote is a verbatim substring of line 169 of both the local snapshot and the fresh fetch,
  after the 4-space Python indent. There are no CR, smart-quote or trailing-space differences
  (`repr`/byte read of the line).
- Word count, counted by me rather than trusting the seat: 9 whitespace tokens. Even counting every
  punctuation/quotation token separately it is 14. Either way it is ≤25.
- Location `llm_fuzzy_match:169` is exact: `def llm_fuzzy_match` starts at 146, ends at 173
  (`ast.parse` on the pinned snapshot gives `lineno=146,end_lineno=173`), and line 169 is the first
  line of its response handling.
- `corpus/SOURCES.md:85` anchor `llm_fuzzy_match:146–173, llm_ua_match:176–208, dynamic
  helpers:23–143`: independently derived AST ranges are fuzzy 146–173, UA 176–208, and helper
  functions starting at 23 (`shopping_get_auth_token`) through 143 (`return role` in
  `gitlab_get_project_memeber_role`). All three ranges are exact.
- Access date 2026-10-21 is reproducible and matches the manifest opening date. The URL, revision,
  byte count and digest are exact.

## Row narrowness: tier / scope / teaches

- `kind=code`, `tier=A`: correct under SOURCES contract v1, which lists source code as primary for
  its own static scope.
- `scope` ("its own helper and LLM-judge call/response contract, not judge accuracy or endpoint
  availability") is narrow and respected by the source. The file does show the judge call settings
  and keyword parsing; it does not establish judge accuracy, endpoint availability, live site state
  or browser outcomes.
- `teaches` ("fuzzy and unachievable-reason branches call a named hosted judge and interpret
  keywords; live helper/API state is outside the static source") is accurate at the helper-file
  level: `llm_fuzzy_match` (146–173) and `llm_ua_match` (176–208) both call
  `generate_from_openai_chat_completion(model="gpt-4-1106-preview", temperature=0, ...)` and parse
  the lower-cased response by substring (`partially correct`/`incorrect` → 0.0; else assert
  `correct` → 1.0; `different` → 0.0; else assert `same` → 1.0). The dynamic site helpers
  (23–143) depend on live services; that state is outside the static file. No tier-A runtime claim
  is made.
- `status=mined` with `used-by=corpus/lessons/round-28.md` follows the round-27 precedent
  (`corpus/lessons/round-27.md:56`: new rows "enter mined with used-by solely this lesson"). The
  lesson exists and contains the S063 row. S063 is not in the frozen C2 population
  (`plans/fixtures/r28/registry/population.json` lists S038 and S049–S060), so this used-by does
  not affect C2 counters.
- **Old-knowledge append-only correction:** none is supported, and none is claimed. S063 is a new
  row, not a `supersedes S0NN` row. `grep -rn "S063" corpus/` finds only the lesson Gate row and
  the SOURCES registry/search-log lines; no `corpus/knowledge/*` path cites S063. The round's
  old-knowledge corrections are S064→S054, S066→S038 and the extraction-policy M66 errata, plus
  S065 as a scoped anchor extension of S053; none involves S063. The candidate is new ground (README Frontier extension), not an
  errata.

## Candidate source use, line by line

| candidate line | S063 use | verification |
|---|---|---|
| `:1` header | URL plus `fuzzy/UA:146–208` | URL exact; 146 is `def llm_fuzzy_match`, 208 is the last line of `llm_ua_match` — exact inclusive span |
| `:21` | "S062/S063 for their own code behavior, **not** actual browser state or judge correctness" | matches the row scope; no runtime/judge-accuracy claim |
| `:32` | String fuzzy: `S062:150–169 invokes S063:146–173 for non-N/A references` | evaluator `case "fuzzy_match"` 150, `else` loop 164–169 calls the `fuzzy_match` wrapper 115–116 → `llm_fuzzy_match`; exact |
| `:33` | Unachievable answer: `S062:152–163 accepts exact N/A first, otherwise calls S063:176–208 against string_note` | evaluator 152–163: exact N/A first, `if score != 1` calls `ua_match` with `string_note`; wrapper 120–121 → `llm_ua_match`; exact |
| `:51–52` | "two LLM helper branches call gpt-4-1106-preview and interpret response keywords (S063:161–173, 196–208); unexpected replies can reach assertions" | 161–168 / 196–203 are the two model calls with `gpt-4-1106-preview`; 169–173 / 204–208 parse keywords and assert; exact |

The draft's next sentence, "Exact N/A bypasses the reason judge", is an evaluator-routing fact
(`evaluators.py:152–158`), not a claim about S063; the table row cites S062 for it. No draft S063
citation is outside the row's scope, and no S063 number or line is off by one.

## Findings

- **Assigned chain:** no defect found. URL, revision, access date, byte count, digest, quote
  verbatimness, word count, anchor line, SOURCES ranges, tier/scope/teaches, status/used-by
  precedent, candidate hash and every candidate S063 line reference pass exactly.
- **O1 (out-of-lineage observation, not counted in this verdict).** `build/RevStringInclude.md:9`
  cites the `llm_ua_match` return contract at `lines 215–217`; the actual lines are 204–208
  (215–217 are inside `PseudoPage.__getattr__`). That build report is not cited by the Gate row,
  the SOURCES row or the frozen candidate (the candidate's UA citation is the correct 196–208),
  so it does not affect S063's row or candidate use. L1 may correct the build report for hygiene.
- **O2 (observation).** `build/OpenHelpers.md` says its broader 169–173 quote is "19 words"; my
  whitespace count of that text is 18. Both are ≤25; the Gate quote is a narrower 9 words. The
  Gate's own quote is exact and within limit. This is a count note, not a Gate defect.
- **O3 (observation).** The exact-N/A success path bypasses `llm_ua_match` in the evaluator, so the
  hosted judge is not called for every N/A task. The row's `teaches` is accurate when read at the
  helper-function level, and the candidate explicitly states the evaluator condition at `:33` and
  `:51–53`. If L1 wants the registry cell to be read branch-uniformly, it could add "when reached";
  the candidate already supplies the qualification. No metric or source claim depends on this.

## Limits

- Static source evidence only: no upstream import/execution, no browser, no benchmark site, no LLM
  judge call, no auth material. The only network request was the pinned `raw.githubusercontent.com`
  S063 URL above. I did **not** contact the S066 DOI/publisher, Wayback capture or any cached PDF;
  S066 is outside this seat's scope, and its access limitations remain as recorded in
  `build/OpenS038.md`.
- No `lsp` tool/device is exposed in this session's tool inventory; symbol ranges were
  independently derived with Python `ast.parse` on the pinned snapshot, and quote/line claims were
  checked by direct byte/line reads, not by text search alone.
- No builds, tests, linters, formatters or production checkers were run. No tools were installed
  or updated. No production file was edited.

**Canonical proposed path:** `corpus/knowledge/webarena-task-spec-audit.md` (not admitted).
**Candidate SHA256:** `77e19d5b2683dbf36b87c8ca0ae36e5b19f281673c1c16e46abfb6ab08ac20a8`.

VERDICT: PASS (assigned S063 row/Gate/draft chain) — the S063 Gate quote is verbatim, 9 words, at
line 169, the URL/date/revision/byte count/digest and all SOURCES anchor ranges are exact, the
candidate's S063 uses are all in-scope and line-exact, and no old-knowledge correction is claimed
or supported. O1 is an out-of-lineage build-report line slip that does not touch the assigned row,
Gate citation or candidate. This is not an admission or an outside closure.
