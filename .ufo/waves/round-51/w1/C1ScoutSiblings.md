# C1ScoutSiblings — sibling surfaces kengaku's PROVINCE still declares

Seat: C1ScoutSiblings (scout). Axis judged: freshness. Feeds the C2 owner map. Read-only. No production edit.

## Axes

1. Quote pair — every overlap carries the sibling PROVINCE line and the kengaku PROVINCE line.
2. Self-claim vs attribution — a sibling owns a surface only when that sibling's PROVINCE says so. Kengaku naming the sibling is attribution, not proof.
3. Surface identity — path, port, or endpoint class, not the lane name alone.
4. Non-absorption — no sibling file edited; scratch removed before yield.

## Revision measured

Working trees, `git status --porcelain -- PROVINCE.md` empty on all five. Kengaku stage-1 freeze `e07f131cf7037e58a21db6e1f3986cf401ad257c` is an ancestor of HEAD, and `git diff --stat e07f131cf7037e58a21db6e1f3986cf401ad257c HEAD -- PROVINCE.md` is empty, so the kengaku lines below are the frozen bytes.

REV 4090c3db79d11279ab5e5121ba25e74aa316e6e7

| lane | HEAD | PROVINCE last touched |
|---|---|---|
| kengaku | `4090c3db79d11279ab5e5121ba25e74aa316e6e7` | `e9d201455c3774921aa5dfc287f07b4b9f113e76` (2026-10-27) |
| kama | `7ee8cbdf160f8c945954e4737e7a2f797e3b2987` | `dc48ee2e9f454b9caf986d14cf81bbc5be28cae1` |
| kasegi | `dbd2e106e35ac5ad14ea80f4c634d3fbf11853fb` | `857cac442862798d6bb33d5782290aad7f943301` |
| kumitate | `14057f3e3899180c95713bace088fb9c0d0046e3` | `76bdda4bde02522829598c1c81f1836ffbea8d34` |
| kotoba | `47dbe8781657de563ff867caca6244d28e3db504` | `a597a15da200d1b3be38b0e1b567c9944c5ecb00` |

Claims base `297e17927ba9342a87ba27a48cc5270a001de7cb` is also an ancestor. No tool installed.

## Commands

```text
git -C <lane> rev-parse HEAD
git -C <lane> status --porcelain -- PROVINCE.md
git -C <lane> log -1 --format='%H %ci %s' -- PROVINCE.md
git -C kengaku-shokunin diff --stat e07f131cf7037e58a21db6e1f3986cf401ad257c HEAD -- PROVINCE.md
git -C kengaku-shokunin merge-base --is-ancestor e07f131cf7037e58a21db6e1f3986cf401ad257c HEAD
git -C kumitate-shokunin show 2ca91a0c81542cad5f731049aa55dd2f99ade98d:PROVINCE.md
```

Keyword grep of the four sibling `PROVINCE.md` files for `8791`, `ds-flash`, `telemetry.jsonl`, `mission-state`, `route resolution`, `godspeed.jinja`: no matches.

## 1. Serving plane and endpoint identity — kama owns them

Kama's own province claims the class and the concrete unit kengaku still lists as a surface.

Sibling (`kama-shokunin/PROVINCE.md:3-4`):

> **Domain:** local model serving & endpoint health — local LLM endpoints, baseURL drift, served-model reconciliation, probe conventions.

Sibling (`kama-shokunin/PROVINCE.md:10`):

> producer discovery & read-only service inspection of local serving ports … The serving unit formerly pinned here — `~/.config/systemd/user/qwen-coder.service` (llama-server, `127.0.0.1:34113`) — is deleted; row-absent since snapshot `20261014T124232Z` … kama governs discovering whatever serves these ports and never claims an installed server

Sibling (`kama-shokunin/PROVINCE.md:12-13`):

> served-model-id reconciliation | `GET /v1/models` vs `--alias` vs the configured model id
> liveness/readiness probe conventions | `/health`, `/props`, `/slots`

Sibling (`kama-shokunin/PROVINCE.md:42-45`):

> **Refuses:** model quality/eval (kengaku), credential material & auth flows (kagi), dispatch/route mechanism (kumitate), remote web surfaces (kake). Boundary rule: kama answers *"is the thing at this baseURL the model this config believes it is, right now"* — never *"is the model good"* or *"is the request safe"*.

