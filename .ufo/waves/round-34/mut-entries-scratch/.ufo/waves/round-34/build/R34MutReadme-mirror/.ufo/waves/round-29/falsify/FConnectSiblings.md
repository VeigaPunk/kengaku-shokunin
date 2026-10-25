writer: KengakuR29-2.FConnectSiblings-2

# FConnectSiblings — sibling-overlap scan for round-29 C1

- **Seat:** `KengakuR29-2.FConnectSiblings-2` (connector, round-29 post-crash falsify wave).
- **Actual writer:** `KengakuR29-2.FConnectSiblings-2`; no delegation, no subagents.
- **Date:** 2026-10-21.
- **Lane revision:** `56fd949a6478342531e61f4feecb4a685d831640` (`git rev-parse HEAD`, lane root).
- **Roots:** lane `/home/vgpnk/Projects/shokunin/kengaku-shokunin`; fleet `/home/vgpnk/Projects/shokunin`.
- **Production-source disclosure:** I read `plans/config_projection.py` (lines 10–21, 59–68, 347–359,
  476–518, 524–548) to test whether the audit path writes files or opens a network surface. This item is
  not an oracle or re-derivation item; the instrument was run read-only (`--summary`, `--selftest`) and
  was not modified.
- **Read-only attestation:** no production, fixture, corpus, SOURCES, SCORECARD, candidate or sibling
  writes; no git add/commit/checkout/stash/reset/branch/worktree; no lane/fleet writes outside this
  report. No tools installed or updated (stdlib `python3`, coreutils, read-only git only).

## 1. Axes named

| Axis | Role in this item |
|---|---|
| **novelty** (round-judged, score 7 held) | ownership-distinctness: does a sibling lane already own benchmark harness/config generation or WebArena serving? |
| **calibration** (score 8 held) | must not move: this scan adds no model run, sample, or statistical unit |
| **scope integrity** (supporting) | does the projection remain inside kengaku's declared province? |
| **evidence reproducibility** (supporting) | exact revisions, hashes, commands and units; no inferred counts |

## 2. Attack

The claim under attack is C1: an offline, source-faithful projection of the pinned WebArena
`scripts/generate_test_data.py` over the pinned 812-task raw file under three synthetic `*.invalid`
profiles, with provenance and output-index/task-ID mapping. The falsification question is not whether
the projection is correct (other seats attack counts and semantics). It is whether the capability is
**already owned by a sibling province** — which would make the round an out-of-province absorption —
or whether it **creates a serving/deployment artifact** outside kengaku's admitted static-interpretation
boundary.

Two concrete falsifiers were run:

1. **Ownership falsifier:** find any of the 20 sibling `*-shokunin` lanes that declares ownership of
   benchmark harnesses, benchmark-config generation, or WebArena serving; or any sibling corpus/tool/
   plan artifact that implements one.
2. **Surface falsifier:** show that the instrument's audit path writes a config file, contacts a
   service, or reads host environment/auth state — any of which would move it toward kama (serving),
   kake/tabi (web properties/browser), kagi (credentials), or kumitate (orchestration config).

## 3. Method and commands (observed)

All commands run from the stated root. Counts are the tool's or command's own output; no count is
inferred from prose.

