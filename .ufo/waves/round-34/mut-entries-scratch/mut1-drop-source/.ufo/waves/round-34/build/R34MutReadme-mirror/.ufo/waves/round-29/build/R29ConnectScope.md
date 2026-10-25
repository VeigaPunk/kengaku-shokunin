# R29ConnectScope — sibling-province overlap scan (round 29, C1)

- **Seat:** `KengakuR28.R29ConnectScope-2` (connector, round-29 build wave).
- **Actual writer:** `KengakuR28.R29ConnectScope-2`; no delegation, no subagents.
- **Date:** 2026-10-21.
- **Read-only attestation:** no production edits, no sibling writes, no commits, no installs,
  no host env/credential reads, no endpoint/site requests. The only file written is this report.
- **Scope:** PROVINCE metadata of chousa, tameshi, kotoba, kake, kumitate, kama, plus kengaku's own
  PROVINCE for the host boundary. Sibling `corpus/knowledge`, tools, plans and gates were **not** read
  (metadata-only mandate). This is a scope scan, not a round admission or source verification.

## 1. Inputs and authentication

Read once, retained digests (all commands run from the lane root
`/home/vgpnk/Projects/shokunin/kengaku-shokunin` for fixtures, and `/home/vgpnk/Projects/shokunin`
for sibling PROVINCE files):

| File | Lines | sha256 |
|---|---:|---|
| `chousa-shokunin/PROVINCE.md` | 17 | `cf7826a43aaab7c00708ab54bb46577217e7a67ab44a43a33e17ee2a58c1bbec` |
| `tameshi-shokunin/PROVINCE.md` | 95 | `cd11b529784018725ec6bed757b9095f885fc127f0ba7c4021eca29f42b77a44` |
| `kotoba-shokunin/PROVINCE.md` | 32 | `c1fa9d97e4fe4798ea873cf2e80acac5f14f8c84b30036c927e1ae038b5fe524` |
| `kake-shokunin/PROVINCE.md` | 78 | `f71df98e6ae9e86f96ec0fa1343afd013daf16656bca70fd4c4790fe73119917` |
| `kumitate-shokunin/PROVINCE.md` | 28 | `fcd69667a1027d5edd07a8ff0390a716a467aff92719071e33cb6157673b665f` |
| `kama-shokunin/PROVINCE.md` | 107 | `b5fc015164cf3b31f2bba027d2ee5b8e5d301343045f43355a02be5d5d9712fd` |
| `kengaku-shokunin/PROVINCE.md` | 202 | `48ca6694b154277dd20b903f849e2d7c12272c88612e047676846eec8fda5df2` |

Pinned inputs re-verified against `plans/round-29-claims.md` and `plans/fixtures/r29/manifest.json`:
`test.raw.json` `7b50386fd69163dbc05d615d834df4c6ed2c35596e97a1b10d17451c02537652` (812 items,
812 distinct `task_id`), `generate_test_data.py`
`45ddba7be49096a18919b4122a8945ff74c292ba17e36892b16e176a8bd921cd` (838 bytes),
`profiles.json` `90fdc34d2f33e3100a2223fdaf5fc5f1016993b8e6723710cc4661e0da94e018`,
`manifest.json` `f6390b924c69f0cc8c47b2320b092060bb344b6a5e81c0075d3eb5aab817bf87`.
No tool install or update was needed; stdlib Python and coreutils only.

Term census across the six sibling PROVINCE files (two runs, exact results):

```
for f in chousa-shokunin/PROVINCE.md tameshi-shokunin/PROVINCE.md kotoba-shokunin/PROVINCE.md \
         kake-shokunin/PROVINCE.md kumitate-shokunin/PROVINCE.md kama-shokunin/PROVINCE.md; do
  grep -cE 'webarena|WebArena|generate_test_data|config_projection|env_config|config_files|test\.raw\.json' "$f"
done
→ 0, 0, 0, 0, 0, 0

for f in chousa-shokunin/PROVINCE.md tameshi-shokunin/PROVINCE.md kotoba-shokunin/PROVINCE.md kake-shokunin/PROVINCE.md kumitate-shokunin/PROVINCE.md kama-shokunin/PROVINCE.md; do
  grep -icE 'bench' "$f"
done
→ 0, 0, 0, 0, 0, 0
```

