# R31ConnSibling — does the C1 ground (harness runtime / verifier execution / benchmark infrastructure) belong to another province?

Seat: connector (sibling-overlap scan), round 31 (kengaku, hyaku run 6, 2026-10-25). Leaf: no subagents,
no production edits. Every `file:line` below was read at the lane working tree of baseline `0883e72`
(lane facts); no `git` command was run by this seat.

Access date for every repo row read here: **2026-10-25**.

## Verdict

**No sibling claims the C1 ground.** The entry reads a *published benchmark's* verifier resolution rule
(Harbor `VerifierConfig.environment_mode` / `Verifier.verify` at `6099b8cf`), a benchmark's own
`v2/tasks/…/tests/test.sh` (`66f92766`), and a benchmark's task tree (`2fd12b88`). Across all 21 lane
`PROVINCE.md` files the word `benchmark` appears in exactly two files — kengaku (12 hits) and kasegi
(1 hit, a routing row naming kengaku as the owner) — and no sibling names `laude-institute`, `harbor`,
`swe-bench`, `terminal-bench` or `toolathlon` at all. Two generalizations the entry *could* make are
adjacent and must be routed rather than absorbed: the isolation-substrate mechanism (kumitate) and the
reusable verifier-isolation craft (tameshi). Neither is contested as written.

## Sibling rows read (each with the check actually run)