| # | Command (root) | Output (exact unit) |
|---|---|---|
| 1 | `ls -d /home/vgpnk/Projects/shokunin/*-shokunin/` | 21 directories: kengaku + 20 siblings |
| 2 | `ls -d *-shokunin/ \| wc -l` (fleet root) | `21` |
| 3 | `ls -d *harness* 2>/dev/null \| wc -l` (fleet root) | `0` |
| 4 | `ls -d *gate-evidence* *rlm-dispatch* 2>/dev/null \| wc -l` (fleet root) | `0` |
| 5 | grep over the 20 sibling `PROVINCE.md` files, pattern `webarena\|WebArena\|generate_test_data\|config_projection\|env_config\|config_files\|test\.raw` | `No matches found` (0 of 20 files) |
| 6 | grep over the same 20 `PROVINCE.md` files, pattern `benchmark\|bench-arena\|harness\|WebArena\|arena` (case-insensitive) | 7 matching files: game-dev-2d, game-dev-3d, kama, kasegi, kotoba, kumitate, revenger; no `WebArena` |
| 7 | grep `webarena\|generate_test_data\|test\.raw` over all 20 sibling `corpus/` dirs, `gitignore:false` | `No matches found` |
| 8 | same pattern over all sibling `plans/` dirs, `gitignore:false` | `No matches found`; 11 paths absent, skipped by the tool (9 present searched) |
| 9 | same pattern over all sibling `tools/`, `scripts/`, `verifiers/` dirs, `gitignore:false` | `No matches found`; 9 paths absent, skipped by the tool |
| 10 | fleet-wide grep `webarena\|WebArena\|WEBARENA` (gitignore default) | only `MANIFEST.json` (round-28 claim text) and kengaku `.ufo/reports/round-28/kengaku.md`; no sibling lane file |
| 11 | `python3 plans/config_projection.py --summary` (lane root) | `POPULATION {"distinct_task_ids": 812, "input_task_count": 812, "profile_count": 3, "task_profile_projections": 2436, "tasks_with_any_token": 812}`; `TOTAL findings=0 exit=0`; process exit `0` |
| 12 | `python3 plans/config_projection.py --selftest` (lane root) | `SELFTEST clean cases=20 ...`; process exit `0` |
| 13 | `git status --porcelain -- plans/config_projection.py plans/fixtures/r29 plans/round-29-claims.md` | empty output; exit `0` |
| 14 | `sha256sum plans/config_projection.py plans/fixtures/r29/manifest.json plans/fixtures/r29/profiles.json` | `5673405e…a12e3`, `f6390b92…7bf87`, `90fdc34d…94e018` (full values below) |
| 15 | Python substring census over `plans/fixtures/r28/webarena/config_files/test.raw.json` | `api_key 0`, `chat/completions 0`, `base_url 0`, `model_name 0`, `:8080 0`, `:34113 0`, `llama 4`, `openai 1`; bytes `880776`; `"task_id"` occurrences `812` |

Pinned hashes (full): `plans/config_projection.py`
`5673405e79a0445c76f3e67e2e30ccf7a89847e90de4a74488b995540cea12e3`;
`plans/fixtures/r29/manifest.json`
`f6390b924c69f0cc8c47b2320b092060bb344b6a5e81c0075d3eb5aab817bf87`;
`plans/fixtures/r29/profiles.json`
`90fdc34d2f33e3100a2223fdaf5fc5f1016993b8e6723710cc4661e0da94e018`.

## 4. Ownership census — all 20 sibling lanes

The authoritative ownership statement is each lane's `PROVINCE.md`. Lines below are current at the
scan date. "No object match" means the lane's PROVINCE contains none of the §3 row 5 object terms.