This is negative metadata evidence only (see §5). `tameshi-shokukin/` contains no `PROVINCE.md`
(only `.ufo/waves/round-18` and a nested `tameshi-shokunin/.ufo`), so it is not counted as a province.

## 2. Per-province boundary

Quotes are exact, line-cited, and word counts below were computed programmatically
(`len(q.split())`), all ≤25.

| Province | Owned surface (PROVINCE lines) | Relation to C1 | Contested fit / disposition |
|---|---|---|---|
| **chousa** | research method: question framing, source hierarchy, citation chaining, claim-vs-source verification, external-target approval (`:5-8`); explicitly refuses model-quality/evaluation claims to kengaku (`:10-11`) | C1 *applies* an already fleet-frozen source/quote discipline for the frontier row; it performs no external research and makes no method claim | No ownership contest. Method adjacency only: S070+ row work is applied craft, not new research method. Disposition: do not price research-method novelty from C1. |
| **tameshi** | verification-fixture craft, mutation testing, fail-closed arms; "every lane's gate remains its own" (`:14-15`); finite environment-differential method F5 (`:87-92`) | C1's `--selftest`, wrong-witness control, exit-code discipline and independent oracle borrow fleet verification *form*; the gate stays kengaku's | Two adjacencies. (a) Word "profile": tameshi's seven profiles vary host environment and run outputs; C1's three profiles are fixed substitution dictionaries with no host-env read and no run variation — C1 cannot be second-lane evidence for F5. (b) Gate ownership: `plans/config_projection.py --selftest` is kengaku's own gate; tameshi never edits it. No method claim. |
| **kotoba** | prompt/skill craft, SKILL.md/AGENTS.md wording and trigger fidelity (`:3`, `:12-13`); routes evaluation to kengaku (`:29`) | No instrument overlap. Only textual adjacency at non-URL-typed leaves | Risk: `eval.program_html[].required_contents.must_include[]` and `eval.reference_answer_raw_annotation` are task text; describing changes there as prompt/task-instruction effects would cross into kotoba's craft. Measured values are URL paths/fragments (§3), so no prompt-craft claim is available. Disposition: report changed path/value only; no behavioral claim. |
| **kake** | named web properties and publishing: ds4cc.com, kimi.page/pro mirrors, Pages deploys (`:3`, `:13`); kake owns remote web properties vs kama endpoints (`:37`) | None. Profiles are `.invalid`; no fetch, render, crawl or deploy | Risk: "remote web properties" could be read onto WebArena target hosts. Those hosts are fixture values in a benchmark config, not kake-owned properties, and C1 asserts nothing about them. Disposition: no kake scope. |
| **kumitate** | orchestration/tooling: OMP task/hub, ufo-fsd scripts and runtime (`:3`, `:12-13`); MCP/isolation frontier (`:17-22`); adjacent serving→kama, prompt→kotoba, method→chousa (`:27`) | None. The wave runs under OMP, but that is harness, not a claim | Risk: the words "config"/`env_config` could be read as OMP route/hub configuration. The object is WebArena serialized task text; no OMP/hub file is read or written, and no route/fallback fact is produced. Disposition: no kumitate scope. |
| **kama** | local model serving, baseURL pins, served-model reconciliation, liveness (`:3`, `:11`); refuses eval to kengaku (`:40`); boundary rule is live endpoint identity (`:41-43`) | None. Profiles are synthetic `.invalid` strings never probed; no listener, readiness or identity evidence exists | Risk: URL-valued replacement tokens could be misread as baseURL repointing. Measured: zero model-serving fields in the 812-task file (§3). C1 cannot support endpoint identity/readiness and must not be cited for it. Disposition: no kama scope. |

