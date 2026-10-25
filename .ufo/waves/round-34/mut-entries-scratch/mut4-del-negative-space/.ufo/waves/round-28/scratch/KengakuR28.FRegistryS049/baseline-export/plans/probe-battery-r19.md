# Round-19 probe battery — live model-route calibration (kengaku-shokunin)

**status: DRAFT — predictions NOT frozen.**
Runners: do **not** send any request until §7 carries a `FROZEN:` line.
The prediction-registrar freezes; the registrar gatekeeps the ordering audit.

- drafted-by: battery-author seat, round-19 flash wave (zai-bucket lane)
- drafted_utc: 2026-10-16T07:44:09Z
- write-scope: this file only (`plans/probe-battery-r19.md`)
- request-budget: **≤20 HTTP requests total, ≤256 output tokens**, one attempt per probe, strictly sequential
- battery-author network state at draft time: **zero HTTP requests issued to any probe target**. The only host reads were `date -u` and one `ss -ltn` listener enumeration at 2026-10-16T07:40:22Z (socket state, no HTTP). Disclosure: that socket check showed no listener on `127.0.0.1:34113`, which P9 predicts on; no other probe's predicted event was observed or exercised before this draft.

## 0. Falsifiable claim (before → after)

**Before** (pre-registered for this round): the lane's calibration proxy — probes with
predictions filed *before the first request*, scored at close — ran **0/1, 1/1, 0/0, 1/1**
across rounds 8–11: intermittent and ad hoc; **no standing battery or reusable template
exists**. Evidence: `SCORECARD.md:34-37` (proxy (a) definition and the r8–r11 counts);
`SCORECARD.md:163` (r12 filed predictions before its first request — `ordering.log`
01:16:08Z < first `request_ts` 01:19:59Z — but scored and landed only in r14, breaching
the proxy's in-round clause); the SCORECARD move log's last row is round 16
(`SCORECARD.md:367`) and the round-18 land is a parent-fleet digest
(`corpus/knowledge/kimi-model-routing-round18.md`), not a lane-run scored battery;
`ls plans/` at 2026-10-16T07:44:09Z shows only `wwkd-round-16-recensus.md` and
`wwkd-round-17-coverage.md` — no battery, no template.

**After** (this file): a frozen battery of **9 falsifiable live-route probes** (19 HTTP
requests, ≤240 output tokens), predictions in §6 hashed with UTC **before any request**
(§7 procedure), each executed with receipts (UTC / exact command / exit / response
excerpt, redacted) in `corpus/evidence/probe-r19-*.log`, scored at close (Brier /
abs-error / range-hit / pass-fail) with an aggregate calibration read (§4). Timestamp
ordering is audited: no outcome may precede its prediction; a breach is recorded, never
patched. The freeze hash covers §0–§6 **as of the freeze instant** (§7 step 6); §0's
revision note below records pre-freeze edits only.

Revisions (append-only, pre-freeze): **v2 2026-10-16T07:52:30Z** — P4/P5 re-based and
P7 disclosure added after runner-seat receipts revealed the operator's post-r18
cascade leg reorders (M7/M9, devin leg out of ds; glm shim now zai-first). The freeze
hash covers the re-based battery; pre-freeze edits are part of the hashed bundle.

## 1. Provenance — every probe from a round-18 receipt

Each probe cites the concrete finding it tests. Primary sources: the round-18 digest
`corpus/knowledge/kimi-model-routing-round18.md` (R18 digest below) and the parent
trees it digests (`../research/round-18-kimi-model-routing/`, merge commits `4738fee`
census, `7e2c473` definitions, `c2174a5` battery, `db82042` fastmode, `bd0c690`
battery-opencode, `fbae972` routing — verified in
`corpus/evidence/round18-kimi-routing/README.md:8-12`). The ledger-telemetry land
(`corpus/knowledge/ledger-route-telemetry.md:60-62`, falsifiable claim 2: *usage_limit
causes are provider-meter events, not model failures*) sets P1's scoring frame: a 429
here is a meter state, not a model-quality signal.

Endpoints below are the fleet's already-configured routes: the six localhost shims
(census `ANALYSIS.md:30-38`, units `devin/cursor/codex/xai/ds-flash/glm-flash-shim`,
ports 8787/8788/8789/8790/8791/8793) and the provider lanes the fleet already uses
(base_urls read from the redacted census `manifest.json` — api_key values are NOT in
that file; only presence/length/digest, `manifest.json:7`). Battery-author verified at
2026-10-16T07:40:22Z that all six shim ports have live listeners (`ss -ltn`; socket
state only). No credential file was opened by battery-author; §2 binds runners to the
same discipline.

## 2. Binding rules for runners

1. **Wait for the freeze.** Poll this file (`sleep 30`) until §7 has a `FROZEN:` line.
   Record the file's frozen hash before your first request (§7 step 5) and put it in
   your log header.
2. **Credentials.** Never read, copy, print, or persist a credential value. Load
   provider credentials at runtime, inside the runner process, from the fleet's
   configured client config, exactly the way the r18 census scripts do
   (`census/ANALYSIS.md:228` — "reads credentials from the config at runtime and passes
   them only into request headers"; values only ever as sha256 digests or length
   markers in captures). Logs carry header **names** and redaction markers only. If
   your seat judges runtime config access out of scope, mark the probe `UNRUN` with the
   reason — do not improvise an auth path.
3. **One attempt per probe.** No retries on HTTP status responses. A single retry is
   allowed only for connection-level failures (timeout / connection refused), and it
   counts against the ≤20-request budget. A 429/401 response **ends** that probe —
   dead lanes get exactly one confirming call, no hammering.
4. **Sequential, ≥2 s between any two requests to the same upstream host.** No
   concurrency anywhere.
5. **Stop conditions.** Two consecutive transport failures on the same lane, or any 5xx,
   end that probe and are recorded as its outcome class. Never widen the request set:
   the ≤20-request enumerated list is the whole budget.
6. **Write discipline.** Runner logs go to `corpus/evidence/probe-r19-*.log` only.
   Scratch (SSE captures) goes to `/tmp`; on `EDQUOT` use `$HOME/.cache/kengaku-tmp`
   and **delete it when done**.
7. **No git commits.** The parent integrates under the kengaku lane identity.
8. **No scalar axis verdicts** anywhere in any artifact this battery produces. Probe
   and aggregate results are measurements.

## 3. The probes

Shared request bodies. `COUNT_PROMPT` =
`Count from 1 to 30, space separated, numbers only. No other text.` (the r18 census
stream prompt, `census/ANALYSIS.md:184` — using it keeps predictions transferable to
the r18 numbers). OpenAI-protocol streaming calls set
`"stream": true, "stream_options": {"include_usage": true}` (the M6 body shape,
`battery-opencode/ANALYSIS.md:24-26`). If a lane 400s naming `stream_options`, record
that as the outcome; usage components score UNPROVABLE — no reshaped retry.

### P1 — quota-dead token-plan keys stay dead past 2026-10-16 (meter state, not model state)

- **Hypothesis (falsifiable):** `alibaba-token-plan-2` and `alibaba-token-plan-3` are
  still quota-exhausted on 2026-10-16 — one minimal chat each returns HTTP 429
  `insufficient_quota` whose `retry-after` matches the r18-stated resets (key 2 →
  2026-10-23T16:00:00Z, key 3 → 2026-10-28T16:00:00Z, each ±7200 s) — while
  `GET /models` still answers 200 on both keys (an endpoint listing is not evidence of
  usable quota).
- **Source:** R18 digest `:109-113` (D2; resets stated; `/models` 200 on dead keys);
  `census/ANALYSIS.md:86-90` (`retry-after` 707432 / 1139431 observed 2026-10-15 —
  consistent with the same reset anchors).
- **Requests (4):** for each key K ∈ {2,3}: (i) `POST
  https://token-plan.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1/chat/completions`
  with key K's configured credential, body `{"model":"deepseek-v4.1-flash",
  "messages":[{"role":"user","content":"ping"}],"max_tokens":8,"temperature":0,
  "stream":false}`; (ii) `GET
  https://token-plan.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1/models` with
  the same credential.