| Sibling lane | Declared surface relevant to C1 | Exact anchor | Overlap with C1 |
|---|---|---|---|
| **kama** | local **model** serving, baseURL pins, served-model reconciliation; refuses model quality/eval to kengaku | `kama-shokunin/PROVINCE.md:40-43`: "model quality/eval (kengaku)" | **None.** C1 uses synthetic `*.invalid` values and never probes a listener. Kama's serving plane is model endpoints, not WebArena web apps. |
| **tameshi** | verification-fixture **method** (hermetic suites, mutation testing, fail-closed arms); product gates stay with their lanes | `tameshi-shokunin/PROVINCE.md:14-18`: "every lane's gate remains its own" | **None.** `config_projection.py --selftest` is kengaku's own gate; tameshi owns no benchmark config generator and never edits a sibling gate. |
| **kumitate** | orchestration/tooling; OMP harness contract (task batch, agent hub, agent discovery) | `kumitate-shokunin/PROVINCE.md:19`: "OMP harness contract" | **None.** "Harness" here is the agent-orchestration runtime, not a benchmark harness. C1 reads no OMP/hub file and writes no route config. |
| **kake** | named web properties and publishing (ds4cc.com, kimi.page/pro mirrors, Pages deploys); remote web properties vs local endpoints | `kake-shokunin/PROVINCE.md:37`: "kama owns local model-serving endpoints; kake owns remote web properties" | **None.** WebArena target hosts are fixture strings in a benchmark config, not kake-owned properties; C1 fetches nothing and deploys nothing. |
| **chousa** | research method and source hierarchy; explicitly refuses model-quality/evaluation claims **to kengaku** | `chousa-shokunin/tools/research-gate.sh:757` (`SCOPE_KENGAKU` includes `llm benchmark`, `llm benchmarks`, `llm scoring`); `:5450-5453` and `:5457` emit `route=kengaku`; `corpus/knowledge/scope-refusal-r12.md:22`; `corpus/knowledge/scope-phrase-gap-r18.md:9-19` | **None; corroborating.** Chousa pre-existing gate assigns LLM-benchmark scope to kengaku; C1 performs no external research and claims no research method. |
| **kasegi** | bounty/security research; adjacent list routes benchmarks to kengaku | `kasegi-shokunin/PROVINCE.md:47`: "kengaku — LLM evaluation and benchmarks" | **None; corroborating.** The explicit adjacent-list ownership line names kengaku. |
| **tabi** | browser and web-interaction craft; drives real browsers against real sites; refuses web publishing and consequential actions | `tabi-shokunin/PROVINCE.md:3-6` domain; `:15-19` refusals | **None.** C1 projects serialized text offline; it opens no browser, target, CDP session, or site. |
| **kaidoku** | reverse engineering of shipped artifacts with REA; static analysis, evidence-first | `kaidoku-shokunin/PROVINCE.md:1-6` (domain) | **None.** No WebArena object terms; C1 analyzes a Python generator as inert AST, not a shipped artifact under REA. |
| **revenger** | reverse-engineering evidence ledger; refuses harness/evidence auditing | `revenger-shokunin/PROVINCE.md:22`: "harness/evidence auditing (harness-integrity, gate-evidence, rlm-dispatch)" | **None.** The refused owners do not exist under this root (`ls -d *harness*` → 0; `*gate-evidence*`/`*rlm-dispatch*` → 0); revenger owns no benchmark generator. |
| **game-dev-2d** | game mechanics; refuses generic harness/evidence auditing | `game-dev-2d-shokunin/PROVINCE.md:10` | **None.** Lane-local replay fixtures only. |
| **game-dev-3d** | Unreal/game development; refuses generic harness/evidence auditing | `game-dev-3d-shokunin/PROVINCE.md:34-35` | **None.** Lane-local pointer/replay harnesses only. |
| **kotoba** | prompt/skill craft and executable verifiers over those surfaces | `kotoba-shokunin/PROVINCE.md:13-14` (verifier list); `:30` routes evaluation to kengaku | **None as an owner.** `verifiers/verify_harness_claims.py:1-6` verifies omp/opencode **skill-router** claims, not benchmark config generation. |
| **audio** | game audio production, headless WAV fixture measurement | `audio-shokunin/PROVINCE.md:3-5` owns audio; `corpus/knowledge/2026-10-14-sox-fifo-hold-bound.md:16` names `measure_audio.py` | **None.** `measure_audio.py` measures WAV fixtures (duration/loudness/spectrum), not benchmark task/config generation. |
| **kagi** | secrets/vault operations and credential hygiene | no object-term match in `PROVINCE.md` | **None.** C1 reads no credential, auth-state, environment value, or private URL. |
| **lore** | world-bible consistency | no object-term match | **None.** |
| **kotodama** | linguistic/cultural worldbuilding | no object-term match | **None.** |
| **mado** | desktop/compositor craft | no object-term match | **None.** |
| **mori** | fleet/host observability | no object-term match | **None.** |
| **souji** | repo/workspace hygiene census | no object-term match | **None.** |
| **tsukuroi** | host operability and repair | no object-term match | **None.** |

