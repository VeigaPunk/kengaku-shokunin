# kengaku-shokunin — Province

**Domain:** LLM/model research & evaluation — scopes ~/Projects/webzites/repos/llm-wiki, route telemetry

**Owns:** the domain knowledge, playbooks, error patterns, and checklists above.
**Refuses:** anything outside this domain; report cross-domain evidence back to the orchestrator rather than absorbing it.

## Surfaces (re-verified round 14, 2026-09-29; route telemetry absent; benchmark battery relocated — see rows)

| Surface | Path / endpoint | What this lane does with it |
|---|---|---|
| Research notes (SSOT for eval craft) | `~/Projects/webzites/repos/llm-wiki` — `wiki/ai/agents-and-engineering/`, `wiki/karpathy/`, `wiki/ai/{foundations,alignment-and-training,books,scaling-and-forecasting}/`, `Home.md`, `raw/` | digest into `corpus/knowledge/eval-*` entries; the `~/wikillm/llm-wiki` path does **not** exist here (`test -e` → absent) **ABSENT 2026-10-20** (round 25: first local path fails `test -e`; superseded by §Province map) |
| Local benchmark battery | `~/archive/bench-arena/` — relocated intact from `~/bench-arena/` during round 14; `tasks/`, `grade.sh`, `loop.sh`, `report-grok45.csv`, `report-qwenlocal*.csv`, `telemetry-qwenlocal-v2.csv` all resolve at the archive path | authored runs, status-flip and truncation taxonomy; content no-drift (0 files newer than 2026-09-28), but historical commands using the old path are frozen evidence **ABSENT 2026-10-20** (round 25: first local path fails `test -e`; superseded by §Province map) |
| Served local model | `http://127.0.0.1:34113` — `/v1/models`, `/health`, `/v1/chat/completions` (Qwen3-Coder-30B-A3B-Instruct **UD-IQ2_XXS**, `owned_by=llamacpp`, `n_ctx=16384`). **Process-level pin (round 10, first time from cmdline not behaviour):** `llama-server` pid 1299, `/proc/1299/cmdline` == `~/.config/systemd/user/qwen-coder.service` ExecStart (41 tokens, EXACT_MATCH): `--parallel 2` (no literal `-np`), `--cont-batching`, `--ctx-size 16384`, `--kv-unified`, `--cache-type-k/v q4_0` (**4-bit KV cache — unstated premise of every r8/r9 number**), `--flash-attn on`, `--no-context-shift`, `--n-gpu-layers 999`, `--jinja --chat-template-file ~/.config/llama/qwen-coder-godspeed.jinja` (custom non-upstream template). Evidence: `corpus/evidence/round10-fleet/r10-scout-endpoint.md` + raw captures `models-34113.json`, `props.json`, `slots.json`; identity re-probed via `/v1/models` + `/health` 200 each round | every probe in `corpus/evidence/`; identity re-probed each round; hermetic gates pin committed bytes, never `/proc` **ABSENT 2026-10-20** (round 25: first local path fails `test -e`; superseded by §Province map) |
| Route telemetry | `~/Projects/bounties/ledger/telemetry.jsonl` — **ABSENT**, reconfirmed round 14 (last resolved round 11 at 7,226 lines; no relocation under `~/Projects`, `~/archive`, or Trash) | model×lane and reroute-chain **historical inference about model service** only; never treat the path as live |
| Client CLI telemetry | `~/.bailian/telemetry.jsonl`, `~/.bailian/wiki-sync-state.json` | quota-vs-auth failure split, poll-verb rule **ABSENT 2026-10-20** (round 25: first local path fails `test -e`; superseded by §Province map) |
| Model catalogs | `~/.bailian/skills/bailian-docs-llm-wiki/models/{index.md,models.jsonl}`, `https://huggingface.co/api/models`, `https://openrouter.ai/api/v1/models` | selection fields, open-weight twins **ABSENT 2026-10-20** (round 25: first local path fails `test -e`; superseded by §Province map) |
| Own probe artifacts | `corpus/evidence/round8-horizon/`, `round9-replication/`, `round9-fleet/`, `round10-fleet/`, `round11-power/`, `round11-fleet/`, `round12-ladder/`, `round12-fleet/`, `round13-ack-state/`, `round14-fleet/` | durable run bytes + analyses + L2 fleet artifacts; nothing headline-bearing cited from `/tmp` or session-only storage |
| In-repo gate | `grader.py` (repo root; `python3 grader.py` → exit 0/1/2; `--selftest` S0–S7) | hermetic offline replay of **four** probe trees (r8/r9/r11/r12); 733 checks after the round-14 analysis-byte pin, including three r12 md5 pins; round-14 mutation test killed 4/4 fresh corruptions |
| Public literature | arXiv / ACL Anthology / ICLR proceedings / vLLM docs / GitHub issues (URLs in `corpus/knowledge/eval-prior-art-calibration.md`) | novelty pricing of local findings |