- **Predictions:** components 1a–1f in §6. Numeric anchor: implied reset =
  `request_epoch + retry_after`; nominal at a 2026-10-16T09:00Z run ≈ 630,000 s (key 2)
  and ≈ 1,062,000 s (key 3).
- **Scoring:** Brier on binaries (1a, 1b, 1e, 1f); abs-error on implied-reset offset
  (1c, 1d, target 0, tolerance ±7200 s counts as range-hit).
- **Frame:** per `ledger-route-telemetry.md:60-62`, a 429 here is a provider-meter
  event, not a model failure; it is scored as a route-state prediction only.

### P2 — codex `service_tier` acceptance set reproduces (priority in, everything else out)

- **Hypothesis (falsifiable):** the M5 acceptance verdict reproduces on 2026-10-16:
  on `POST http://127.0.0.1:8789/backend-api/codex/responses` with the D6-minimal
  shape, `service_tier` values `omit/default/priority` return 200 and
  `flex/fast/auto/<invalid>` return 400 `Unsupported service_tier: <value>`.
- **Source:** R18 digest `:166-176` (M5 no-go; "`priority` is accepted (200) while
  `flex`/`fast`/`auto`/an invalid control all return 400"); `fastmode/ANALYSIS.md:122-131`
  (acceptance table, reproduced byte-for-byte across two runs).
- **Requests (7):** seven minimal POSTs, body exactly the M5 `build_body` shape —
  `{"model":"gpt-6.1-sol","stream":true,"store":false,"max_output_tokens":16,
  "input":[{"type":"message","role":"user","content":[{"type":"input_text",
  "text":"ping"}]}]}` — plus patch `service_tier` ∈ {omit, "default", "flex",
  "priority", "fast", "auto", "r19-invalid-tier"}. Runner: copy the request/header
  construction verbatim from `fastmode/scripts/probe_fastmode.py:103-115` (hygiene
  gate: `fastmode/HYGIENE.md`, 0 hits); **do not run that script itself** — it spends
  its own full quota. Headers: the script's proven set, credential values loader-fed.
- **Predictions:** status vector `[200,200,400,200,400,400,400]` in the listed order
  (2a); all four 400 bodies name `Unsupported service_tier: <value>` (2b).
- **Scoring:** Brier on 2a, 2b. Rejections cost no output tokens; serviced legs ≤16
  tokens each.

### P3 — codex priority stays accepted-but-inert (echo + quota telemetry static)

- **Hypothesis (falsifiable):** on P2's three serviced responses, no signal
  distinguishes `priority` from `omit`/`default`: the final `service_tier` echo is
  `default` (never `priority`), `x-codex-credits-balance` is `62500.0000000000`,
  `x-codex-primary-used-percent` ≤ 2, and the usage `input_tokens` are identical across
  the three (same prompt, same billing).
- **Source:** `fastmode/ANALYSIS.md:184-195` (echo sequence `auto→…→default`,
  byte-identical for omit and priority), `:199-215` (static quota headers and usage
  table); R18 digest `:171-173`.
- **Requests (0 extra):** reads P2's captured responses.
- **Predictions:** components 3a–3d in §6.
- **Scoring:** Brier on 3a–3d.

### P4 — cascade leg order matches the operator's post-r18 reorder (both shims)

- **Hypothesis (falsifiable):** on 2026-10-16 the ds-flash cascade (:8791) serves
  leg-1 `alibaba-token-plan` (Aliyun `server: istio-envoy` signature, no
  `x-opencode-*` header) and the glm-flash cascade (:8793) reports legs
  `[zai, devin, hyper]` with its stream served by leg-1 zai — the operator's M7/M9
  reorders persisted overnight, replacing the r18 census order (ds: opencode-go
  first; glm: devin first).
- **Source:** `../research/round-18-kimi-model-routing/cascade-legorder/LEGORDER.md:20-21`
  (ds before/after legs) and `:107-127` (after-state verification: Aliyun signature,
  `leg=1/alibaba-token-plan OK` journal lines);
  `../research/round-18-kimi-model-routing/glm-flash-legorder/LEGORDER.md` (M9: the
  live glm shim WAS devin-first, now zai→devin→hyper, zai leg verified serving,
  `prompt_tokens=19`); R18 digest `:163-165` (the operator check this probes);
  runner seat-level predictions `corpus/evidence/probe-r19-shim-ds-predictions.log`
  (S1/S2/S6/S7 — the same ds claims at seat level, filed 07:43:30Z; the battery adds
  the glm leg and the drift framing).
- **Drift note:** the r18 D9 numbers (`census/ANALYSIS.md:134-144`: glm-flash 11734
  prompt_tokens with devin leg-1; ds 48 with opencode-go leg-1) describe the
  pre-reorder state. If 4a/4c hit, that drift is CONFIRMED as an operator
  serving-plane change — a routing-relevant fact, not a lane measurement error.
- **Requests (4):** (i) `POST http://127.0.0.1:8791/v1/chat/completions` non-stream,
  body `{"model":"deepseek-v4.1-flash","messages":[{"role":"user","content":"ping"}],
  "max_tokens":16,"temperature":0,"stream":false}`; (ii) same URL and body with
  `"stream":true,"stream_options":{"include_usage":true}` (≥2 s after (i)); (iii)
  `GET http://127.0.0.1:8793/health` (zero quota; the direct leg-order read); (iv)
  `POST http://127.0.0.1:8793/v1/chat/completions` stream, body
  `{"model":"glm-5.3-flash","messages":[{"role":"user","content":"COUNT_PROMPT"}],
  "max_tokens":16,"temperature":0,"stream":true,"stream_options":{"include_usage":true}}`
  (client timeout 320 s: glm leg-2 is devin, so D7's cold start applies only on
  failover). All shim api_keys via loader.
- **Predictions:** 4a (i) served by leg-1 alibaba-token-plan, p=0.90 (journal base
  rate 95.6% per `probe-r19-shim-ds-predictions.log` [JRNL]; residual = leg-1
  429/content-inspection at probe time); 4b (ii) same, p=0.90; 4c (iii) legs ==
  `["zai","devin","hyper"]`, p=0.85 (the /health endpoint is verified on the ds shim
  family, unverified on glm — if absent, 4c scores on (iv)'s response headers and
  the miss is an instrument miss, recorded as such); 4d (iv) served by leg-1 zai
  (z.ai signature / stream model echo `glm-5.3-flash`), p=0.90; 4e (i) wall time
  point 1.8 s, band [0.8, 4.0] (M7 1.360 s small-probe basis); 4f (iv) prompt_tokens
  point 30, range [15, 60] (census zai direct billed 30 for COUNT_PROMPT,
  `census/ANALYSIS.md:139`; M9's zai leg billed 19 on a shorter prompt).
- **Scoring:** Brier 4a–4d; 4e abs-error + band hit/miss; 4f abs-error + range
  hit/miss.

### P5 — cascade stream transport: burst vs incremental is a per-leg property

- **Hypothesis (falsifiable):** on the post-reorder shims, the ds-flash stream (leg-1
  alibaba-token-plan) delivers its deltas incrementally (first→last delta span ≥ 50 ms)
  while the glm-flash stream (leg-1 zai) delivers its deltas in one burst (span < 50 ms)
  — burst-vs-incremental follows the serving leg, not the cascade wrapper.
- **Source:** `census/ANALYSIS.md:189` (token-plan key-1 lane: incremental, 304 ms
  decode span) vs `:192` (zai direct: burst, 0 ms span); old-order cascade bursts
  (`:201-202`, pre-reorder); M9's leg-1 zai verification; the M3 burst rule
  (`battery/ANALYSIS.md:20`, <50 ms = burst).
- **Requests (0 extra):** timing read from P4's two streams.
- **Predictions:** 5a ds incremental (span ≥ 50 ms), p=0.85; 5b glm burst (span < 50
  ms), p=0.50 — the r18 corpus contradicts itself on zai's flush behavior (census
  burst at `census/ANALYSIS.md:192` vs M3 incremental 148.5/127.9 ms at
  `battery/ANALYSIS.md:31`), so the honest prior is a coin flip and the probe is
  designed to adjudicate it.
- **Scoring:** Brier 5a, 5b.

### P6 — the operator's zai flash lane answers and its first-token latency holds

- **Hypothesis (falsifiable):** one minimal streaming chat to
  `zai-coding-plan`/`glm-5.3-flash` (the operator's zai subscription lane; this wave's
  own routing bucket) returns 200 with a populated usage block, first-decoded-token
  TTFT in [1500, 6000] ms.
- **Source:** `census/ANALYSIS.md:55` (zai chat 200, 2159 ms) and `:192` (TTFT 3163 ms
  on COUNT_PROMPT, max_tokens 64, first-decoded basis); `battery/ANALYSIS.md:31`
  (same model id under the `-low` alias: 2796 ms, no content in a 256 budget —
  secondary basis).
- **Requests (1):** `POST https://api.z.ai/api/coding/paas/v4/chat/completions`, body
  `{"model":"glm-5.3-flash","messages":[{"role":"user","content":"COUNT_PROMPT"}],
  "max_tokens":64,"temperature":0,"stream":true,"stream_options":{"include_usage":true}}`.
- **Predictions:** 6a status 200; 6b usage with completion_tokens > 0; 6c first-decoded
  TTFT point 3000, range [1500, 6000] ms.
- **Scoring:** Brier 6a, 6b; abs-error + range hit/miss 6c.

### P7 — the verify-first add `opencode-go/deepseek-v4.1-flash` still serves as measured

- **Hypothesis (falsifiable):** with a browser-class User-Agent, one minimal streaming
  chat returns 200 (never the 403/`error code: 1010` Cloudflare wall a scripted agent
  gets), the stream `model` field echoes `deepseek-v4.1-flash` (no silent reroute),
  prompt_tokens ∈ [20, 120], first-decoded TTFT ∈ [1500, 6500] ms.
- **Source:** `battery-opencode/ANALYSIS.md:15` (UA class `browser-chrome-141-linux`;
  scripted UA → 403/1010), `:46-62` (reps: first-decoded 3356 ms, content 4958 ms;
  200 on 11/11), `:78-87` (headers `x-zen-model: deepseek-v4.1-flash`, no reroute;
  usage on all requests), `:119-121` (the cascade-proxy 2467 ms figure is DISQUALIFIED
  as a latency bound — buffered shim, not this lane's TTFT); R18 digest `:89` (M6 row)
  and `:149` (verify-first status).
- **Drafting-time disclosure:** runner-leg-opencode's accidental pre-run
  (`corpus/evidence/probe-r19-opencode-health.log`, DEFECT 0) observed this exact
  endpoint at 07:45:01–04Z — 200 on both requests, model echo correct, prompt_tokens
  38, zero content at a 16-token budget. Those bytes are the other seat's host-state
  observations, NOT scored battery outcomes; they are disclosed because they are
  drafting-time evidence bearing on 7a/7b/7c, and every observed value sits inside
  the predicted ranges.
- **Requests (1):** `POST https://opencode.ai/inference/go/v1/chat/completions`, body
  as P6 with `"model":"deepseek-v4.1-flash"`, header
  `User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)
  Chrome/141.0.0.0 Safari/537.36`, plus the lane's configured `x-opencode-session`
  header (loader-fed, name-only in logs).
- **Predictions:** 7a status 200; 7b model echo; 7c prompt_tokens point 45, range
  [20, 120] (basis: same lane family billed 30 for COUNT_PROMPT,
  `census/ANALYSIS.md:139`); 7d first-decoded TTFT point 4000, range [1500, 6500] ms
  (basis: M6 3356 ms; M6's own warning that its upstream routing could move the number
  is why the range is wide).
- **Scoring:** Brier 7a, 7b; abs-error + range hit/miss 7c, 7d.

### P8 — `managed:kimi-code` is still auth-dead (401, distinct from quota-dead)

- **Hypothesis (falsifiable):** `GET https://api.kimi.ai/coding/v1/models` with **no
  Authorization header** returns 401 with an auth-error body — the lane is auth-dead
  (empty OAuth store), a different failure class from P1's meter-dead keys.
- **Source:** R18 digest `:129-133` ("4 on `managed:kimi-code` (401 on every path;
  empty OAuth store; includes `default_model = kimi-code/kimi-for-coding`)");
  `census/ANALYSIS.md:80-84` (D1: 401 `invalid_authentication_error` / "Invalid
  Authentication" on every path; zero-byte token store).
- **Requests (1):** the GET above, no auth header, 5 s timeout. Zero quota spent.
- **Predictions:** 8a status 401; 8b body contains `invalid_authentication_error` or
  `Invalid Authentication`. A 200 falsifies (store repopulated); 404/5xx falsifies the
  route-shape part.
- **Scoring:** Brier 8a, 8b.

### P9 — the lane's local served model is still absent (`:34113`)

- **Hypothesis (falsifiable):** `GET http://127.0.0.1:34113/health` still fails with a
  connection error on 2026-10-16 — the surface declared absent stays absent, and its
  restore (if it ever happens) is caught by this standing battery rather than by
  accident.
- **Source:** `corpus/knowledge/bench-arena-fresh-run.md:11` (availability-evidence:
  `http://127.0.0.1:34113/health connection refused`, observed 2026-10-15T04:49:50Z);
  `PROVINCE.md:212-220` (round-15 sweep: no llama-server process, unit "could not be
  found", carried debt named). Disclosure: battery-author's `ss -ltn` at
  07:40:22Z showed no `:34113` listener — hence the honest-but-informed p=0.80.
- **Requests (1):** the GET above, 5 s timeout, e.g. `curl -sS -m 5 -o /dev/null -w
  '%{http_code} %{exitcode}' http://127.0.0.1:34113/health` (record curl's real exit).
- **Prediction:** 9a connection refused / timeout (curl exit 7 or 28, http 000). A 200
  (or any HTTP status) falsifies and is a **freshness event**: report it to the
  integrator instead of absorbing a re-pin.
- **Scoring:** Brier 9a.

## 4. Scoring at close (scorer contract → `corpus/knowledge/probe-battery-r19.md`)

1. **Ordering gate (pass/fail for the whole battery):** for every runner log, verify
   `frozen_utc < first_request_utc` and `battery_sha256_at_start ==` the §7 hash. Any
   violation = `ORDERING-BREACH`: the affected outcomes are excluded from the
   calibration aggregate and the breach is recorded. This gate implements "no outcome
   may precede its prediction".
2. **Per-component scores.** Binary components: Brier `(p − o)²` with o ∈ {0,1}.
   Numeric components: signed abs-error and range hit/miss. Components whose probe
   ended UNRUN / TRANSPORT-UNREACHABLE are UNPROVABLE: excluded from denominators,
   listed with reasons (the M3 "unprovable" idiom, `battery/predictions/PREDICTIONS.md:41-43`).
3. **Per-probe verdict:** PASS iff every scored component hit its prediction
   (binary outcome on the >0.5 side; numeric inside range); otherwise FAIL with the
   signed misses shown. A probe is neither pass nor fail when UNPROVABLE.
4. **Aggregate calibration read (measurements, not axis scores):** (i) mean Brier over
   all scored binary components, with the always-0.5 reference (0.25) stated beside it
   as a comparison, not a grade; (ii) mean abs-error per numeric quantity, reported
   per unit (implied-reset seconds; prompt_tokens; TTFT ms); (iii) range hit-rate;
   (iv) probe pass/fail/unprovable counts. **No scalar axis verdict** — these lines
   feed SCORECARD via the parent, in the lane's own proxy units.
5. **Defects and surprises** (e.g. a shim leg-order flip falsifying P4, a restored
   `:34113` falsifying P9, an `Unsupported service_tier` string change) are recorded
   as findings with receipts, and routed per PROVINCE §Refusals if they belong to the
   unowned serving plane.

## 5. Runner log contract (`corpus/evidence/probe-r19-*.log`, one file per probe)

```
probe: P<n>
runner-seat: <seat id>
battery_sha256_at_start: <hash from the FROZEN line>
first_request_utc: 2026-10-16THH:MM:SSZ
---
[1/4] 2026-10-16T07:55:00Z POST https://token-plan.../v1/chat/completions
exit: 0  http: 429  ms: 1032
headers-sent: Authorization=<len 113>, Content-Type=application/json
response-headers: retry-after=<value>   # header VALUES only for non-credential headers
excerpt: {"error":{"code":"insufficient_quota",...}}   # ≤400 chars, credential-shaped strings stripped
...
last_request_utc: 2026-10-16T07:56:10Z
outcome: <all-components-recorded | UNRUN: <reason> | TRANSPORT-UNREACHABLE | ...>
```

Redaction: no Authorization/api_key/session-header values; header names and length
markers only; SSE excerpts show event types and the `service_tier` echoes, not raw
bodies. The r18 hygiene gates are the precedent (`fastmode/ANALYSIS.md:279-303`,
`TOTAL HITS: 0`).

## 6. Frozen prediction set (the numbers the registrar freezes)

| id | probe | type | prediction | p / point / range |
|---|---|---|---|---|
| 1a | P1 key2 chat | binary | HTTP 429 | p=0.93 |
| 1b | P1 key3 chat | binary | HTTP 429 | p=0.93 |
| 1c | P1 key2 retry-after | numeric | implied reset = 2026-10-23T16:00:00Z | offset 0, range ±7200 s |
| 1d | P1 key3 retry-after | numeric | implied reset = 2026-10-28T16:00:00Z | offset 0, range ±7200 s |
| 1e | P1 bodies | binary | both contain `insufficient_quota` | p=0.85 |
| 1f | P1 /models ×2 | binary | both HTTP 200 | p=0.90 |
| 2a | P2 status vector | binary | [200,200,400,200,400,400,400] (omit,default,flex,priority,fast,auto,r19-invalid-tier) | p=0.90 |
| 2b | P2 400 bodies | binary | all name `Unsupported service_tier: <value>` | p=0.85 |
| 3a | P3 tier echo | binary | final echo `default` on all 3 serviced | p=0.85 |
| 3b | P3 credits | binary | `x-codex-credits-balance` = 62500.0000000000 on all serviced | p=0.85 |
| 3c | P3 used-percent | binary | `x-codex-primary-used-percent` ≤ 2 on all serviced | p=0.90 |
| 3d | P3 usage parity | binary | usage input_tokens identical across the 3 serviced | p=0.90 |
| 4a | P4 ds non-stream leg | binary | served by leg-1 alibaba-token-plan | p=0.90 |
| 4b | P4 ds stream leg | binary | served by leg-1 alibaba-token-plan | p=0.90 |
| 4c | P4 glm /health legs | binary | legs == ["zai","devin","hyper"] | p=0.85 |
| 4d | P4 glm stream leg | binary | served by leg-1 zai | p=0.90 |
| 4e | P4 ds wall time | numeric | point 1.8 s | band [0.8, 4.0] |
| 4f | P4 glm prompt_tokens | numeric | point 30 | range [15, 60] |
| 5a | P5 ds stream span | binary | incremental: first→last delta span ≥ 50 ms | p=0.85 |
| 5b | P5 glm stream span | binary | burst: first→last delta span < 50 ms | p=0.50 |
| 6a | P6 zai status | binary | HTTP 200 | p=0.93 |
| 6b | P6 zai usage | binary | usage block, completion_tokens > 0 | p=0.90 |
| 6c | P6 zai TTFT | numeric | first-decoded point 3000 ms | range [1500, 6000] |
| 7a | P7 opencode status | binary | HTTP 200, no 403/1010 | p=0.90 |
| 7b | P7 model echo | binary | stream `model` == `deepseek-v4.1-flash` | p=0.90 |
| 7c | P7 prompt_tokens | numeric | point 45 | range [20, 120] |
| 7d | P7 TTFT | numeric | first-decoded point 4000 ms | range [1500, 6500] |
| 8a | P8 kimi-code | binary | HTTP 401 (no auth header) | p=0.90 |
| 8b | P8 body class | binary | contains `invalid_authentication_error` or `Invalid Authentication` | p=0.85 |
| 9a | P9 `:34113` | binary | connection refused / timeout (curl exit 7/28, http 000) | p=0.80 |

Totals: 23 binary components (Brier), 7 numeric components (abs-error + range),
19 HTTP requests (incl. P4's /health GET), ≤240 output tokens.

## 7. FROZEN PREDICTIONS — registrar fills; runners MUST wait for this

Registrar procedure (you own this file jointly with battery-author; touch **only** the
`FROZEN:` line below the anchor):

1. Verify no probe request has been logged yet (no `corpus/evidence/probe-r19-*.log`
   exists).
2. `HASH=$(sed -n '1,/FROZEN-PREDICTIONS-ANCHO[R]/p' plans/probe-battery-r19.md | sha256sum | cut -d' ' -f1)`
   (the `[R]` bracket is deliberate: it matches the anchor line below without the
   pattern matching its own first occurrence earlier in this step's command text —
   the hashed range is line 1 through the anchor line inclusive)
3. `NOW=$(date -u '+%Y-%m-%dT%H:%M:%SZ')`
4. **Re-verify immediately before writing** (closes the compute-then-write race that
   produced breach BR-1): re-run step 2; if the hash differs from step 2's value, the
   file changed mid-procedure — restart from step 2. Write the FROZEN line only when
   the just-recomputed hash equals the one you are about to post.
5. Replace the pending line below with exactly: `FROZEN: <NOW> sha256:<HASH>`
6. Post the FROZEN line (and only that change) — runners may now start. Runners verify:
   re-run step 2; the hash must equal the one on the FROZEN line. The hash covers every
   byte above the anchor, i.e. all of §0–§6 including this procedure; any later edit
   above the anchor invalidates the freeze and must be recorded as a breach.

<!-- FROZEN-PREDICTIONS-ANCHOR -->
FROZEN: 2026-10-16T07:55:58Z sha256:e1a867773ef14ce457a0d560180587324dd07b4deea1ec76d0c2adf65aaa00a1

### 7.1 Freeze and ordering record (append-only)

- **BR-1 (stale freeze, 2026-10-16T07:52:04Z → repaired 07:55:58Z).** The registrar
  posted `FROZEN: 2026-10-16T07:52:04Z sha256:e3f08a09…` — the hash of the
  **pre-rebase** bundle (battery-author's own 07:50:47Z dry-run output), while
  battery-author's v2 re-base edits (P4/P5 re-based on the M7/M9 leg reorders, P7
  disclosure, totals) landed through 07:52:08Z. Root cause: a compute-then-write race
  in the §7 procedure (hash computed ~07:50:47Z, line written ~07:52:04Z) combined
  with drafting and freezing running concurrently. Consequence: the posted freeze did
  not cover the re-based predictions; any runner starting in that window would have
  failed the §7 verify step — a safe deadlock, not a mis-scored outcome. Repair: §7
  step 4 (re-verify immediately before writing) closes the race; the seat holding the
  re-base re-froze at **07:55:58Z** with `sha256:e1a86777…` after a double-read
  stability check (H1 == H2 across a 1 s gap), and the post-write recompute matches.
  The superseded hash `e3f08a09…` is recorded here as the identity of the
  pre-rebase bytes, not as a valid freeze.
- **Runner-side breach, cross-reference (not re-filed):** runner-leg-opencode's
  accidental pre-run — two live requests at 2026-10-16T07:45:00–04Z, before this file
  existed (born 07:47:53Z) — is self-filed with verbatim receipts in
  `corpus/evidence/probe-r19-opencode-health.log` (DEFECT 0), contained by that seat.
  The §4 ordering gate excludes any outcome that precedes its prediction.
- **No runner executions between the stale freeze and the re-freeze:** as of
  07:56:30Z, `probe-r19-shim-ds-run.log` contains header lines only (no execution
  entries), and `probe-r19-opencode-health.log`'s last entry is its 07:47Z containment
  note. First battery-governed request must postdate 07:55:58Z and verify against
  `e1a86777…`.

- **RA-1 (registrar ordering audit, filed 2026-10-16T08:07Z — revises the two
  bullets above where receipts conflict).** The registrar's 07:52:04Z stamp
  matched the on-disk bytes at stamp time: three independent recomputes
  reproduced `e3f08a09…` after the stamp — the registrar's own (~07:52:15Z),
  runner-leg-glm-cascade's (probe-r19-P4-glm.log:9-10, at 07:52:40Z), and
  runner-shim-glm's (probe-r19-shim-glm-predictions.log:5-6, at 07:52:58Z).
  BR-1's "v2 re-base edits … landed through 07:52:08Z" is therefore falsified
  as a disk timeline: the above-anchor edits landed in (07:52:58Z, 07:55:58Z),
  after those verifications. The freeze-invalidating event per §7 step 5 is
  the post-freeze above-anchor edit itself; freeze-1 was byte-valid at stamp
  time and for ≥54 s after, and the runners that verified `e3f08a09…` followed
  the then-live gate. BR-1's compute-then-write-race root cause is revised
  accordingly; its content-level judgment (v1's P4/P5 premises stale vs the
  M7/M9 leg reorders) stands.
- **RA-2 (BR-1's "no runner executions between the stale freeze and the
  re-freeze" is falsified).** Battery-governed first requests inside the
  07:52:04Z→07:55:58Z window: P6 07:52:25Z (probe-r19-P6-zai.log:5), P7
  07:52:29Z (probe-r19-opencode-health.log:52), P1-key1 addendum 07:52:50Z
  (probe-r19-P1-key1-quota.log:10), P1 07:52:53Z (probe-r19-p1-listing-mismatch.log:4)
  and its duplicate seat 07:53:02Z (probe-r19-quota23.log:5), shim-ds
  S7/S6/S1/S2/S5 07:52:48–07:53:05Z (probe-r19-shim-ds-run.log), P4-glm
  07:53:22–25Z (probe-r19-P4-glm.log), devin seat-check 07:53:54–07:54:38Z
  (probe-r19-devin-shim-seat.log). Every one records
  `battery_sha256_at_start == e3f08a09…` — the live FROZEN hash at its
  verification time. The BR-1 bullet's own observation is contradicted by
  probe-r19-shim-ds-run.log (mtime 07:54:31Z, execution entries at
  07:52:48–07:53:29Z) and by this file's mtime (07:56:09Z) predating the
  07:56:30Z observation time it quotes.
- **RA-3 (ordering-based scoreability, for the scorer; scoring itself is the
  scorer's seat).** §6 rows 1a–1f, 2a–2b, 3a–3d, 6a–6c, 7a–7d, 8a–8b, 9a are
  byte-identical across the freeze-1 and freeze-2 versions, so the
  freeze-1-window outcomes listed in RA-2 are scoreable against them (every
  outcome postdates freeze-1; no outcome precedes its prediction). The 4x/5x
  rows were rewritten between versions and their id semantics shifted (v1-4a
  = glm prompt_tokens point 11734; v2-4a = ds non-stream leg binary), so:
  (a) pre-freeze-2 P4/P5 outcomes (P4-glm/P5-glm, 07:53:22–25Z) precede the
  v2 freeze and are UNPROVABLE as battery 4x/5x components; (b) shim-glm's
  receipts (07:56:26Z / 07:57:52.331Z) postdate freeze-2 and its seat
  predictions (07:55:05Z) predate its requests — validly ordered; (c)
  runner-leg-devin's P4 log (probe-r19-P4-devinleg.log) cites `e3f08a09…`
  while its requests (07:56:39Z+) postdate freeze-2 — stale-hash citation,
  §4-gate mismatch, excluded from the battery aggregate unless the scorer
  rules otherwise.
- **RA-4 (deviations recorded, not adjudicated).** (i) shim-glm attempt 2
  re-sent the P4(i) body minus `temperature` after a 400 — a reshaped retry
  (battery §2 rule 3 allows retries only for connection-level failures);
  self-disclosed in probe-r19-shim-glm-run.log §2. (ii) P1 ran in two seats
  (8 requests vs 4 budgeted; receipts agree on every component) and P4(i) in
  three seats (7 requests to :8793 vs 2 budgeted) — the ≤20-request budget is
  exceeded in aggregate when seat-level probes on the same hosts are counted;
  budget accounting belongs to the scorer/integrator. (iii)
  probe-r19-P4-devinleg.log carries a duplicated header block and a
  NameError-crashed [3/3] whose response was still captured
  (prompt_tokens 48, span 0 ms — probe-r19-P4-devinleg.log:30-35).
- **RA-5 (post-freeze-2 status at audit time).** Freeze-2 `e1a86777…`
  re-verified by the registrar at 07:59:40–08:04:38Z (8 consecutive polls,
  unchanged) and independently by runner-leg-hyper
  (probe-r19-hyper.log:15-18, 07:58:11Z + 07:59:26Z pre-execution). Of the
  post-freeze-2 runs, only runner-leg-hyper's log records the §4-gate hash
  matching the live freeze. No P2/P8/P9 runner logs exist as of 08:07Z;
  freeze-2 stands for them if they run. The zai-leg 429 wave visible at the
  glm shim (probe-r19-P4-glm.log finding 3) is the likely mechanism behind
  P6's 429 outcome (probe-r19-P6-zai.log:8-12) — a route-state observation
  for the scorer's aggregate read, per ledger-route-telemetry.md:60-62.

## 8. Sources

- `corpus/knowledge/kimi-model-routing-round18.md` (:89 M6 row; :109-113 D2; :117-123
  DEF-3b; :129-133 D1; :137-138 devin billing; :149 verify-first; :163-165 shim leg
  question; :166-176 M5) — primary digest.
- `corpus/knowledge/ledger-route-telemetry.md:60-62` — meter-state vs model-failure
  frame.
- `corpus/knowledge/bench-arena-fresh-run.md:11` — `:34113` availability evidence.
- Parent trees `../research/round-18-kimi-model-routing/`: `census/ANALYSIS.md`
  (:30-38 shims; :55, :80-96 D1/D3; :134-144 D9; :184-208 stream table + burst rule;
  :228 secrets handling; `manifest.json` redacted base_urls), `fastmode/ANALYSIS.md`
  (:122-131 acceptance; :184-215 echo + quota), `fastmode/scripts/probe_fastmode.py:103-115`
  (request shape), `battery/ANALYSIS.md` (:20-23 method/burst/warm-up; :31-33 pool rows),
  `battery-opencode/ANALYSIS.md` (:15, :24-26, :46-62, :78-87, :119-121), `battery/predictions/PREDICTIONS.md`
  (ex-ante idiom).
- `../research/round-18-kimi-model-routing/cascade-legorder/LEGORDER.md` (M7: ds
  reorder alibaba→hyper→opencode-go, applied 2026-10-15) and
  `../research/round-18-kimi-model-routing/glm-flash-legorder/LEGORDER.md` (M9: glm
  reorder zai→devin→hyper) — post-r18 serving-plane state, discovered via runner
  receipts during drafting.
- Lane contracts: `SCORECARD.md:34-37,163,367` (calibration proxy + round history),
  `PROVINCE.md` (surfaces, refusals), `corpus/evidence/round18-kimi-routing/README.md`
  (merge verification).