Result: **0 of 20 sibling lanes claim benchmark harness/config generation or WebArena serving.** The
only sibling lines that touch the words are (a) routes of evaluation/benchmark scope **to kengaku**
(chousa, kasegi, kotoba, kama), and (b) lane-local measurement/verification harnesses whose objects are
audio WAVs, game replays, skill routers, OMP orchestration, or fleet gates — not LLM benchmark configs.

The fleet-level ROADMAP corroborates the absence of an unowned harness province: the candidate domain
`kessho` ("CI/verification harnesses") was **not minted** because "every instance was absorbed by the
province that needed it" (`ROADMAP.md:80-83`). Kengaku's projection gate is one such absorbed instance.

Term false positives, disposed rather than counted: a broader `config_files` scan matches
`audio-shokunin/corpus/fixtures/measure_audio.py:44681` (a regex for `opening config file`) and
`mado-shokunin/corpus/knowledge/walker-route-r18.md:119` (`find_config_files("themes")`). Neither is
WebArena's `config_files/` directory or a config generator. A scan for `config_projection` and
`env_config` across all sibling corpora/plans/tools returned `No matches found`.

## 5. Surface falsifier — does C1 stay inside kengaku's province?

### 5.1 Province text

- Kengaku's domain is "LLM/model research & evaluation" (`PROVINCE.md:3`).
- The round-28 admission owns "static LLM-evaluation interpretation, not the benchmark's web properties
  or runtime services" (`PROVINCE.md:196`).
- The same section names the exact open frontier C1 advances: "generated configs, runtime task validity,
  hosted judges and contamination remain open. Serving-plane restoration stays operator/kama-owned"
  (`PROVINCE.md:200-202`).
- The corpus index repeats that "generated eval-time configs" remain open (`corpus/README.md:337-338`).

Thus C1 is on kengaku's **declared frontier**, and its object (serialized task text → projected text)
is the same static-interpretation class as the admitted round-28 audit. This is a scope finding; it
does not admit the candidate or raise novelty.

### 5.2 Audit path is read-only and offline

`plans/config_projection.py` at the pinned hash:

- `audit()` (`:347-359`) reads pinned bytes with `read_pinned`, parses the generator with `ast.parse`,
  parses profiles/raw with `json.loads`, and calls `audit_text`; it returns an in-memory result.
- `main()` (`:524-548`) prints JSON or summary lines to stdout and returns the exit code.
- File writes occur only inside `selftest()` (starts `:385`): `mkdir` `:477`, `copyfile` `:478`,
  `write_bytes` `:487`, `write_text` `:497`, `write_bytes` `:511`, `write_bytes` `:518`. Those are
  `tempfile`-backed CLI controls, not the `--summary`/`--json` path.
- Imports (`:10-21`) include `subprocess`, `tempfile`, `shutil` for the selftest; there is no `socket`,
  `urllib`, `requests`, or `http` import. `browser_env` appears only as an AST string comparison
  (`:65-68`), never as an import.
- `--summary` emits its own limit: "no runtime evaluator, browser, helper, judge, task-validity,
  model-performance or contamination claim" (11 words).
- None of the instrument's output names a real endpoint; all 18 profile values use a `.invalid` host and
  each profile's purpose is "controlled synthetic text-substitution profile, not an observed deployment"
  (8 words). `profiles.json` has 3 profiles × 6 values = 18 synthetic values.
- The raw task file contains no serving config fields: `api_key 0`, `chat/completions 0`, `base_url 0`,
  `model_name 0`, `:8080 0`, `:34113 0`. The 4 `llama` and 1 `openai` substrings are task text, not
  fields: `test.raw.json:12754` (Reddit slug), `:22594` and `:22596` (issue/intent text), `:22611`
  (`must_include` value), `:12719` (Reddit slug).

Conclusion: the projection neither serves, configures a deployment, probes an endpoint, nor writes a
benchmark file. It is an offline static audit, inside kengaku's admitted static-interpretation boundary
and on its declared generated-config frontier.