| Lane | Row read | Bytes that decide the boundary |
|---|---|---|
| kumitate | `kumitate-shokunin/PROVINCE.md:21` | "Isolation substrates for parallel agents (git worktrees, harness isolation backends) — first entry `corpus/knowledge/agent-isolation-substrates.md` (round 45, exploratory): seat-containment rules derived from their mechanisms with demos; harness isolation is off on this host, jj workspaces are not demonstrated." — the **only** sibling claim that names a harness isolation substrate, and it names its own object: *parallel agents*. |
| kumitate | `kumitate-shokunin/PROVINCE.md:19` | "OMP harness contract (task batch, agent hub, agent discovery) — first entry `corpus/knowledge/omp-task-contract.md` (round 34); the docs track upstream `main` while the host runs the installed `omp` binary" — the harness is **OMP**, not a benchmark's. |
| kumitate | `kumitate-shokunin/PROVINCE.md:3` | "**Domain:** orchestration & tooling — scopes OMP task/hub, ufo-fsd scripts & runtime" |
| kumitate | `kumitate-shokunin/PROVINCE.md:13` | "Origin runtime layer `/home/vgpnk/Projects/ufo-fsd-alpha/crates/ufo-core-runtime/src/` … (`coverage_runtime`)" — "runtime" here is the ufo-core-runtime crate, not a verifier. |
| mori | `mori-shokunin/PROVINCE.md:294` | "- **Core, harness background-job capacity runway read (new FR15 advance, admitted round 25):**" |
| mori | `mori-shokunin/PROVINCE.md:307` | "(`maxRunningJobs: () => Math.min(100, cfgAsyncMaxJobs.get(settings))`), so the ceiling is a / property of the shipped harness, not of the configuration file." — reads the installed `omp` binary's clamp. |
| mori | `mori-shokunin/PROVINCE.md:335` | "- **Adjacent (kumitate owns the harness mechanism; the operator owns the configuration):**" — mori itself routes harness *mechanism* to kumitate. |
| kotoba | `kotoba-shokunin/PROVINCE.md:14` | "- Executable instruments over those surfaces — … `verifiers/verify_harness_claims.py`, `verifiers/compare_harness_independent.py`, …" — instruments over harness **claims** about kotoba's own substrate (SKILL.md/AGENTS.md/dispatch), not a benchmark harness. |
| kotoba | `kotoba-shokunin/PROVINCE.md:57` | "| kengaku | adjacent | 1f3b0f1e… | LLM and model research and evaluation (route telemetry is marked absent since 2026-10-15 …); kengaku keeps measured capability effects of prompt format, kotoba owns the craft rules …" |
| kaidoku | `kaidoku-shokunin/PROVINCE.md:102-104` | "- **Malware triage at scale** — verdict pipelines, sandbox detonation, bulk / classification `(unowned)`. The lane analyzes declared, caller-supplied / artifacts; it does not run a triage queue or label samples malicious/benign." — a **refusal** that marks sandbox detonation `unowned`; it is malware detonation, not a verifier container. |
| kama | `kama-shokunin/PROVINCE.md:73` | "tool now emits `kama-llamacpp-live/v2`: exact ready body, harness-SIGTERM / graceful teardown with returncode 0, …" — kama's own liveness probe harness for `llama-server`. |
| mado | `mado-shokunin/PROVINCE.md:28` | "`--regression` writes the embedded defect spec … into scratch, hashes the harness and its own bytes, and hands the spec to tameshi's `mutate-and-run.sh` read-only" — mado's own regression harness. |
| game-dev-2d | `game-dev-2d-shokunin/PROVINCE.md:10` | "Refuses: … harness/evidence auditing (harness-integrity, gate-evidence, rlm-dispatch); narrative canon (lore lane — contested scope is reported, not absorbed)." — a **refusal** naming fleet integrity agents, not a benchmark harness. |
| game-dev-3d | `game-dev-3d-shokunin/PROVINCE.md:34-35` | "asset rights clearance (art-east-asian-design); harness/evidence auditing / (harness-integrity, gate-evidence, rlm-dispatch); narrative canon (lore" — same refusal. |
| game-dev-3d | `game-dev-3d-shokunin/PROVINCE.md:77` | "- LLM/model research and evaluation belong to `kengaku-shokunin` (`../kengaku-shokunin/PROVINCE.md:3-6`)." |
| revenger | `revenger-shokunin/PROVINCE.md:22` | "harness/evidence auditing (harness-integrity, gate-evidence, rlm-dispatch);" — same refusal. |
| tameshi | `tameshi-shokunin/PROVINCE.md:3-4` | "**Domain:** verification-fixture craft — the reusable method of honest / checks: hermetic suites, mutation testing, fail-closed arms, verdict-line / discipline, no-permissiveness audits, before/after proof." |
| tameshi | `tameshi-shokunin/PROVINCE.md:11` | "ids), the game lanes' verifier-AGREE loops (fleet root `.ufo/waves/`)." — tameshi's verifier surface is *fleet* gates. |
| tameshi | `tameshi-shokunin/PROVINCE.md:14` | "**Refuses:** product domains — every lane's gate remains its own; tameshi" |
| kasegi | `kasegi-shokunin/PROVINCE.md:49` | "- kengaku — LLM evaluation and benchmarks" — kasegi's own adjacency row, naming this lane as the owner. |
| chousa | `chousa-shokunin/PROVINCE.md:10-11` | "**Refuses:** bounty-program scope and claim packages (→ kasegi); model-quality / or evaluation claims (→ kengaku); orchestration, multi-agent dispatch and agent" — chousa's own text routes the **claim** to kengaku. |
| kengaku | `kengaku-shokunin/PROVINCE.md:6` | "**Refuses:** anything outside this domain; report cross-domain evidence back to the orchestrator rather than absorbing it." — the standing rule this seat applies. |
| kengaku | `kengaku-shokunin/PROVINCE.md:51` | "§Errata round 10) sits in this lane's measurement harness and its fix is" — kengaku's own `bench-arena` `loop.sh`; the lane's only in-file "harness". |
| kengaku | `kengaku-shokunin/PROVINCE.md:141` | "\| **kumitate** \| OMP route resolution, fallback policy, operational failure taxonomy (`loop.sh` telemetry-source semantics, informational) \|" |
| kengaku | `kengaku-shokunin/PROVINCE.md:215-219` | "**Core addition:** the published task-validity instruments a benchmark maintainer runs on its own … it does not run a benchmark, certify a task, or own deployment configuration, runtime task validity, hosted judges, contamination measurement or any benchmark's web properties." |
| kengaku | `kengaku-shokunin/corpus/README.md:251` | "…a locus. Not deployment config, not runtime task validity, not contamination measurement." — the round-29 coverage row's own bound that C1 narrows. |
| kengaku | `kengaku-shokunin/corpus/README.md:273` | "*Partly discharged round 29 attempt 2 (2026-10-25):* `knowledge/benchmark-task-validity-checklist.md` builds the …" — the frontier bullet C1 continues. |