## Refusals and reported-out scope (round 9, `corpus/evidence/round9-fleet/sibling-overlap.md`)

- **Not owned:** the model-serving plane (llama-server flags, slot/batch
  config) — no lane owns it; escalate to the integrator instead of remediating.
- **kagi:** Janitor consumer-side endpoint/credential config.
- **kumitate:** OMP route resolution, fallback policy, operational failure
  taxonomy.
- **kasegi:** bounty ledger mission-state / dispatcher semantics.
- **kotoba:** prompt- and skill-craft rules, render/trigger behaviour — this
  lane keeps the *measured* effect of prompt format on capability and hands the
  reusable craft implication out.
- **kake:** web properties; the shared word "probe" carries no scope.

Reported out this round (evidence sent, not absorbed): (1) kotoba — keep an
explicit output-contract system prompt whenever tool affordances are exposed,
else a benchmark records `finish=tool_calls` instead of capability
(`corpus/knowledge/bench-arena-round7-scaffold-ablation.md`); (2) kasegi +
kumitate — the ledger split recorded in the round-3 aggregator ruling stays
explicit; (3) kagi — any Janitor consumer-endpoint discrepancy, with the
unowned serving plane escalated.

Round-10 report-outs (evidence sent, not absorbed): (1) **integrator / unowned
serving plane** — the process-level pin above is capability-*interpretation*
evidence this lane keeps, but flag-change authority (KV quantization level,
`--parallel`, context-shift policy) stays unowned; the q4_0 KV cache and
`--kv-unified` semantics are material to any cross-model comparison drawn from
:34113 and were unstated until round 10. (2) **kumitate (informational)** — the
bench-arena `loop.sh` field-count bug (5 emitted fields read into 6 vars ⇒
`telemetry_source=journal` unconditionally; `corpus/knowledge/bench-arena-fresh-run.md`
§Errata round 10) sits in this lane's measurement harness and its fix is
in-lane backlog, but the resulting telemetry-source semantics touch the
operational failure taxonomy kumitate owns — recorded so the taxonomy does not
treat `source=journal` rows as scraper outages. (3) Operator rule re-confirmed
mid-round: domain source repos (webzites/llm-wiki, bounties, ufo-fsd-alpha) are
read-only for this lane; upstream-bound findings travel in the round report.