Sibling (`kama-shokunin/PROVINCE.md:27-31`, same unit, liveness separate from identity):

> nothing listens on `8080` or `34113` … restoring a unit is operator-owned work … server/health discovery and drift reconciliation remain governed here

Sibling (`kama-shokunin/PROVINCE.md:131-144`) holds the `/v1/chat/completions` conversion layer on the lane-owned fixture and records that kengaku excludes the model-serving plane.

Kengaku (`PROVINCE.md:14`, surfaces row SF03):

> | Served local model | `http://127.0.0.1:34113` — `/v1/models`, `/health`, `/v1/chat/completions` … `llama-server` pid 1299, `/proc/1299/cmdline` == `~/.config/systemd/user/qwen-coder.service` ExecStart … identity re-probed via `/v1/models` + `/health` 200 each round | … **ABSENT 2026-10-20**

Kengaku (`PROVINCE.md:156-157`, historical, same artifacts):

> | `http://127.0.0.1:34113` | `ss -ltn 'sport = :34113'` | no listener | …
> | `/proc/1299/cmdline`, `~/.config/systemd/user/qwen-coder.service`, `~/.config/llama/qwen-coder-godspeed.jinja` | `test -e` | absent | …

Kengaku (`PROVINCE.md:136`, later adjacent row, agrees with kama):

> | **kama** | serving plane + endpoint identity — … kama is rostered and owns serving-plane health/detection and endpoint identity; kengaku keeps *interpretation* evidence and never remediates flags (`--kv-unified`, q4_0 KV, `--parallel`) — flag-change authority is unowned/integrator |

Kengaku (`PROVINCE.md:24-25`, earlier refusal, contradicts both kama and line 136):

> - **Not owned:** the model-serving plane (llama-server flags, slot/batch config) — no lane owns it; escalate to the integrator instead of remediating.

Owner-map reading: the `:34113` identity probes (`/v1/models`, `/health`, `/props`, `/slots`) and the deleted `qwen-coder.service` unit are kama's surfaces. Kengaku's kept piece is interpretation of eval numbers, which kama refuses. Line 24's "no lane owns it" is the stale sentence; line 136 is the one that matches kama. Flag-change and unit restore stay operator/integrator on both sides (kama "never claims an installed server"; kengaku "flag-change authority is unowned/integrator"). The jinja path is named only by kengaku:14 and :157. Neither kama nor kotoba names `godspeed.jinja`.

`:8791` is not a kama-named artifact. Kengaku (`PROVINCE.md:114`):

> | Live probe endpoint | `ss -ltn 'sport = :8791'` | LISTEN on `127.0.0.1:8791` (ds-flash-shim, read-only shim; `:8793` not probed this round) |

Kama owns the class "whatever serves these ports" (`PROVINCE.md:10`) and does not name `:8791` or `ds-flash-shim`. Do not attribute that row to kama as a declared artifact.

## 2. Route telemetry and mission state — kasegi owns the scope root, not those words

Sibling (`kasegi-shokunin/PROVINCE.md:3`):

> **Domain:** bounty & security research — scopes ~/Projects/bounties, program rules, claim packages

Sibling (`kasegi-shokunin/PROVINCE.md:6-9`):

> `~/Projects/bounties` was removed from the filesystem at 2026-09-28T23:51:31Z … The domain is unchanged — bounty & security research, program rules, claim packages

Sibling (`kasegi-shokunin/PROVINCE.md:16-22`):

> Both surviving roots named above are now ABSENT — `~/Projects/the-bounty-hunter` and the whole `~/Projects/origin-work` tree disappeared on/around 2026-10-12 … coverage claims against the absent trees are corpus-attested records, not live-openable.

Sibling (`kasegi-shokunin/PROVINCE.md:29-30`):

> The line-3 domain comprises program rules, scopes, and claim packages; the core also covers triage and claim gates, and submission/disclosure packaging.

Kengaku (`PROVINCE.md:3`):

> **Domain:** LLM/model research & evaluation — scopes ~/Projects/webzites/repos/llm-wiki, route telemetry

