# kengaku-shokunin — Province

**Domain:** LLM/model research & evaluation — scopes ~/Projects/webzites/repos/llm-wiki, route telemetry

**Owns:** the domain knowledge, playbooks, error patterns, and checklists above.
**Refuses:** anything outside this domain; report cross-domain evidence back to the orchestrator rather than absorbing it.

## Surfaces (re-verified round 14, 2026-09-29; route telemetry absent; benchmark battery relocated — see rows)

| Surface | Path / endpoint | What this lane does with it |
|---|---|---|
| Research notes (SSOT for eval craft) | `~/Projects/webzites/repos/llm-wiki` — `wiki/ai/agents-and-engineering/`, `wiki/karpathy/`, `wiki/ai/{foundations,alignment-and-training,books,scaling-and-forecasting}/`, `Home.md`, `raw/` | digest into `corpus/knowledge/eval-*` entries; the `~/wikillm/llm-wiki` path does **not** exist here (`test -e` → absent) |
| Local benchmark battery | `~/archive/bench-arena/` — relocated intact from `~/bench-arena/` during round 14; `tasks/`, `grade.sh`, `loop.sh`, `report-grok45.csv`, `report-qwenlocal*.csv`, `telemetry-qwenlocal-v2.csv` all resolve at the archive path | authored runs, status-flip and truncation taxonomy; content no-drift (0 files newer than 2026-09-28), but historical commands using the old path are frozen evidence |
| Served local model | `http://127.0.0.1:34113` — `/v1/models`, `/health`, `/v1/chat/completions` (Qwen3-Coder-30B-A3B-Instruct **UD-IQ2_XXS**, `owned_by=llamacpp`, `n_ctx=16384`). **Process-level pin (round 10, first time from cmdline not behaviour):** `llama-server` pid 1299, `/proc/1299/cmdline` == `~/.config/systemd/user/qwen-coder.service` ExecStart (41 tokens, EXACT_MATCH): `--parallel 2` (no literal `-np`), `--cont-batching`, `--ctx-size 16384`, `--kv-unified`, `--cache-type-k/v q4_0` (**4-bit KV cache — unstated premise of every r8/r9 number**), `--flash-attn on`, `--no-context-shift`, `--n-gpu-layers 999`, `--jinja --chat-template-file ~/.config/llama/qwen-coder-godspeed.jinja` (custom non-upstream template). Evidence: `corpus/evidence/round10-fleet/r10-scout-endpoint.md` + raw captures `models-34113.json`, `props.json`, `slots.json`; identity re-probed via `/v1/models` + `/health` 200 each round | every probe in `corpus/evidence/`; identity re-probed each round; hermetic gates pin committed bytes, never `/proc` |
| Route telemetry | `~/Projects/bounties/ledger/telemetry.jsonl` — **ABSENT**, reconfirmed round 14 (last resolved round 11 at 7,226 lines; no relocation under `~/Projects`, `~/archive`, or Trash) | model×lane and reroute-chain **historical inference about model service** only; never treat the path as live |
| Client CLI telemetry | `~/.bailian/telemetry.jsonl`, `~/.bailian/wiki-sync-state.json` | quota-vs-auth failure split, poll-verb rule |
| Model catalogs | `~/.bailian/skills/bailian-docs-llm-wiki/models/{index.md,models.jsonl}`, `https://huggingface.co/api/models`, `https://openrouter.ai/api/v1/models` | selection fields, open-weight twins |
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