## 6. Mismatches, corrections, and contradictions (exact)

No mismatch changes the scope conclusion. The following are recorded rather than smoothed.

| # | Location / claim | Observed value | Disposition |
|---|---|---|---|
| **M1** | `build/R29ConnectScope.md:140-141` and `:186-188`: sibling corpora/tools/plans "were not read"; "a sibling may hold benchmark-config material outside its PROVINCE" | I read all 20 sibling `corpus/`, `plans/`, `tools/`/`scripts/`/`verifiers/` dirs with `gitignore:false`; 0 matches for `webarena\|generate_test_data\|test\.raw` (§3 rows 7–9) | Residual narrowed for current tracked/ignored text. It is still not a proof of absence in git object stores or opaque binaries. |
| **M2** | `build/R29ConnectScope.md` §3: "zero model-serving fields in the 812-task file" | Six field literals are 0 (`api_key`, `chat/completions`, `base_url`, `model_name`, `:8080`, `:34113`); the same file has `llama 4` and `openai 1` as task text | **No value contradiction, but a wording hazard.** Do not cite the phrase as "zero model-name text"; the model names are target-site/task content. |
| **M3** | Build report's kotoba anchor: `kotoba-shokunin/PROVINCE.md` `:29`, 32 lines, sha256 `c1fa9d97e4fe4798ea873cf2e80acac5f14f8c84b30036c927e1ae038b5fe524` | Current: 33 lines, sha256 `2e683ed1c946edbc732e96cdae7a06e7d3d2a2281fced548abca7414b2058e64`; the same sentence is at `:30`. History: `f2f9ee1d88bc42d80fb96075db0fc3b43fb8a321` has the old blob; `7ad7fadfc09354b74fb66605dfb0c1182c115a2f` (round-47, `2026-10-21T13:46:13-03:00`) has the new blob; `git status --porcelain -- PROVINCE.md` empty | **Real stale line anchor.** The routing stance is unchanged; only the line moved. Cite `:30` today, or label the old citation with its blob/revision. |
| **M4** | `PROVINCE.md:14` still lists a historical served model at `http://127.0.0.1:34113`; `PROVINCE.md:200-202` says serving-plane restoration is operator/kama-owned; the `§Province map` historical table marks that endpoint absent | Three different temporal statements in one file | **Internal historical/supersession ambiguity, not a sibling conflict.** C1 uses none of them; no endpoint is probed or claimed. |
| **M5** | Candidate draft `:80` says "Serving-plane ownership stays outside this lane" | Consistent with `PROVINCE.md:200-202` and kama's refusal (`PROVINCE.md:40-43`) | **No mismatch.** |
| **M6** | The task prompt's examples "kama serving plane, tameshi testing" | Kama's surface is local **model** serving (not WebArena web serving); tameshi's surface is verification-fixture **craft** (not benchmark harness generation) | **Terminology collision only.** Neither owns C1's object. |

M3 reproduction commands: `wc -l PROVINCE.md` → `33`; `sha256sum PROVINCE.md` → `2e683ed1…`;
`git log --oneline -3 -- PROVINCE.md` → `7ad7fad`, `f2f9ee1`, `43e0c02`;
`git show <rev>:PROVINCE.md | sha256sum` → `2e683ed1…` at `7ad7fad`, `c1fa9d97…` at `f2f9ee1`;
`git status --porcelain -- PROVINCE.md` → empty.

No sibling declaration contradicts kengaku's ownership; no sibling artifact matching the object terms
implements the generator projection. The concrete citation defect is M3's stale kotoba line anchor;
M2 is a wording hazard and M4 an internal history ambiguity. None is a scope failure.

## 7. Affected axes

- **Novelty (judged):** the ownership-distinctness evidence supports the capability's novelty claim
  against "a sibling already owns this"; it does **not** raise score 7 and adds no new capability.