Kengaku (`PROVINCE.md:15`, surfaces row SF04):

> | Route telemetry | `~/Projects/bounties/ledger/telemetry.jsonl` — **ABSENT**, reconfirmed round 14 … | model×lane and reroute-chain **historical inference about model service** only; never treat the path as live |

Kengaku (`PROVINCE.md:29` and `:142`):

> - **kasegi:** bounty ledger mission-state / dispatcher semantics.
> | **kasegi** | bounty-ledger mission-state / dispatcher semantics — plus the round-11 report that `~/Projects/bounties/` went absent operator-side |

Kengaku (`PROVINCE.md:74-80`):

> (4) **kasegi** — the bounty-ledger tree `~/Projects/bounties/` (their namesake surface, incl. `ledger/telemetry.jsonl`) went absent from this host mid-round-11; last observed resolving 23:32Z (`corpus/lessons/round-8-aggregator-box3-coldrun.md` command 3, live count 7,226). … `~/Projects/the-bounty-hunter/` exists but carries no `ledger/telemetry.jsonl`.

Kengaku (`PROVINCE.md:158-159`) repeats the absent path and says the live count was 23:32Z 2026-09-29, and that `~/Projects/the-bounty-hunter` is now gone.

Owner-map reading: the path overlap is real — `ledger/telemetry.jsonl` sits under the root kasegi scopes. The labels "route telemetry", "mission-state", and "dispatcher semantics" appear only on kengaku's side. Kasegi's PROVINCE does not contain `telemetry`, `mission-state`, or `dispatcher`. What kasegi claims there is bounty program rules, claim packages, triage, and disclosure. Both provinces record the tree absent. The clocks do not match and were not re-measured: kasegi says removed `2026-09-28T23:51:31Z`; kengaku says last live `23:32Z 2026-09-29`. Kengaku:79 still says `the-bounty-hunter` exists; kasegi:16-22 and kengaku:159 say it is gone. SF05 `~/.bailian/telemetry.jsonl` is not named by any of these four provinces.

## 3. OMP route resolution — kumitate owns OMP task/hub, not that phrase

Sibling (`kumitate-shokunin/PROVINCE.md:3`):

> **Domain:** orchestration & tooling — scopes OMP task/hub, ufo-fsd scripts & runtime

Sibling (`kumitate-shokunin/PROVINCE.md:19`, frontier, not core):

> - OMP harness contract (task batch, agent hub, agent discovery) — first entry `corpus/knowledge/omp-task-contract.md` (round 34); …

Sibling (`kumitate-shokunin/PROVINCE.md:23`, frontier):

> - Durable-execution and multi-agent failure research (idempotency, timeouts, failure taxonomies) — …

That band is broker and workflow failure (delivery identity, redelivery budgets, visibility leases, heartbeats, sagas). It does not name bench-arena `telemetry_source` or OMP route fallback.

Sibling (`kumitate-shokunin/PROVINCE.md:24`):

> adjacent, not absorbed: kengaku evaluates agents, this lane arranges the seats around that judgment

Sibling (`kumitate-shokunin/PROVINCE.md:29` at HEAD `14057f3e`; line 28 at the pin kotoba cites, `2ca91a0c`):

> - Local model serving and endpoints → kama. Prompt and skill craft → kotoba. Research method → chousa.

A second sibling attributes route mechanism to kumitate without kumitate saying it. Kama (`PROVINCE.md:43`): `dispatch/route mechanism (kumitate)`.

Kengaku (`PROVINCE.md:27-28` and `:141`):

> - **kumitate:** OMP route resolution, fallback policy, operational failure taxonomy.
> | **kumitate** | OMP route resolution, fallback policy, operational failure taxonomy (`loop.sh` telemetry-source semantics, informational) |

Kengaku (`PROVINCE.md:48-53`): the bench-arena `loop.sh` bug forces `telemetry_source=journal`, and "the resulting telemetry-source semantics touch the operational failure taxonomy kumitate owns".

Kengaku (`PROVINCE.md:168-171`): interval leg-share bounds "are within-sample shares, never natural fallback rates or OMP route-resolution facts, which stay kumitate's".