Fleet scans run (read-only, whole fleet, `*/PROVINCE.md`):
- per-lane `grep -c -i benchmark` → **kengaku 12, kasegi 1, every other lane 0.**
- per-lane `grep -c -i harness` → mori 13, game-dev-2d 2, game-dev-3d 2, kotoba 2, kumitate 2, revenger 2,
  kama 1, kengaku 1, mado 1, all others 0. Every non-kengaku hit is one of the rows in the table above.
- `grep -rn -i "laude-institute\|harbor\|swe-bench\|terminal-bench\|toolathlon\|verifier" */PROVINCE.md` →
  the five benchmark/repo names occur **only** in `kengaku-shokunin/PROVINCE.md` (`:124`, `:200`, `:221`);
  every other `verifier` hit is the literal `*-verifier-spotcheck.md` lesson filename, tameshi's
  "verifier-AGREE loops" (`:11`), or kotoba's `verify_harness_claims.py` (`:14`).
- `grep -rn -i "task validity\|task-validity" */PROVINCE.md` → only `kengaku-shokunin/PROVINCE.md`
  (`:201`, `:210`, `:215`, `:217`, `:219`). No sibling claims runtime task validity.
- Pre-append state confirmed: `test -e corpus/knowledge/benchmark-verifier-execution-model.md` → **ABSENT**
  (staged only, `~/Projects/shokuknow/merge/kengaku/`); `grep -cE '^\|[[:space:]]*S(092|093|100)[[:space:]]*\|'
  corpus/SOURCES.md` → **0**; registry holds **88** rows (`grep -cE '^\| *S[0-9]{3,} *\|'` → 88).

## (a) Siblings claiming harness runtime, sandbox/verifier execution, or benchmark infrastructure

Ranked by proximity. **Four claims exist; none of them is on this entry's ground.**

1. **kumitate — `kumitate-shokunin/PROVINCE.md:21`, a real claim on "harness isolation backends."**
   The closest text in the fleet. It is a Frontier row whose object is stated in the same sentence:
   *isolation substrates for parallel agents*. Its recorded state is "harness isolation is off on this
   host". Nothing in kumitate's file names a benchmark, a verifier, a task tree, or a reward file.
2. **kumitate — `:19` OMP harness contract, and `:13` the ufo-core-runtime layer.** Both claim *a*
   harness/runtime, and both are the fleet's own substrate (`omp` binary, `crates/ufo-core-runtime/src/`).
3. **mori — `:294`, `:307`, `:335`.** Claims a read of the installed `omp` binary's job clamp and, at
   `:335`, explicitly disclaims the mechanism ("kumitate owns the harness mechanism"). A harness *runtime*
   property read, on OMP, with the boundary already drawn by mori itself.
4. **kotoba — `:14`, `verifiers/verify_harness_claims.py` + `verifiers/compare_harness_independent.py`.**
   Claims *verification of harness claims*, scoped to kotoba's own surfaces (SKILL.md, AGENTS.md, dispatch
   prompts, substrate pins). A different verb on a different object.

**Negative claims (refusals), which create no contest:** game-dev-2d `:10`, game-dev-3d `:34-35`,
revenger `:22` all refuse "harness/evidence auditing (harness-integrity, gate-evidence, rlm-dispatch)" —
fleet *integrity* agents, no benchmark referent. kaidoku `:102-104` refuses "sandbox detonation" and marks
it `(unowned)`; a malware detonation sandbox is not a benchmark verifier container.