- **Calibration (held):** no model run, sample, trial, or statistical unit was added; score 8 unchanged.
- **Scope integrity (supporting):** C1 remains static/offline; the serving/deployment boundary is intact.
- **Evidence reproducibility (supporting):** every count above is a command output at `56fd949`; sibling
  hashes/line anchors are dated.

## 8. One bounded move (proposal to L1)

**Move:** add a single dated "cross-lane ownership receipt" to the candidate entry — via a re-cut freeze
or an append-only errata, never by editing the frozen `7006b93d…` bytes — stating exactly:

> At kengaku `56fd949` (2026-10-21), 20 sibling lanes were scanned: 0/20 `PROVINCE.md` files and 0
> matches in sibling `corpus/`, `plans/`, and `tools/` for `webarena|generate_test_data|test.raw`.
> Chousa routes `llm benchmark(s)` to kengaku; kama refuses eval; tameshi keeps gate ownership;
> kumitate owns the OMP harness only; kake owns named web properties only. `config_projection.py`
> audit mode writes stdout only.

Use the current kotoba anchor `:30` (blob `2e683ed1…`), not the build's `:29` (`c1fa9d97…`).

**Why non-obvious:** the novelty threat is not a visible competitor lane; it is *silent absence of an
owner*, which can be misread either as unowned ground anyone may take or as someone else's harness.
A dated, bounded negative receipt fixes the boundary without adding a claim, a count, or a method.

**Affected axis:** novelty (ownership distinctness / construct clarity). **Held:** calibration 8,
score 7, all count units.

## 9. Risks

- The receipt is a **dated bounded census**, not a fleet-wide absence proof; sibling repos can move
  (M3 is the live example). Keep the revision/date and recheck on-release.
- A negative receipt can be mistaken for a new capability or a score increase. It must remain provenance.
- Adding it to the frozen candidate would break the freeze digest; use a re-cut freeze or an
  append-only errata with the old digest named.
- `gitignore:false` searches text files; git object stores and opaque binaries were not decoded.

## 10. Verification (for L1, not run here)

1. Re-run §3 rows 5, 7, 8, 9, 10; expect `No matches found` for the object terms and only the fleet
   `MANIFEST.json` + kengaku round-28 report for the fleet-wide term.
2. `python3 plans/config_projection.py --summary` → `TOTAL findings=0 exit=0`; `--selftest` → exit 0.
3. `git status --porcelain -- plans/config_projection.py plans/fixtures/r29 plans/round-29-claims.md`
   → empty.
4. Confirm the candidate cites kotoba `PROVINCE.md:30` at blob `2e683ed1…`, or labels the old
   `:29`/`c1fa9d97…` citation with its revision.
5. Confirm no new counts or score language entered the entry; the receipt is provenance only.

## 11. Unknowns and limits

- Sibling git object stores, `.jj` operation logs, and opaque binaries were not decoded; a historical
  commit could contain WebArena material even though no current tracked/ignored text does.
- `PROVINCE.md` is the declared ownership source; a lane could hold undeclared material. The corpus/tool
  searches reduce, but do not eliminate, that risk.
- Kama's serving-plane scope is local model endpoints; whether a future WebArena **web-app** serving
  plane would be kama's, kake's, or unowned is not decided here.
- This scan does not verify C1's projection counts, oracle, implementation, or admission; it is scope
  evidence only.
- No tools were installed or updated.

## 12. Scoped verdict

The attack resolves in favor of the claim's scope: by declared `PROVINCE.md` and the scanned text, no
sibling lane owns benchmark harness/config generation or WebArena serving; the sibling benchmark
references route to kengaku; and the instrument's audit path is offline/read-only with synthetic
`*.invalid` values and no serving artifact.
The projection stays inside kengaku's declared province and its open generated-config frontier. The
concrete citation mismatch is the build report's stale kotoba line anchor (`:29`/`c1fa9d97…` vs
current `:30`/`2e683ed1…`); M2 is a wording hazard and M4 an internal history ambiguity. The repair
does not change the scope conclusion. This is scope evidence, not round admission and not verification
of C1's counts.

VERDICT: PASS
