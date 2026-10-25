# ConnectScope — round 28 sibling overlap scan (author-side, read-only)

Writer/seat: `KengakuR28.ConnectScope-2` (connector, leaf, read-only). Date 2026-10-21.
Scope: sibling `PROVINCE.md` metadata only (no sibling SKILL/corpus reads, no edits), plus
the lane's own claims file, `corpus/QUALITY.md`, `corpus/README.md` §Frontier and the pinned
r28 WebArena fixture. This is author-side advice, not non-author closure. No source was
opened on the network; no new source row or knowledge admission is proposed by this seat.

## Axes

Declared axes (`plans/round-28-claims.md:7-8`): novelty legacy → canonical coverage/constructs
(lowest, 7; C1) and calibration (8; C2). Scores held; this seat finds no evidence that warrants
repricing either.

## Inputs read (bytes pinned)

| Path (relative to `/home/vgpnk/Projects/shokunin`) | sha256 | last PROVINCE commit |
|---|---|---|
| `chousa-shokunin/PROVINCE.md` | `cf7826a4…bbec` | `3282042b` 2026-10-14 |
| `tameshi-shokunin/PROVINCE.md` | `cd11b529…7a44` | `370f2dff` 2026-10-21 |
| `kotoba-shokunin/PROVINCE.md` | `c1fa9d97…e524` | `f2f9ee1d` 2026-10-19 |
| `kake-shokunin/PROVINCE.md` | `f71df98e…9917` | `9f62cda0` 2026-10-21 |
| `kaidoku-shokunin/PROVINCE.md` | `dbf757fe…ed97` | `2ee3d9f5` 2026-10-21 |
| `souji-shokunin/PROVINCE.md` | `3a2364d7…bda8` | `4b826a52` 2026-10-21 |
| `kengaku-shokunin/PROVINCE.md` | `eed536c4…37b1` | (own lane) |

The fixture's `evaluators.py` (`e23edb39…0c22`), `helper_functions.py` (`ec758da4…e275`) and
`test.raw.json` (`7b50386f…7652`) byte hashes equal `plans/fixtures/r28/webarena/manifest.json`.

## Observed commands

- `sha256sum` and `git -C <lane> log -1 -- PROVINCE.md` over the seven PROVINCE files (above).
- Keyword census, one `rg -i -c 'benchmark|webarena|task.spec|judge|grader|scoring'` per
  `*-shokunin/PROVINCE.md` (21 lanes). Every sibling returned 0 except `kasegi-shokunin/PROVINCE.md:47`
  ("kengaku — LLM evaluation and benchmarks"), which routes the ground **to** kengaku. Kengaku: 10.
- `rg -i 'link.?(rot|drift|check)|dead link|broken link|citation|cross-ref|used.by|SOURCES\.md|registry'`
  over every PROVINCE (results used below).
- A stdlib `json.load` count over `test.raw.json` (data read only; no upstream import/exec):
  812 tasks; reference-answer operators exact_match 45, must_include 176, fuzzy_match 118
  (36 of them `"N/A"`), program_html tasks 411. Selected 16: exact 1, must_include 2,
  fuzzy 2 (task 173 list, task 791 `"N/A"`), program_html 9.

## Ownership boundary per sibling