**Own-harness mentions, not claims on harness ground:** kama `:73` (its liveness probe's SIGTERM
teardown), mado `:28` (its regression harness), kengaku `:51` (its own `bench-arena` `loop.sh`).

**Benchmark infrastructure:** **no sibling claims it.** `kasegi-shokunin/PROVINCE.md:49` is the only
sibling line containing the word `benchmark`, and it is an adjacency row that *assigns* benchmarks to this
lane. `chousa-shokunin/PROVINCE.md:10-11` and `game-dev-3d-shokunin/PROVINCE.md:77` likewise route
evaluation to kengaku by their own text.

## (b) The closest non-contested boundary for this entry

**kumitate's `PROVINCE.md:21`, drawn by the object, not the word.** The lane's recorded rule from the
round-9 map is exactly this test — "Keep the boundary on the *object being measured*: kengaku owns
model/agent capability, benchmark design, calibration, and the causal interpretation of experimental
outcomes. A shared prompt, route, endpoint, or transcript does not transfer that subject-matter ownership"
(`corpus/evidence/round9-fleet/sibling-overlap.md:5`).

Applied here:

- **kumitate's isolation substrate contains *fleet agent seats*** — git worktrees, `omp` isolation
  backends, seat containment (`:21`). Its measured state is "harness isolation is off on this host".
- **The entry's container is a *benchmark task environment*** whose verifier may share it with the agent
  under test. The object is the benchmark's grading phase, not the fleet's seat boundary.

The two are non-contested because (i) kumitate's sentence fixes its own object ("for parallel agents"),
(ii) kumitate names no benchmark, verifier, task tree or reward file anywhere in the file, and (iii) the
entry's finding is a *default resolution rule in a published harness*, which is benchmark design — the
first item in the round-9 ruling's kengaku list.

Two further boundaries, also non-contested:

- **tameshi (`:3-4`, `:14`) — method, not object.** tameshi owns "the reusable method of honest checks";
  its own refusal says "every lane's gate remains its own". A fact about *Harbor's* grader is not a fact
  about the craft of writing gates, and the entry does not build a gate.
- **chousa (`:10-11`) — already routed here.** chousa owns "claim-vs-source verification" as *method* and
  refuses "model-quality / or evaluation claims (→ kengaku)". Opening three pinned source trees is this
  lane acting under chousa's method on an evaluation claim chousa has already handed over. The lane's own
  adjacent table records the same split at `kengaku-shokunin/PROVINCE.md:137`: "| **chousa** | research
  method — … the question → source-hierarchy → citation-chain → claim-vs-source method stays chousa's
  (`chousa-shokunin/SKILL.md`); this lane holds neither method nor duplicates it |".

## (c) What belongs partly to a sibling, and what the report must route rather than absorb

**Partly, yes — two slivers, both generalizations, neither of them the finding.**

| Sliver | Owner | Why it is theirs | What stays here |
|---|---|---|---|
| **A. The isolation-substrate mechanism reading**: what "shared" vs "separate" *contains*, and that the only unconditional protections are the tests-directory re-upload and the stale-reward deletion | **kumitate** (`PROVINCE.md:21`) | "Isolation substrates for parallel agents (git worktrees, harness isolation backends) … seat-containment rules derived from their mechanisms" is the same question asked of a different container | The benchmark-specific default, the per-benchmark axis-E answer, and the "which code path produced this score" qualification |
| **B. The reusable verifier-isolation craft**: "a grader that runs in the agent's environment grades an agent-modified environment; a trustworthy grader overwrites test files and deletes stale rewards" | **tameshi** (`PROVINCE.md:3-4`) | "hermetic suites, mutation testing, fail-closed arms, verdict-line discipline" is that craft, stated as reusable method | The evidence that a *named, published* harness defaults to shared mode — that is a benchmark fact, not a method claim |

Route the *craft/mechanism* sentences; do not route the entry's bytes, its predicate, or its three
`source:` rows. The precedent for that exact shape is already in this lane's file: round 10 kept the
`loop.sh` field-count bug in-lane and routed only "the resulting telemetry-source semantics" to kumitate
(`kengaku-shokunin/PROVINCE.md:48-53`).