Owner-map reading: partial. Kumitate self-claims OMP task/hub, the OMP harness contract, and a durable-execution failure-taxonomy research band, and it routes serving to kama and prompt craft to kotoba. It does not self-claim "OMP route resolution", "fallback policy", or `loop.sh` telemetry-source semantics. Those three strings are kengaku's attribution (kama adds "dispatch/route mechanism"). Do not copy kengaku:27 into the owner field as if kumitate's PROVINCE said it.

## 4. Prompt craft — kotoba owns it; kengaku keeps the measurement

Sibling (`kotoba-shokunin/PROVINCE.md:3`):

> **Domain:** prompt & skill craft — scopes SKILL.md/AGENTS.md quality, trigger fidelity

Sibling (`kotoba-shokunin/PROVINCE.md:12-13`):

> - `SKILL.md` — trigger/frontmatter craft, anatomy and compression, decision tables, the four fidelity checklists …
> - Agent-definition, always-on (AGENTS.md-class) and dispatch-prompt craft — …

Sibling (`kotoba-shokunin/PROVINCE.md:66`), quoting kengaku back:

> kengaku owns measured capability effects of prompt format and hands reusable craft out; kotoba owns the prompt/skill craft rules (kengaku SKILL.md:3, PROVINCE.md:30-32,138)

Sibling (`kotoba-shokunin/PROVINCE.md:64`):

> kama owns local model-serving endpoint identity and health (SKILL.md:8-9); … kotoba owns instruction text, kama verifies the endpoint.

Kengaku (`PROVINCE.md:30-32`):

> - **kotoba:** prompt- and skill-craft rules, render/trigger behaviour — this lane keeps the *measured* effect of prompt format on capability and hands the reusable craft implication out.

Kengaku (`PROVINCE.md:138`):

> | **kotoba** | prompt- and skill-craft rules — measured capability effects of prompt format stay here; reusable craft implications route out (r7 tools-without-system, r11/r12 ack-intent findings) |

Owner-map reading: agreed split, not a contested path. No kengaku surface-table row is a prompt-craft artifact kotoba also names. The jinja file inside SF03 stays unnamed by kotoba. Kotoba's citation of kumitate `PROVINCE.md:28` is correct at pin `2ca91a0c`; at kumitate HEAD the same sentence is line 29.

## What not to attribute

| kengaku surface | sibling self-claim |
|---|---|
| SF03 `:34113` `/v1/models` `/health` `/props` `/slots` and `qwen-coder.service` | kama, yes |
| SF03 flag-change / unit restore | neither; both say operator or integrator |
| Core `:8791` ds-flash-shim | no sibling names it; kama owns the port class only |
| `qwen-coder-godspeed.jinja` | no sibling names it |
| SF04 `~/Projects/bounties/ledger/telemetry.jsonl` | path is inside kasegi's scope root; the telemetry/mission/dispatcher wording is not kasegi's |
| SF05 `~/.bailian/telemetry.jsonl` | none of the four |
| "OMP route resolution, fallback policy" | not a kumitate sentence; OMP task/hub and harness contract are |
| prompt/skill craft rules | kotoba, yes; kengaku keeps measured effect |

## Limits

- Ownership is taken only from each lane's `PROVINCE.md`. A `SKILL.md` or corpus file was not opened to widen a claim. Lines that cite another file are quoted as citations, not re-verified.
- Ports and home paths were not re-probed. Absence dates are the provinces' own sentences.
- Grep-absence of `telemetry` / `mission-state` / `route resolution` / `8791` / `ds-flash` / `godspeed.jinja` is over these four files only.
- Kotoba's adjacent-table commits are older pins than today's sibling HEADs. The kumitate 28→29 shift is the one line re-checked.

Scratch `/fast/scratch/hyaku/kengaku-r51/C1ScoutSiblings` held only `TMPDIR`. No clone. Removed before yield.

VERDICT: kama owns the serving-plane and endpoint-identity surfaces kengaku still declares at :34113; kasegi owns the ~/Projects/bounties root under that telemetry path but not mission-state or dispatcher wording; kumitate owns OMP task/hub, not the phrase "route resolution / fallback policy"; kotoba owns prompt and skill craft and both provinces leave measured prompt effects with kengaku.