| Sibling | Its own claim (exact line) | Possible overlap with r28 | In-lane interpretation |
|---|---|---|---|
| **chousa** | Owns "source hierarchy … citation chaining and hop resolution; claim-vs-source verification" (`chousa-shokunin/PROVINCE.md:5-7`); refuses "model-quality or evaluation claims (→ kengaku)" (`:10-11`) | C2 source-row/citation consistency; the S061–S063 openings | C1 is decisively kengaku (chousa routes evaluation here; kengaku `corpus/README.md:258` already names "Agentic benchmark task-spec audits" as own frontier). C2 is literal `S[0-9]{3,}` token ↔ `used-by` completeness, explicitly "NOT semantic citation support" (`plans/round-28-claims.md:8`) — that exclusion is exactly chousa's claim-vs-source ground. Openings apply chousa's method without restating it (`corpus/QUALITY.md:7-8`). |
| **tameshi** | Owns "verification-fixture craft … hermetic suites, mutation testing, fail-closed arms" (`tameshi-shokunin/PROVINCE.md:3-5`); "every lane's gate remains its own"; general pattern needs "evidence in TWO independent lanes" (`:14-16`); never edits a sibling gate (`:16-17`) | `benchmark_spec_audit.py` / `registry_check.py` selftests, exit 0/1/2 discipline, mutation probes on scratch copies (`plans/round-28-claims.md:16,20,26`) | Both instruments are kengaku gates; tameshi owns only reusable craft. Kengaku must not claim a general verification method; a pattern may be *reported* to tameshi, not absorbed. |
| **kotoba** | "prompt & skill craft — scopes SKILL.md/AGENTS.md quality, trigger fidelity" (`kotoba-shokunin/PROVINCE.md:3`); lists "kengaku — LLM/model evaluation" as adjacent (`:29`) | The two LLM-judge prompts the scorer sends (`helper_functions.py:150-155` fuzzy, `:180-190` ua); task `intent` strings | Judge validity and calibration (model pin `gpt-4-1106-preview` `:162,:197`, substring verdict rules `:169-173`, `:204-208`, N/A fallback `evaluators.py:150-163`) are evaluator validity → Main/kengaku. Kengaku PROVINCE:137 already keeps measured prompt effects and routes only reusable craft implications out. Prompt wording is data, not a kotoba surface (kotoba's Core is SKILL/AGENTS/dispatch-prompt craft, `:12-14`). |
| **kake** | "audits, drift checks and source-fix guidance for the lane's web properties" (`kake-shokunin/PROVINCE.md:12-13`); browser driving is tabi's (`:30-31`) | C1 `url_match` notes; site set (shopping, shopping_admin, gitlab, reddit, map, wikipedia) | WebArena sites are benchmark environments, not kake's publisher properties. C1 URL notes are static scorer-contract parsing (`evaluators.py:187-196`, `urlparse`/`parse_qs`), never live drift. Any live site/browser operation would be tabi-adjacent and is forbidden by the assignment. |
| **kaidoku** | RE of "shipped artifacts with REA" (`kaidoku-shokunin/PROVINCE.md:3-6`); "Source-available reconstruction of ordinary repositories — REA's own anti-trigger `(unowned)`" (`:106-107`) | C1 parses upstream Python via AST without executing (`plans/round-28-claims.md:16`) | Pinned WebArena source is an ordinary source-available repo, so this is explicitly *not* kaidoku ground; C1's AST read is a scorer-contract trace, not reverse engineering. No REA use (assignment forbids it). |
| **souji** | Removal of stale artifacts, incl. "stale generated output with no live references" (`souji-shokunin/PROVINCE.md:10-14`); applies chousa's method in its own SOURCES (`:82-83`) | C2 "reference drift" | **Contradiction stated:** souji's PROVINCE contains no link-drift claim (`link.?(drift|rot|check)|dead link|broken link` → 0 hits). Its only reference-liveness ground serves removal eligibility; C2 removes nothing and edits only allowed registry cells. No overlap. |

## Decisive possible overlap (found outside the named six)

The closest prior art to C2 is not souji but two sibling **own-registry gates**:

- `kagi-shokunin/PROVINCE.md:55` — `corpus/sources-census.sh`: "the SOURCES-CONTRACT-v1 census over `corpus/SOURCES.md` plus the citation handshake with `corpus/knowledge/` entries that carry `source:`"; and `:83` "checks citations, not vendor truth".
- `kumitate-shokunin/PROVINCE.md:15` — "its learning registry `corpus/SOURCES.md` (checked by `scripts/sources-check.mjs`)"; tameshi already mutation-tested that gate (`tameshi-shokunin/PROVINCE.md:74-83`).

No ownership conflict exists, because each lane gates its own registry (`tameshi-shokunin/PROVINCE.md:14-15`). But it constrains how C2 is priced: its baseline "absent dedicated diagnostic (0 frozen source rows checked)" (`plans/round-28-claims.md:8`) is true **in-lane only**. Registry-vs-knowledge citation checking already exists in the fleet. C2 must stay a calibration claim, with no "new method" or "fleet-first" wording. This agrees with F6 (`:41`) and does not affect the held score8.

For C1, the census finds no sibling claiming benchmark task-spec or scoring ground (0 hits in 20 sibling PROVINCE files; kasegi:47 and chousa:10-11 both route it to kengaku). So "new ground in this corpus" (`plans/round-28-claims.md:7`) is supported at PROVINCE level. Score7 stays held, since PROVINCE silence is not a prior-art check.

## Proposed move (one, bounded)

Add one **"Adjacent routing (evidence sent, not absorbed)"** paragraph to the round-28 lesson draft. It should follow the existing PROVINCE report-out form (`kengaku-shokunin/PROVINCE.md:36-41,165-171`) and carry three routes:

1. **kotoba:** the two judge-prompt texts (`helper_functions.py:150-155,180-190`) are prompt-craft data only. Kengaku keeps judge validity: the verdict substring rules, the model pin and the N/A fallback. The selected-sample exposure is 2/16 tasks (173, 791), and 118/812 tasks use `fuzzy_match`.
2. **tameshi:** the C2 literal-token contract with quote/code-fence controls and frozen-population exclusion (`plans/round-28-claims.md:26-28`) is a *candidate* reusable pattern. Kagi's `sources-census.sh` and kumitate's `sources-check.mjs` are the other lanes' independent gates, so tameshi's two-lane bar (`:15-16`) may be reachable. That is tameshi's judgment, not kengaku's.
3. **chousa / kagi / kumitate (pricing note):** C2 checks literal reference completeness. Claim-vs-source verification stays chousa's. Registry-citation gating already exists in kagi and kumitate, so C2 makes no novelty claim.

Affected axes: calibration improves, because the scope wording now matches what sibling evidence supports and blocks a latent fleet-first or method overclaim on C2. Novelty/coverage is unharmed: C1's in-corpus new-ground claim is confirmed, not narrowed. C1/C2 separability is preserved, because the paragraph is prose in the lesson and is in neither C1's counted population nor C2's frozen 35 paths (`plans/round-28-claims.md:10`). It touches no checker, fixture or production file.

## Risks / second-order effects

- **Contract:** the lesson lives under round-28 drafts, which C2 excludes (`:8,:28`). If it were ever placed in a frozen baseline-35 path, its `S0xx` mentions would enter C2's literal census. The paragraph must cite sibling paths, not S-IDs, or stay out of the 35.
- **Runtime/verification:** none. No command, fixture or gate changes, and two-way revert measurements are unaffected.
- **Substrate:** sibling PROVINCE files drift; tameshi, kake, kaidoku and souji were all edited 2026-10-21. The line citations above are pinned to the hashes in the table and may go stale.
- **Calibration risk:** route (2) must not read as "tameshi agrees". It is a report-out, not endorsement (cf. Q13 structural evidence ≠ endorsement).

## Verification Main can run (read-only)

- `sha256sum` on the six sibling PROVINCE files, checked against the table above.
- `for f in *-shokunin/PROVINCE.md; do rg -i -c 'benchmark|webarena|task.spec|judge|grader|scoring' "$f"; done` from the fleet root. Expected: only kengaku (10) and kasegi (1) are non-zero.
- `rg -n 'sources-census|sources-check' kagi-shokunin/PROVINCE.md kumitate-shokunin/PROVINCE.md` → `:55` / `:15`.
- `rg -n -i 'link.?(drift|rot|check)|dead link|broken link' souji-shokunin/PROVINCE.md` → no output.

## Limitations

- PROVINCE metadata only. Sibling SKILL/corpus claims (for example chousa's `SKILL.md` method detail) were not read, and silence in a PROVINCE file is not proof that a lane has no knowledge entries in the area.
- The keyword census is lexical and can miss synonyms.
- No prior-art or literature check was done, so this report cannot reprice novelty.
- The judge-prompt and scorer lines are cited as structure, not as evidence of actual task invalidity.
- Tools installed/updated: none.

## Verdict

**PASS (scoped):** for the question "does r28 C1/C2 ground collide with chousa, tameshi, kotoba, kake, kaidoku or souji ownership at PROVINCE level?" there is no ownership collision, and the in-lane interpretations above hold. The souji "link drift" framing does not match souji's PROVINCE. The decisive C2 overlap is kagi's and kumitate's own registry gates, which cap C2's pricing but not its ownership. This is not a round PASS and makes no C1/C2 correctness judgment.