**Must NOT be routed:**

- the SWE-bench Pro V2 qualification ("The verifier never runs in the agent's sandbox" is true of the
  locked replay protocol, not of Harbor's default path for the same task) — both statements are true of
  different code paths, and only this lane is reading both;
- the round-1 framing correction (axis E "partly observable" → "shared by default"), which edits this
  lane's own `corpus/knowledge/benchmark-task-validity-checklist.md`;
- the three `SOURCES.md` rows and the `used-by` binding — the registry is this lane's authority
  (`kengaku-shokunin/PROVINCE.md:215-219` already fixes the admission shape);
- **anything to chousa, kama, mori or kagi**: no endpoint, no serving plane, no credential and no
  journal/cgroup surface is read by this entry. kama's only near neighbour is `PROVINCE.md:73` (its own
  probe harness), and mori's is the OMP clamp (`:294-344`) — neither is touched.

**One framing hazard to state now, not after landing.** If the entry is described as reading "the harness's
runtime contract" without the benchmark qualifier, it collides with mori `:294-344` and kumitate `:19`
(both *do* own an OMP harness runtime property), and the round owes them a report-out. The qualifier that
keeps it clean is already in the entry's own first line: *Harbor, the harness both Terminal-Bench 2.0 and
SWE-bench Pro V2 run on*.

## (d) The pattern this lane has used before for such routing

The lane's established form is an appended, round-scoped block that names the recipient, the artifact, and
the boundary, and says in the first clause that the evidence was sent and not absorbed. Verbatim from
`kengaku-shokunin/PROVINCE.md:35-41`:

> Reported out this round (evidence sent, not absorbed): (1) kotoba — keep an
> explicit output-contract system prompt whenever tool affordances are exposed,
> else a benchmark records `finish=tool_calls` instead of capability
> (`corpus/knowledge/bench-arena-round7-scaffold-ablation.md`); (2) kasegi +
> kumitate — the ledger split recorded in the round-3 aggregator ruling stays
> explicit; (3) kagi — any Janitor consumer-endpoint discrepancy, with the
> unowned serving plane escalated.

Three properties of that pattern, all reused here:

1. **The recipient is named, and the claim is not transferred.** The block sits under the heading
   "## Refusals and reported-out scope (round 9, `corpus/evidence/round9-fleet/sibling-overlap.md`)"
   (`:22`), immediately after the standing rule at `:6` — "report cross-domain evidence back to the
   orchestrator rather than absorbing it."
2. **A pointer travels with it.** Round 10's instance (`:48-53`) is the closest analogue to sliver A:
   the `loop.sh` bug "sits in this lane's measurement harness and its fix is in-lane backlog, but the
   resulting telemetry-source semantics touch the operational failure taxonomy kumitate owns — recorded so
   the taxonomy does not treat `source=journal` rows as scraper outages." Mechanism routed, measurement
   kept.
3. **The routed artifact is filed, not just mentioned.** Round 25's form (`:168-172`) names the entry, the
   bound, the recipient, and a filed path: "its leg-share bounds are within-sample shares, never natural
   fallback rates or OMP route-resolution facts, which stay kumitate's
   (`falsify/ConnKumitateReportOut.md`)."

The tameshi form of the same pattern is already stated on the receiving side and should be reused for
sliver B: "ask for method advice, not transfer of gate ownership or a general claim from one lane"
(`tsukuroi-shokunin/PROVINCE.md:52`, ADJ-07).

## Draft report-out lines (for the round report, only if the framing ships)

Adjacent, not contested. File only if the corresponding generalization is written into the entry or the
round report:

```
kumitate | round-31 | kengaku C1's Harbor `environment_mode` reading is a benchmark task environment's
verifier container (shared vs separate), not an agent-seat isolation substrate. Recorded so
`agent-isolation-substrates.md` is not read as covering verifier grading phases; no change requested to
kumitate's row or entry.

tameshi | round-31 | kengaku C1 records that a named harness defaults to grading inside the agent's
environment, and that the only unconditional protections are a tests-directory re-upload and stale-reward
deletion. That is a benchmark fact, offered as method input for the hermetic-suite/ fail-closed craft; no
gate, no method ownership and no general claim is transferred.
```

No report-out is owed to chousa, kasegi, kotoba, kama, mori, kagi, kaidoku, kake, mado, game-dev-2d,
game-dev-3d or revenger for C1: each boundary is already stated in the sibling's own text, in this lane's
favour, or the sibling's surface is not read by this entry at all.

## Observed pointer drift (report, do not silently fix)

The frozen claim C1 quotes the round-29 coverage row's bound as `corpus/README.md:250`. At the baseline
tree the string is at **`corpus/README.md:251`**:

```
$ grep -n "Not deployment config, not runtime task validity" kengaku-shokunin/corpus/README.md
251:- **Benchmark task-validity instruments**: covered at primary-document synthesis depth (round 29 attempt 2, 2026-10-…
```

This seat did not adjudicate it. It is a citation pointer, not a predicate term: C1's predicate names the
entry, the three rows, the `verified-at` line, the index row and the `adoption_check.py` line, none of
which reads `README.md:250`. Flagged for the round to decide as an R-item or a dated erratum; not repaired
here (no production edits by this seat).

## Verification (commands actually run by this seat)

- `ls -d /home/vgpnk/Projects/shokunin/*-shokunin/` → 21 lane repos; `*/PROVINCE.md` present in all 21.
- Whole-fleet per-lane `grep -c -i benchmark` / `grep -c -i harness` over `*/PROVINCE.md` → counts as in
  §Sibling rows read. `grep -rn -i "laude-institute\|harbor\|swe-bench\|terminal-bench\|toolathlon\|verifier"`
  → the five names occur only in `kengaku-shokunin/PROVINCE.md`.
- `grep -rn -i "task validity\|task-validity" */PROVINCE.md` → kengaku only.
- `test -e corpus/knowledge/benchmark-verifier-execution-model.md` → ABSENT (staged only).
- `grep -cE '^\|[[:space:]]*S(092|093|100)[[:space:]]*\|' corpus/SOURCES.md` → 0;
  `grep -cE '^\| *S[0-9]{3,} *\|' corpus/SOURCES.md` → 88.
- `sed -n '3,6p;22,25p;141p' PROVINCE.md`, `sed -n '251p' corpus/README.md`,
  `sed -n '5p' corpus/evidence/round9-fleet/sibling-overlap.md` → the quoted bytes above.
- Read: all 21 sibling `PROVINCE.md`, `kengaku-shokunin/PROVINCE.md`, `kengaku-shokunin/corpus/README.md`,
  `corpus/evidence/round9-fleet/sibling-overlap.md`, `.ufo/waves/round-30/build/R30ConnSibling.md`, and the
  staged entry `~/Projects/shokuknow/merge/kengaku/knowledge/corpus/knowledge/benchmark-verifier-execution-model.md`.

Not run, and not claimed: no network fetch (none of the three pinned commits was opened by this seat — the
S092/S093/S100 source seats own that), no `adoption_check.py`, no `sources_adopt.py` run, no `git`
command, no write outside this file.

Tool installs/upgrades: **none**.

VERDICT: NO-CONTEST — the C1 ground is claimed by no sibling PROVINCE (no lane names Harbor, SWE-bench Pro, terminal-bench or Toolathlon; `benchmark` occurs only in kengaku and in kasegi's row routing it to kengaku); the closest boundary is kumitate `PROVINCE.md:21` ("harness isolation backends", object = fleet agent seats, harness isolation off on this host), so the round routes two generalizations out — the isolation-substrate mechanism to kumitate and the verifier-isolation craft to tameshi — and keeps the finding, the two-code-paths qualification and the three source rows in-lane.