Round-11 report-outs (evidence sent, not absorbed): (1) **protocol** — the
preregistration standard (hashed predictions + filed power analysis + Brier
scoring + ordering proof + hermetic replay gate) has no sibling owner per
`corpus/evidence/round11-fleet/r11-connector.md`; a fleet-wide *standard*
would belong to protocol/integrator — referred, not imposed. (2) **kotoba** —
ack compliance under checkpoint schedules is 49–65% (the model emits
unrequested full states on ack turns; the r9-verbatim post-checkpoint
spillover ask inflates this by design): prompt-craft evidence for benchmark
authors who treat "Reply 'ok'" turns as free
(`corpus/knowledge/bench-arena-round11-power.md`). (3) **integrator / unowned
serving plane** — the r11 `descriptors` record re-pins the same stack as
round 10 (pid 1299, 41-token argv, q4_0 KV, `--kv-unified`); ScoutPrereg
fetched public evidence that q4_0-KV measurably perturbs outputs (llama.cpp
PR #21038 tables), making the KV-quantization level material to ANY
cross-model number drawn from :34113 — flag-change authority remains unowned.

Round-11 report-out addition: (4) **kasegi** — the bounty-ledger tree
`~/Projects/bounties/` (their namesake surface, incl. `ledger/telemetry.jsonl`)
went absent from this host mid-round-11; last observed resolving 23:32Z
(`corpus/lessons/round-8-aggregator-box3-coldrun.md` command 3, live count
7,226). `find ~ -maxdepth 4 -name 'telemetry.jsonl' -path '*ledger*'` → 0
hits; `~/Projects/the-bounty-hunter/` exists but carries no
`ledger/telemetry.jsonl`. Cause is operator-side host state, not lane state;
this lane marks its surface ABSENT and keeps its historical citations.

Round-12/14 report-outs (evidence sent, not absorbed): (1) **kotoba** — prompt
intent must be derived from the runner, not from a `-ack` storage suffix:
r11 CKPT710 is 85.9% prefix / 84.4% bare `ok` over 384 true ack-only turns,
not 64.5% over 512 mixed-label rows; state fidelity and contract compliance are
separate. (2) **aggregator/protocol** — rounds 12 and 13 both stopped with
artifacts uncommitted and unindexed; a closeout carry-over gate should require
commit + LOG + SCORECARD + index parity before a lane report closes.
Respawn as the cause is `[INFERENCE]`, not established. (3) **No new serving
plane report-out** — endpoint id, pid 1299, 41-token argv, q4_0 KV,
`--kv-unified`, and `--parallel 2` remain exact matches. Evidence:
`corpus/evidence/round14-fleet/{r14-connector,r14-scout-surfaces}.md`.

## Province map — round 24 (2026-10-19)

*Correction note (appended, append-only): the header's "re-verified round 14,
2026-09-29" on `## Surfaces` is superseded by this section — several rows there
no longer resolve. The old table is retained verbatim as the historical record;
the current state is below.*

### Core

Surfaces that resolve today, each with the check actually run and its result:

| Surface | Check run today | Result |
|---|---|---|
| In-repo verdict gate | `test -e grader.py && sha256sum grader.py` | present; `90c87c88…ae941f` (replay tree r8/r9/r11/r12; `python3 grader.py` is the offline entry point) |
| Own probe artifacts | `for d in round8-horizon round9-replication round9-fleet round10-fleet round11-power round11-fleet round12-ladder round12-fleet round13-ack-state round13-coverage round14-fleet round18-kimi-routing; do test -d corpus/evidence/$d || echo missing $d; done` (prints nothing) | all present; plus 28 root receipt logs indexed in `corpus/README.md` |
| Attribution instrument + frozen tables | `test -e plans/attrib_probe.py && sha256sum plans/attrib_probe.py`; `test -e plans/attrib-r21-frozen.md` / `-r22-` / `-r23-` | all present; probe sha256 today `489f938a…16e06b` (floats between trials and landing per the r21 lesson — frozen anchors live in the `-frozen.md` files) |
| Corpus gate docs | `test -e corpus/QUALITY.md` | present (admission bar Q1–Q8 + round-closure criteria, created round 24) |
| Public-literature registry | `test -e corpus/SOURCES.md` | present; 25 rows, contract-v1 census clean (`corpus/evidence/round24-census/after.txt`); receipts `corpus/evidence/round24-sources/gate.md` |
| ds-flash-shim source (read-only) | `sha256sum ~/.local/share/ds-flash-shim/shim.py` | present; `42d86d99…15a386` — identical to the disclosed pin in `evidence/attrib-r22-*.log` / `attrib-r23-stream.log` |
| Live probe endpoint | `ss -ltn 'sport = :8791'` | LISTEN on `127.0.0.1:8791` (ds-flash-shim, read-only shim; `:8793` not probed this round) |
| Public literature | URLs cited in `knowledge/eval-prior-art-calibration.md`, `attrib-prior-art-r21.md`, and the ART dossier | reachable-by-citation only — documentation reads only this round, no live model/endpoint traffic |
| Interval re-verdict instrument (round 25) | `python3 plans/attrib_calibration.py --summary` and `--selftest` | exit 0 / exit 0; P1 receipts sha256-pinned; 4 unique samples, 92/92 correct, transitions FAIL>UNTESTED 2, PASS>INDETERMINATE 1 |
| State-assertion check (round 25) | `python3 plans/state_check.py --summary` and `--selftest` | exit 0 / exit 0 on the landed tree (base `6180e4f`: exit 1, 10 mismatches) |

*Round-25 correction (appended 2026-10-20): the "Public-literature registry" row above says 25 rows; the registry held 26 at base (S026, `e21f9ea`) and holds 37 after round 25 (`grep -cE '^\| *S[0-9]{3,} *\|' corpus/SOURCES.md`). Five `## Surfaces` rows now carry dated `ABSENT` markers (QUALITY R4).*

### Frontier

The ground named in `corpus/README.md` §Frontier: agentic benchmark task-spec
audits (Terminal-Bench 2.0 / Toolathlon / SWE-bench Pro primary specs —
unopened leads), contamination transparency cards, judge calibration applied
to this lane's own grader/attribution outputs, an identity-verified endpoint
for novelty probes, and non-karpathy wiki topics (source absent).

### Adjacent

Owner lanes and what is routed to them (grounded in existing PROVINCE/lesson
text, not renegotiated this round):

| Owner | What is routed |
|---|---|
| **kama** | serving plane + endpoint identity — `SKILL.md` and `lessons/round-16-recensus.md` record that kama is rostered and owns serving-plane health/detection and endpoint identity; kengaku keeps *interpretation* evidence and never remediates flags (`--kv-unified`, q4_0 KV, `--parallel`) — flag-change authority is unowned/integrator |
| **chousa** | research method — `corpus/QUALITY.md` and the SOURCES contract both state the question → source-hierarchy → citation-chain → claim-vs-source method stays chousa's (`chousa-shokunin/SKILL.md`); this lane holds neither method nor duplicates it |
| **kotoba** | prompt- and skill-craft rules — measured capability effects of prompt format stay here; reusable craft implications route out (r7 tools-without-system, r11/r12 ack-intent findings) |
| **protocol / aggregator** | fleet process — a fleet-wide preregistration/replay-gate standard and closeout carry-over gates were referred round 11/12–14, not imposed; `SOURCES.md` contract-v1 is fleet-frozen |
| **kagi** | Janitor consumer-side endpoint/credential config (round-9 routing) |
| **kumitate** | OMP route resolution, fallback policy, operational failure taxonomy (`loop.sh` telemetry-source semantics, informational) |
| **kasegi** | bounty-ledger mission-state / dispatcher semantics — plus the round-11 report that `~/Projects/bounties/` went absent operator-side |
| **kake** | web properties; the shared word "probe" carries no scope |

### Historical — absent, not governed

Every path in the `## Surfaces` table that does not resolve today. `test -e`
was run on each; the port was checked with `ss` only (no HTTP traffic):

| Surface | Check | Result today | Last resolved |
|---|---|---|---|
| `~/Projects/webzites/repos/llm-wiki` | `test -e` | absent | wiki reads recorded rounds 8–12 (2026-09-28/29); absent since round-13 coverage receipt |
| `~/wikillm/llm-wiki` | `test -e` | absent | never existed on this host (noted in the table itself) |
| `~/archive/bench-arena` | `test -e` | absent | round 14 (2026-09-29, relocated from `~/bench-arena`); absent per round-13 receipt |
| `~/bench-arena` | `test -e` | absent | round 13; superseded by the archive path, now also absent |
| `http://127.0.0.1:34113` | `ss -ltn 'sport = :34113'` | no listener | endpoint 200 + identity re-probed through round 14 (2026-09-29); refusal recorded at the round-13 re-dispatch (2026-10-15) |
| `/proc/1299/cmdline`, `~/.config/systemd/user/qwen-coder.service`, `~/.config/llama/qwen-coder-godspeed.jinja` | `test -e` | absent | process-level pin rounds 10–14 (pid 1299, 41-token argv EXACT_MATCH) |
| `~/Projects/bounties/ledger/telemetry.jsonl` | `test -e` (whole `~/Projects/bounties` tree absent) | absent | round 11 at 7,226 lines, live count 23:32Z 2026-09-29; went absent mid-round-11 |
| `~/Projects/the-bounty-hunter` | `test -e` | absent | recorded round 11 as existing-but-no-telemetry.jsonl; the tree itself is now gone |
| `~/.bailian/telemetry.jsonl`, `~/.bailian/wiki-sync-state.json` | `test -e` (whole `~/.bailian` absent) | absent | profiled 2026-09-28 (4,274-record digest) |
| `~/.bailian/skills/bailian-docs-llm-wiki/models/{index.md,models.jsonl}` | `test -e` (whole `~/.bailian` absent) | absent | read 2026-09-28 (Bailian model index digest) |
| `/tmp/bench-r{4,5,6,7,7-l2-executor}` run trees | `test -e` | absent (ephemeral by design) | graded runs of 2026-09-28; durable numbers are pasted in-entry per the evidence standard |
| HF + OpenRouter catalog endpoints | not probed this round (docs-reads-only policy) | unverified | probed 2026-09-28 (`knowledge/open-model-catalogs.md`) |

Nothing in this section is governed: these are historical sources whose
digests and receipts are retained in `corpus/`, not current dependencies.

Round-25 report-outs (evidence sent, not absorbed): (1) **kumitate** — the round-25 interval re-verdict
(`corpus/knowledge/attribution-interval-calibration.md`) bounds attribution accuracy on the shim's upstream
cascade legs over forced and natural P1 samples; its leg-share bounds are within-sample shares, never natural
fallback rates or OMP route-resolution facts, which stay kumitate's (`falsify/ConnKumitateReportOut.md`).
(2) **every citer of the r22 "hyper validated" reading** — that verdict is INDETERMINATE under the exact CP95 rule on
the registered population (`corpus/knowledge/attrib-r21.md` §Erratum round 25).

*Round-26 correction R26-E3 (appended 2026-10-21; supersedes the round-25 correction at `:119` "holds 37 after round 25"):
the registry holds **42** rows after round 25 — S001–S042; the `:119` sentence was written before S038–S042 landed
(`grep -cE '^\| *S[0-9]{3,} *\|' corpus/SOURCES.md` → 42 at `f11bffbf`; closure `corpus/lessons/round-25-verifier-spotcheck.md:103-104`).
The `:112` "25 rows" cell stays superseded by `:119` and this line.*

- **R26-E3a (2026-10-21)** supersedes `P3b.province.public-literature-registry.rows` — now `rows=42` (S001–S042 frozen round-25 population; count `SOURCES.md` ids ≤42, not future additions).
- **R26-E3b (2026-10-21)** supersedes `P3b.province.round25-correction.rows` — now `rows=42` (same dated population; `git show f11bffbf:corpus/SOURCES.md`).

Parser-format addendum: E3b's extra inline command is not a value token. The v3 exact-token restatement is:
- **R26-E7 (2026-10-21)** supersedes `P3b.province.round25-correction.rows` — now `rows=42`
- **R26-E8 (2026-10-21)** supersedes `P3b.province.public-literature-registry.rows` — now `rows=42`

Exact-ID-set addendum (2026-10-21): Amendment 1's census also verifies the complete S001–S042 identity set.
E7/E8's count-only restatements omit that new token; FxP3BInstruments caught the omission before entry admission.
- **R26-E9 (2026-10-21)** supersedes `P3b.province.round25-correction.rows` — now `rows=42` `id_set=exact`
- **R26-E10 (2026-10-21)** supersedes `P3b.province.public-literature-registry.rows` — now `rows=42` `id_set=exact`

## Round28 partial frontier admission (2026-10-21)

**Core addition:** pinned WebArena task-spec/scorer observability, via
`plans/benchmark_spec_audit.py` and `corpus/knowledge/webarena-task-spec-audit.md`.
This owns static LLM-evaluation interpretation, not the benchmark's web properties or runtime services.
**Calibration addition:** `plans/registry_check.py`, a bounded frozen13-row/35-path literal-reference
diagnostic, not semantic source truth or a whole-current-tree assertion census.

The task-spec frontier is only partly advanced: named Terminal-Bench/Toolathlon/SWE-bench Pro specs,
generated configs, runtime task validity, hosted judges and contamination remain open. Serving-plane
restoration stays operator/kama-owned. Existing historical absent surfaces are not restored or re-scored.

## Round29 partial frontier admission (2026-10-21)

**Core addition:** an offline, source-faithful projection of the pinned WebArena generator
(`scripts/generate_test_data.py` at dce04686) over the 812 raw tasks × 3 synthetic `*.invalid` profiles,
via `plans/config_projection.py` and `corpus/knowledge/webarena-config-projection.md`. This owns static
interpretation of how generated eval configs are derived, not the benchmark's sites, env_config values or
any deployment. Actual env_config-derived/deployment configs, runtime task validity, hosted judges and
contamination remain open. The round28 gap line above stays as written; this paragraph narrows it.

## Round29 attempt-2 partial frontier admission (2026-10-25)

**Core addition:** the published task-validity instruments a benchmark maintainer runs on its own
tasks, read from primary documents at pinned revisions, via
`corpus/knowledge/benchmark-task-validity-checklist.md` (S077–S080, S090). This owns reading
published maintainer artefacts; it does not run a benchmark, certify a task, or own deployment
configuration, runtime task validity, hosted judges, contamination measurement or any benchmark's
web properties. The attempt-1 paragraph above stays as written; this paragraph narrows only the
"unopened leads" phrase for Terminal-Bench 2.0, SWE-bench Pro V2 and Toolathlon-Verified, which are
now opened.

**Operability addition:** `plans/sources_adopt.py` — a pre-append gate for registry adoption (id
collisions under the census's own 0–3-space anchor, staged-row schema, prose-`recheck`
normalization, `used-by` projection) with a ten-case selftest — and `plans/adoption_check.py`, the
one-command counter for an adoption round. Both are lane-local and compose with the fleet census,
which remains the registry's authority; neither replaces it.

## Round35 partial frontier admission (2026-10-25)

**Core addition:** static interpretation and offline synthetic-fixture execution of one pinned
Terminal-Bench 2.0 grader function — `protein-assembly/tests/test_outputs.py::test_gblock` at
terminal-bench-2 `2fd12b88` — via `corpus/knowledge/tb2-protein-assembly-grader.md` (S105–S107) and
`plans/tb2_grader_probe.py`. This records how the captured function responds to lane-authored inputs
only; it does not run Terminal-Bench or the task image, validate or certify the task or any real
submission, establish biological correctness or the literals' correctness, or measure model
performance. Runtime task validity, hosted judges, contamination and the other 88 TB2 tasks' scoring
code stay open. The round29 attempt-2 paragraph above stays as written; this paragraph narrows only
the Terminal-Bench 2.0 scoring-code clause for this one task.

## Round36 partial frontier admission (2026-10-25)

**Core addition:** offline execution of one more pinned Terminal-Bench 2.0 grader —
`regex-log/tests/test_outputs.py::test_regex_matches_dates` at terminal-bench-2 `2fd12b88` — over 24
frozen `/app/regex.txt` candidates, via `corpus/knowledge/tb2-regex-log-grader.md` (S108–S110),
`plans/regex_log_probe.py` and receipt `corpus/evidence/round36/regex-log-probe.txt` (`cases=24
observed_pass=8 observed_fail=16 mismatches=0`); the graded artefact is an agent-authored regex file,
run against the grader's fixed 25-line log. It records how that captured grader answers synthetic
patterns only: it does not run Terminal-Bench, the task image or a real submission, validate or
certify a task, establish which pattern the instruction demands, measure model or agent performance,
observe hidden or held-out tests, or speak for any other TB2 task. Adjacent: verification-fixture
craft (tameshi), research method (chousa), prompt craft (kotoba) and seat arrangement (kumitate) stay
theirs; pattern text is data. The round35 paragraph above stays as written; this paragraph narrows
only its "other 88 TB2 tasks" clause for this one task.

**Reported out:** nothing absorbed — `plans/pkg_gate.py` stays this lane's own gate (tameshi owns the reusable fixture/mutation method and never edits a sibling's gate, `tameshi-shokunin/PROVINCE.md:3,14-17,44-45`); capture and citation method stay chousa's (`chousa-shokunin/PROVINCE.md:5-7,10-11`); prompt/skill wording stays kotoba's (`kotoba-shokunin/PROVINCE.md:61`); seat arrangement, not evaluation, stays kumitate's (`kumitate-shokunin/PROVINCE.md:23,28`).