Host boundary (kengaku's own PROVINCE `:194-196`): the round-28 admission owns "static LLM-evaluation
interpretation, not the benchmark's web properties or runtime services." C1's generated-config
projection is the same class of static interpretation and stays inside it.

### Quote word counts (programmatic)

| Line(s) | Quote | Words |
|---|---|---:|
| chousa `:10-11` | "model-quality or evaluation claims (→ kengaku)" | 6 |
| tameshi `:14-15` | "every lane's gate remains its own; tameshi owns only the reusable craft" | 12 |
| kotoba `:29` | "kengaku — LLM/model evaluation and route telemetry." | 7 |
| kake `:37` | "`kama` owns local model-serving endpoints; kake owns remote web properties." | 10 |
| kumitate `:27` | "Local model serving and endpoints → kama." | 7 |
| kama `:41-43` | "is the thing at this baseURL the model this config believes it is, right now" | 15 |
| kengaku `:196` | "This owns static LLM-evaluation interpretation, not the benchmark's web properties or runtime services." | 13 |

## 3. Measured scope census (connector-side, not production output)

Method: `json.load` of the authenticated raw bytes, recursive string walk over all 812 task
objects, count the six pinned tokens by leaf path. Units are **token occurrences**, not changed
leaves and not task/profile projections.

| Leaf path (relative to one task object) | Token occurrences |
|---|---:|
| `start_url` | 818 |
| `eval.program_html[].url` | 338 |
| `eval.reference_url` | 217 |
| `eval.program_html[].required_contents.must_include[]` | 60 |
| `eval.reference_answer_raw_annotation` | 2 |
| **Total** | **1435** |

Independent cross-check by token: GITLAB 385 + REDDIT 336 + SHOPPING 281 + SHOPPING_ADMIN 300 +
WIKIPEDIA 0 + MAP 133 = 1435. The two counting orders agree.

Boundary-relevant observations:

- **No model-serving configuration.** `api_key` 0, `chat/completions` 0. The single `openai`
  substring is inside a Reddit post slug at `task_id 406`,
  `eval.program_html[0].url = __REDDIT__/f/Futurology/119517/openai-ceo-...` — a target-site path,
  not a baseURL field.
- **The two structurally non-URL leaves carry URL-shaped values.** `must_include[]` entries are
  relative URL paths (e.g. `__REDDIT__/f/space/...` at `task_id 552`); `reference_answer_raw_annotation`
  at `task_id 66` is two comma-separated relative URLs. Thus F3's phrase "non-URL-valued field"
  needs an explicit definition — schema/path type vs value content — before it is scored. Under the
  schema/path reading 62 occurrences qualify; under the value-content reading all 1435 are
  URL-bearing. This report does not score F3.
- **`__WIKIPEDIA__` has 0 raw occurrences.** That is silence about the generator contract, not
  evidence the token is unused; do not price it either way.
- These counts are **not** the projection's per-profile output and were not oracle-verified.
  `1435 token occurrences ≠ 2436 task/profile projections`; the units are distinct.

## 4. Contested fits — consolidated

1. **Terminology, not ownership:** "config/env_config" (kumitate), "endpoint/baseURL" (kama),
   "profile" (tameshi), "task text" (kotoba), "web property" (kake). Each resolves by object
   identity and required evidence standard: C1's object is pinned WebArena task text; its evidence
   is source-faithful text projection, with no host env, no runtime, no network and no deployment.
2. **Method adjacency:** tameshi's finite environment-differential vs C1's three-profile sweep.
   Different objects (host environment vs fixed substitution dictionaries) and different evidence
   (run-output variation vs deterministic text replacement). C1 must not be offered as F5 evidence.
3. **Within-claim definitional item:** F3's non-URL boundary (above). This is L1's call; it is not
   a sibling-province conflict.
4. **Reciprocity asymmetry (informational):** chousa, kotoba and kama explicitly route
   evaluation/model-quality to kengaku; kumitate, kake and tameshi do not name kengaku but their
   PROVINCE surfaces are disjoint from C1. Lack of a reciprocal line is not a claim of ownership.

No PROVINCE in the scanned set claims WebArena, generated eval configs, `config_projection`, or
`env_config` (six zero counts). That is consistent with disjoint scope; it is not proof of
fleet-wide absence.

## 5. What sibling silence does not license

- It does **not** establish that no lane owns generated-config work: sibling corpora, knowledge
  entries, tools and plans were not read under the metadata-only mandate.
- It does **not** raise novelty, score 7, calibration 8, or method standing. No new-method or
  new-model pricing follows, and no round/knowledge admission is implied.
- It does **not** verify C1's implementation, counts, oracle or tests; those remain L1/executor work.

## 6. Proposed bounded move (one)

**Typed replacement-role accounting with per-role oracle agreement, roles closed to observed key
paths.**

Classify every changed string leaf into exactly one role derived from its position in the pinned task
object:

| Role | Leaf paths |
|---|---|
| `target_locator` | `start_url`, `eval.program_html[].url`, `eval.reference_url` |
| `scorer_predicate_text` | `eval.program_html[].required_contents.must_include[]` |
| `annotation_text` | `eval.reference_answer_raw_annotation` |

Report occurrence counts **and** changed-leaf counts per role per profile, as separate units never
pooled with task counts. The independent oracle repeats the classification from the text contract
and any per-role mismatch is an exit-1 finding. Add one hand witness: a non-token,
model-endpoint-shaped key in a selftest fixture stays byte-identical, demonstrating closure of the
six-token dictionary.

Why non-obvious: the prereg requires "changed string leaves by JSON path and category" but never
defines category. A schema-shape reading labels 62 occurrences "non-URL" and inflates F3; a
value-content reading labels all 1435 URL-bearing and makes F3 false by construction. Role
classification measures what the benchmark contract consumes — the r28-owned static scorer surface —
and turns F3 into a typed, oracle-checkable result without any runtime inference.

- **Affected axis:** novelty (construct resolution of the coverage capability).
- **Held axes:** score 7 and calibration 8 unchanged; no new population, model run, runtime
  validity, method claim, or output-count change (still 812×3 = 2436 task/profile projections).
- **Risks:** role names could be read as runtime predicate consumption (keep them descriptive of
  text position; consumption stays r28's static trace); new counters could be mistaken for new
  metric units (label units explicitly); the role set must stay closed to observed paths or unseen
  roles become speculative.
- **Verification (for L1, not run here):** production and oracle per-role totals equal on all three
  profiles; role key sets identical across profiles; the non-token hand witness passes; summary
  prints role counts separately from token occurrences and task counts; exit 1 on any role mismatch.
- **If rejected:** C1 still meets the prereg with path+category; this is construct sharpening, not
  scope expansion.

## 7. Unknowns preserved

- Sibling `corpus/knowledge`, tools, plans and gates were not read; a sibling may hold
  benchmark-config material outside its PROVINCE.
- `browser_env.env_config` was not executed or inspected (contract); whether it defines more than
  the six expectation tokens is unknown here.
- Whether any projected value can create new token occurrences through cascade under these exact
  profiles is not asserted; the instrument/oracle must measure it.
- The upstream generator's behavior beyond the pinned 838 bytes and the raw JSON's JSON semantics
  beyond stdlib parsing were not re-derived here.
- F3's structural-vs-semantic definition and all forecast scoring remain L1's.
- No claim is made about sibling gate health, versions, branches or current work.

## 8. Verdict

Scope-only: no sibling PROVINCE ownership conflict blocks C1; every term adjacency resolves by
object identity and evidence standard; the one method adjacency (tameshi env-differential) is
explicitly non-transferable; residuals are named above. This is not round admission, not source
verification, and not a test report.

VERDICT: PASS
