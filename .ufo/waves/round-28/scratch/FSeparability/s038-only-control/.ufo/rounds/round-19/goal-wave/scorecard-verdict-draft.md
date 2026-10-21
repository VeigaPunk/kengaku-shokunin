# scorecard-verdict-draft — kengaku round 19 (calibration: standing probe battery)

Scribe seat, round-19 goal wave. Written 2026-10-16, updated through
2026-10-16T08:10Z; starting commit `05cb955`. **This file writes nothing**:
every block below is a paste-ready delta for a PARENT-owned file
(`SCORECARD.md`, `LOG.md`); the parent integrates under the kengaku lane
identity. `[PARENT]` markers flag cells the parent must confirm or fill from
landed artifacts at integration time. No scalar axis verdicts — verdicts are
recorded per gate, per the round-16 idiom
(`corpus/lessons/round-16-recensus.md` "Verdict lines (measured)").

## 0. Measured state at draft time

| Quantity | Value | Command (run 2026-10-16T07:48:55Z) |
|---|---|---|
| HEAD | `05cb955` | `git rev-parse --short HEAD` |
| Gate | `CHECKS n=733 mismatches=0 errata_pinned=1` / `VERDICT: PASS — stored evidence fully re-derives offline`, exit 0 | `python3 grader.py` |
| Selftest | exit 0 (`[selftest] ALL PASS`, S0–S7) | `python3 grader.py --selftest` |
| Working tree (lane) | `?? .ufo/interactive-sessions/` + r19 evidence logs + battery plan; no tracked-file edits | `git status --porcelain` |

## 1. The round's falsifiable claim, with receipts

**Before-claim (pre-registered in `plans/probe-battery-r19.md` §0, drafted
2026-10-16T07:44:09Z):** the calibration proxy (probes with predictions filed
before the first request, scored at close) ran **0/1, 1/1, 0/0, 1/1** across
rounds 8–11 — intermittent, ad hoc; **no standing battery or reusable template
exists**.

Scribe re-verification of the before-state (independent of the battery-author's
citations):

- `SCORECARD.md:33-46` — proxy (a) carries exactly the r8 `0/1`, r9 `1/1`,
  r10 `0/0` ("hermetic round, no probe ran"), r11 `1/1` history; r12's
  predictions are recorded at `SCORECARD.md:163` as filed before its first
  request (`ordering.log` 01:16:08Z < first `request_ts` 01:19:59Z) but scored
  and landed only in round 14 — the in-round clause breached by lateness.
- `find . -path ./.git -prune -o -iname '*battery*' -print` (run
  2026-10-16T07:36Z, pre-battery) → 1 hit:
  `corpus/knowledge/bench-arena-round5-battery.md` — a knowledge digest of an
  external battery, not a lane battery. `grep -ril template plans/` → 0 hits;
  `plans/` held only `wwkd-round-16-recensus.md` and `wwkd-round-17-coverage.md`.
  **No standing battery, no template** — the before-claim's negative half is
  true at round start.
- The move log's last row is round 16 (`SCORECARD.md:367-368`); rounds 17
  (blocked, `SCORECARD.md:369-414`) and 18 (parent-fleet digest land,
  `LOG.md` §18) ran no scored lane battery.

## 2. Verdict draft — calibration axis-move (paste-ready section)

```markdown
## Round 19 — standing probe battery (calibration axis-move)

The round's deliverable is a standing, pre-registered probe battery:
`plans/probe-battery-r19.md` — 9 falsifiable live-route probes (P1–P9),
predictions in §6 frozen with UTC before any request (registrar
`FROZEN: 2026-10-16T07:55:58Z sha256:e1a86777…` after the BR-1 stale-freeze
repair; the superseded `e3f08a09…` freeze is recorded in plan §7.1), every
probe citing its round-18 receipt (§1), scored at close with an aggregate
calibration read (§4), plus a reusable host-agnostic template
`plans/probe-battery-TEMPLATE.md`.

| Axis | Verdict | Evidence / limit |
|---|---|---|
| calibration | [PARENT: verdict line from the landed scorer note] | `plans/probe-battery-r19.md` (frozen e3f08a09; post-freeze amendment 8446efc7 recorded — see breach line); `corpus/evidence/probe-r19-*.log` ({{N_LOGS}} logs); `corpus/knowledge/probe-battery-r19.md` (scorer); `plans/probe-battery-TEMPLATE.md` |
| novelty | unchanged | No new construct: every probe re-tests a round-18 receipt on the same routes. |
| operability | unchanged | No gate change; `python3 grader.py` → `CHECKS n=733 mismatches=0 errata_pinned=1`, exit 0 at round start (this draft §0). [PARENT: re-run at close] |
| freshness | [PARENT: verdict lines from the battery's own re-verification receipts] | P8/P9 are standing re-verification probes (auth-dead lane, absent served model); outcomes land in the scorer note. |
| coverage | unchanged | No index change claimed by the battery itself. [PARENT: index rows for the scorer note/template if landed] |
| depth | unchanged | No new sourced claim beyond the battery artifacts. |
| adjacency | unchanged | Serving-plane findings route per PROVINCE §Refusals: the confirmed leg-order drift (P4 drift note) is an operator serving-plane fact, routed not absorbed. |

Proxy (a) reading for this round (measurement, not a score): {{PROXY_A_LINE —
the scorer's aggregate calibration read}}. Timestamp ordering audited per plan
§4 step 1: {{ORDERING_LINE — e.g. "all scored outcomes postdate their
predictions; the recorded breaches are: BR-1 (stale freeze, repaired by
re-freeze), DEFECT 0 (out-of-band pre-run, excluded), the six stale-freeze
runner executions (D-s6), the shim-glm reshaped retry (D-s11), the duplicate
P1 (D-s7), the same-second addendum filing (D-s8) — each recorded, never
patched"}}.
```

**[PARENT] Fill rules for the table above:**

1. `{{N_LOGS}}` — `ls corpus/evidence/ | grep -c 'probe-r19-.*\.log'` at close.
2. `{{PROXY_A_LINE}}`, `{{ORDERING_LINE}}` — quote the scorer note's own lines
   (`corpus/knowledge/probe-battery-r19.md`); do not recompute differently.
3. The calibration cell's verdict line must be a verdict *per gate* (round-16
   idiom), not a scalar. Whether calibration moves is the parent's judgement;
   this draft files the evidence, not the number.
4. **Rulings the scorer note must carry for the parent to integrate cleanly**
   (each is already receipt-backed; the scorer adjudicates, the parent
   records):
   - (i) **Which prediction set governs P4/P5** — the frozen e3f08a09 set
     (22 binary / 18 requests) or the post-freeze amended 8446efc7 set
     (23 binary / 19 requests) which was never re-frozen. Per plan §7 step 5,
     a post-freeze edit above the anchor invalidates the freeze; the scorer
     must say whether P4/P5 outcomes score inside the aggregate, outside it,
     or as a recorded-breach class of their own.
   - (ii) **Duplicate P1** — two seats each ran P1's full 4-request set
     (runner-listing-mismatch 07:52:53–07:53:06Z; runner-quota-23
     07:53:02–07:53:13Z); the plan budgeted 4. Both receipts are complete and
     mutually corroborating; one presumably joins the aggregate and the other
     is recorded as an over-budget duplicate.
   - (iii) **P1-key1 addendum** (`probe-r19-P1-key1-quota.log`) — a
     parent-dispatched probe outside §6 with its own three-way prediction
     filed at 07:52:50Z, the same second as its first request (see D-s8).
   - (iv) **DEFECT 0** (`probe-r19-opencode-health.log:8-42`) — two live
     requests at 07:45:00–07:45:04Z, before the battery existed; seat
     self-reported, contained 07:46:36Z; outcomes excluded from the aggregate.
   - (v) **Budget cap** — §2's binding "≤20 HTTP requests total" vs amended
     19 + 4 duplicate P1 = 23 battery-governed requests (plus the two
     out-of-band opencode requests and three seat-level devin requests, which
     the seats themselves excluded from the battery aggregate).

## 3. Scribe findings (filed, not patched; each with its receipt)

- **D-s1 (cosmetic, runner-owned file — scribe does not edit):**
  `corpus/evidence/probe-r19-shim-ds-predictions.log:105` originally embedded
  its digest as `EOF78de64d9…` (stray literal prefix). The arithmetic always
  verified (`head -n -1 <file> | sha256sum` →
  `78de64d930c3c7e80b6e98efe4b8f4418168365093a23f589c3422d508e1e264`), and the
  runner superseded the line in its 07:44:02Z revision; the companion run log
  (`probe-r19-shim-ds-run.log:2`) cites the clean hash. Recorded for the audit
  trail; no action.
- **D-s2 (wording erratum, not a defect — resolves the battery plan's three
  budget numbers):** §2 binds "≤20 HTTP requests total, ≤256 output tokens";
  the frozen §6 totalled 18 requests / ≤232 tokens; §0 said 18 / ≤240. The
  numbers reconcile structurally: 17 enumerated + P4's warm-up = 18 requests;
  ≤232 = serviced output tokens, ≤240 = including the warm-up, ≤256 = the
  binding cap. The re-based §6 re-totalled to 19 requests / ≤240 tokens
  (P4 gained a `/health` GET). The plan never states the reconciliation; a
  one-line footnote would prevent the next reader from filing this as a
  defect.
- **D-s3 (hash-lineage nuance, verified, no defect):** the shim-ds predictions
  cite `[CODE] ~/.local/share/ds-flash-shim/shim.py sha256 42d86d99…` (mtime
  2026-10-15 14:15 -03, post-M7), while M7's artifact
  (`../research/round-18-kimi-model-routing/cascade-legorder/LEGORDER.md:69`)
  records post-edit hash `054011ea…`. The two differ because the mori round-3
  content-inspection patch (fleet `MANIFEST.json:2414`) landed after M7.
  Scribe re-hash at 07:47Z → `42d86d99d42658214e362c2759ecab88a03de005e9ed93e9c1804cbf8c15a386`
  — the prediction file's pin matches the live bytes exactly. Lineage:
  M7-edit → mori-patch → probed bytes; recorded so the two hashes are not read
  as a contradiction.
- **D-s4 (premise check — negative half verified; positive half landed):**
  the before-claim's negative half was independently re-verified at 07:36Z
  before any battery artifact existed (§1 above). The template
  `plans/probe-battery-TEMPLATE.md` landed by 08:07Z (308 lines; §9
  instantiation checklist; lineage table extracting r9/r11/r18/r19 practices
  with receipts). Its own r19 citations are stale in three places — see
  D-s14. [PARENT: confirm both files at integration; if the scorer note has
  not landed, the "scored at close" leg of the after-claim is unmet and the
  verdict must say so.]
- **D-s5 (scribe self-disclosure, ordering-safe):** at 07:48:55Z — before the
  battery plan was noticed to exist — the scribe ran one identity-confirming
  `curl -s -m 5 http://127.0.0.1:8791/health` → 200 `{"ok": true, "service":
  "ds-flash-shim", "port": 8791, "legs": ["alibaba-token-plan", "hyper",
  "opencode-go"]}`. Third-party observation of the event shim-ds's S7
  predicts; it postdates that prediction's hash (07:44:02Z revision, original
  07:43:30Z), is idempotent, consumes no battery budget, and touches no runner
  log. No further battery-target requests were issued by this seat.
- **D-s6 (THE FREEZE SAGA — four hash states, one re-freeze, outcome-informed
  re-base; the round's central ordering event).** All hashes below were
  computed by the scribe with the plan's own §7 step-2 command; file mtimes
  via `stat -c '%y'` (local -03, +3 h = UTC).
  - 07:44:09Z — plan v1 drafted (390 lines): P4 predicted the r18-digest
    framing (glm cascade devin-first, prompt_tokens 11734 [10000, 13000]).
  - 07:52:04Z — registrar posts `FROZEN: 2026-10-16T07:52:04Z
    sha256:e3f08a09…`. The scribe had independently computed the same hash
    moments earlier over the pre-freeze bytes (pre-computation predates the
    observed FROZEN line). Six seats then executed against this stale freeze:
    P6-zai (first request 07:52:25Z), P1-key1 addendum (07:52:50Z), shim-ds
    S1–S8 (07:52:48Z+), listing-mismatch P1 (07:52:53Z), quota23 P1
    (07:53:02Z), P4-glm (07:53:22–25Z) — every one recording
    `battery_sha256_at_start: e3f08a09…` and (where documented) verifying it
    against the then-posted FROZEN line.
  - 07:52:30Z (plan §0 revision note) — "v2 … P4/P5 re-based and P7
    disclosure added **after runner-seat receipts revealed** the operator's
    post-r18 cascade leg reorders (M7/M9…)". The plan says this itself: the
    re-base is receipt-informed. The re-based P4/P5 predict what the runner
    receipts had already shown (zai-first glm, shim-ds's S1/S2 alibaba
    leg-1) — **no outcome may precede its prediction cannot hold for the
    re-based components whose outcomes were already on disk.**
  - 07:54:5xZ — scribe re-run → `1a1f8b69…` (re-base mid-landing);
    07:55:02Z — file mtime; scribe re-run → `8446efc7…` (settled re-base,
    pre-re-freeze; this transient state is scribe-observed only, recorded in
    no other artifact).
  - 07:55:58Z — re-freeze: the FROZEN line (plan :415) now reads
    `FROZEN: 2026-10-16T07:55:58Z
    sha256:e1a867773ef14ce457a0d560180587324dd07b4deea1ec76d0c2adf65aaa00a1`.
    Scribe re-run at ~08:02Z → `e1a86777…` exactly. **The current freeze
    verifies.**
  - Plan :417-443 (new §7.1 BR-1) records the registrar's own account: the
    07:52:04Z freeze hashed the battery-author's **pre-rebase** dry-run bytes
    (a compute-then-write race); repair = §7 step 4 (re-verify before write)
    + the 07:55:58Z re-freeze; "the superseded hash `e3f08a09…` is recorded
    here as the identity of the pre-rebase bytes, not as a valid freeze."
  - **Contradictions the scorer must resolve** (each receipt-backed):
    (a) §7.1's "No runner executions between the stale freeze and the
    re-freeze … as of 07:56:30Z `probe-r19-shim-ds-run.log` contains header
    lines only" is falsified by mtimes: the shim-ds run log's last write was
    **07:54:31Z** (172 lines: full S1–S8 executions + the seat scoring
    table), and five other logs carry first-request stamps 07:52:25–07:53:25Z
    in the claimed-empty window. (b) §7.1 claims the v2 re-base "landed
    through 07:52:08Z", yet quota23's §7 re-computation (~07:53Z) and
    P4-glm's (07:52:40Z) still returned the pre-rebase `e3f08a09…` — the
    rebase bytes were not yet observable to runners; the landing window the
    scribe observed is ~07:54–07:55:02Z. (c) §7.1's "as of 07:56:30Z"
    observation stamp postdates the file's own last-edit mtime 07:56:09Z.
    (d) The re-based component ids renumber the frozen set (frozen 4b = ds
    prompt_tokens, 5a = glm burst; re-based 4a–4d = leg identities, 4f = glm
    tokens, 5a = ds incremental) — runner logs cite the FROZEN ids while the
    current file carries the re-based ones; the scorer must score each
    outcome against the set that actually predicted it.
  - [PARENT/scorer: the adjudication this draft requests: (i) the six
    stale-freeze executions are battery-governed under the then-posted FROZEN
    line but "not a valid freeze" per §7.1 — rule which framing governs;
    (ii) the re-based P4/P5 components whose outcomes predate 07:55:58Z are
    outcome-informed — they cannot enter the calibration aggregate as
    predictions; score them as recorded findings or breach-class, never as
    forecast skill; (iii) the frozen-set components that DID have
    pre-outcome predictions (P1 1a–1f, P6 6a–6c, P4 frozen 4b, 5a/5b) are
    the aggregate's legitimate input, plus every cleanly-ordered seat-level
    set (shim-ds S1–S8, shim-glm G1–G8, hyper H1–H10, devin D1–D5).]
- **D-s7 (duplicate P1 + budget-cap arithmetic):** two seats each executed
  P1's full 4-request set against the same two dead keys within 21 s of each
  other (runner-listing-mismatch 07:52:53Z start; runner-quota-23 07:53:02Z
  start) — 8 requests where the plan budgeted 4, and the two seats' requests
  interleave 1 s apart at 07:53:01/07:53:02Z (§2 rule 4's ≥2 s same-host
  spacing is per-seat here; cross-seat coordination was impossible without a
  shared dispatch ledger). Battery-governed total under the amended §6:
  19 + 4 duplicate = 23 > §2's binding ≤20. Both receipts are complete and
  corroborate each other (same 429 bodies, retry-after 634017/634027 and
  1066010/1066018 — 10 s/8 s of meter drift between the two runs). Scorer
  rules which run joins the aggregate; the cap breach is recorded either way.
- **D-s8 (same-second addendum filing):** `probe-r19-P1-key1-quota.log:5,8`
  — `prediction_filed_utc: 2026-10-16T07:52:50Z` equals
  `first_request_utc: 2026-10-16T07:52:50Z`. At one-second resolution the
  ordering is `filed == first request`, not strictly `<`; the r12 precedent
  (SCORECARD round-12/14 errata: one-second timestamps prove `<=`, not `<`)
  applies. The probe is a parent-dispatched addendum outside battery §6, so
  the strict gate does not bind it — but the scorer should state the
  convention used.
- **D-s9 (opencode DEFECT 0 — carried from the runner's own filing):**
  `corpus/evidence/probe-r19-opencode-health.log:8-42`: two live requests
  07:45:00–07:45:04Z fired by a draft-rev runner whose dry mode did not gate
  the probe loop, before the battery plan existed (seat polled 07:37:14Z →
  07:44:30Z, BATTERY_NOT_YET throughout). Self-reported, gate fixed and
  re-tested 07:46:36Z (0 socket connections), requests recorded as
  out-of-band, not scored. Incidental observation preserved: the opencode
  lane spent its entire 16-token budget on reasoning with zero content
  (consistent with the r18 digest's `‡` footnote class).
- **D-s10 (devin seat D5 numeric not derivable from the landed log as
  written):** `probe-r19-devin-shim-seat.log:99-105` records D3/D4 receipts
  (stream 200, prompt_tokens 485, completion 162, 126 SSE lines, content
  correct 1→30) but no first-content-delta timestamp, so D5 (TTFT point
  3700 ms, band [800, 12000]) cannot be scored from the file as landed.
  Scorer rules UNPROVABLE or the seat appends the timing. D2 is the round's
  first seat-level MISS: predicted 200 (p=0.80), observed HTTP 400
  `invalid_argument` on the r18 census shape (temperature:0, non-stream,
  swe-2) — extending M10's field-isolation finding (opus 400s on
  temperature:0) to swe-2; D4's range hit (485 ∈ [4, 13000]) comes with a
  point miss of 11,678 tokens against the 12,163 carry-over, and its
  falsifier band [4, 120] did not fire.
- **D-s11 (shim-glm reshaped retry — §2 rule 3 breach, transparently
  documented):** `probe-r19-shim-glm-run.log:42-115` — attempt 1 (07:56:26Z,
  battery P4 body with `temperature`) returned 400 terminal; the seat itself
  states rule 3 "allows one retry for connection-level failures only; a 400
  is an HTTP status response", files attempt 1 as an outcome — and then runs
  attempt 2 (07:57:52Z) with the identical body minus `temperature` as "the
  scored run". This is the reshaped retry the battery forbids ("no reshaped
  retry", §3 shared-body note). The seat's transparency is exemplary (the
  cross-check against direct :8787 isolates `temperature` as the rejected
  field — a genuinely valuable finding), but the attempt-2-derived component
  scores (battery 4a = 407, 5a = burst) are post-reshape measurements.
  [PARENT/scorer: rule whether attempt-2-derived component scores join the
  aggregate or are breach-class; the seat-level G-verdicts filed on attempt 2
  (G2/G5/G6) carry the same question.]
- **D-s12 (serving-plane findings cluster — routed, not absorbed; each
  already receipt-backed by its seat):** (a) both cascade shims were
  redeployed as new software at 2026-10-15T17:16:22Z — `Server:
  devin-openai-shim/2` today vs the r18 census `BaseHTTP/0.6 Python/3.14.7`
  (`probe-r19-P4-glm.log:73-78`) — a fleet-level shim upgrade sits between
  every r18 number and this battery; (b) the devin leg rejects any
  `temperature`-bearing body with 400 `devin_shim_error/invalid_argument`
  and the glm cascade treats that 400 as terminal (no fall-through), so a
  zai 429 + a temperature-bearing body = caller gets 400 with zero output
  (`probe-r19-shim-glm-run.log` F-2); (c) status masking: on all-legs-fail
  the new shim returns the LAST leg's status, hiding the zai 429
  (`probe-r19-P4-glm.log:93-96`); (d) the zai leg is rate-limited under the
  wave's aggregate load — journal 302 OK / 547 FAIL-429 (35.6% serve) in one
  window, absorbed by devin fallback 525/0 (`probe-r19-shim-glm-run.log` F-3;
  route-state per `ledger-route-telemetry.md:60-62`, not model quality);
  (e) the glm-flash caller-auth finding: the shim reads no Authorization
  header at all (`shim-glm` G7, HIT — the battery's "shim api_key via
  loader" step is unnecessary for this shim). All of it belongs to the
  unowned serving plane → integrator/operator per `PROVINCE.md` §Refusals.
  (f) hyper prompt-billing drift: identical COUNT_PROMPT billed 31 (census
  D9, 2026-10-15) → 48 (2026-10-16) with no request-shape change — a
  serving-side change on hyper.charm.land, same routing (`probe-r19-hyper.log`
  finding 2).
- **D-s13 (P4-devinleg log structure + post-re-freeze hash ambiguity):**
  `probe-r19-P4-devinleg.log` carries two `probe: P4` header blocks (the
  seat restarted its runner): 3 glm-cascade attempts (07:56:39Z, 07:57:06Z,
  07:57:11Z — all 400 terminal on the temperature shape) plus 1 ds-cascade
  stream (07:57:59Z). The ds request crashed the seat's own runner
  (`exit: http=error … error=NameError: name 'rec' is not defined`,
  `:30`) while still capturing the response (prompt_tokens 48, span 0 ms,
  18 SSE lines) and declaring "outcome: all-components-recorded" (`:37`) —
  generous, and the crash means the runner's capture code did not survive to
  process the stream. The seat also recorded
  `battery_sha256_at_start: e3f08a09…` (`:3`, `:14`) for requests made at
  07:56:39Z+ — after both the re-base and the 07:55:58Z re-freeze; whether
  the seat re-verified §7 at start is not documented, and any re-verification
  after 07:55:58Z would have returned `e1a86777…`, not the recorded hash.
  [PARENT/scorer: treat this seat's P4/P5 components as breach-class or
  UNPROVABLE unless the seat documents its verification moment.]
- **Raw observations the scorer owns the combination of** (receipts cited;
  the scribe files no scores): frozen-set components with clean pre-outcome
  predictions: 1a–1f all hit (implied resets 2026-10-23T15:59:59Z /
  2026-10-28T15:59:59Z, abs-errors 1 s vs ±7200 s bands; both listings 200);
  6a/6b miss (zai 429), 6c unprovable; frozen 4b (ds prompt_tokens point 48
  [30, 80]) HIT exactly (48, `probe-r19-P4-devinleg.log:32`); frozen 5b (ds
  burst) HIT (span 0 ms) while the re-based 5a (ds INCREMENTAL, p=0.85)
  would MISS on the same observation — the component-id flip of D-s6(d)
  matters here; battery 4a (glm ≥ 10000) falsified via the leg-change path
  (407 from the devin fallback, `probe-r19-shim-glm-run.log` F-1); frozen
  5a (glm burst p=0.80) HIT on shim-glm's stream (0.033 ms). Seat-level
  sets, cleanly ordered by their own prereg hashes: shim-ds S1–S8 (9/9 HIT,
  mean Brier 0.0050), shim-glm G1–G8 (mean Brier 0.0772 over 7 scored),
  devin D1–D5 (D2 miss, D5 unscorable), hyper H1–H10 (12/13 components hit,
  mean Brier 0.0332 over 11 scored binaries; the one miss is the DESIGNED
  H8 coin-flip p=0.55 → incremental 145 ms, falsifying the census's
  "burst-lane" prior as a per-model, not per-lane, property; prompt_tokens
  for identical COUNT_PROMPT drifted 31 → 48 vs census D9 — serving-side
  change, routed; ordering clean: freeze < predictions < first request).
- **D-s14 (template sync defects — template-author-owned file, recorded not
  patched):** `plans/probe-battery-TEMPLATE.md` (a) :17 cites the r19
  freeze as `FROZEN 2026-10-16T07:52:04Z sha256 e3f08a09…98943` — the hash
  plan §7.1 BR-1 records as "the identity of the pre-rebase bytes, not a
  valid freeze"; the valid credential is the 07:55:58Z `e1a86777…` re-freeze;
  (b) §5's registrar procedure omits the BR-1-closing step the r19 plan
  carries (:404-406: "Re-verify immediately before writing … closes the
  compute-then-write race that produced breach BR-1") — a future round
  following the template verbatim would reintroduce the race; (c) §5 step 6's
  breach doctrine ("corrections land as appended errata below the anchor")
  does not describe what actually repaired r19 (a re-freeze with a new hash
  and a §7.1 record); (d) :241 quotes the frozen-set budget "18 requests,
  ≤232 output tokens" superseded by the re-based 19/≤240. The template is
  otherwise the round's structural deliverable — §10's "known defects of
  this instrument" is exactly the right shape — and these are sync defects,
  not design defects.
- **Runner-command nuance (cosmetic, for the audit trail):** runner logs
  document the freeze verification with the un-bracketed pattern
  `sed -n '1,/FROZEN-PREDICTIONS-ANCHOR/p'` (`probe-r19-quota23.log:14`)
  while plan §7 step 2 specifies the bracketed `ANCHO[R]` form; both hash the
  same byte range (scribe verified both forms produce identical digests at
  07:54Z and 07:56Z) because the bracket exists only so the command text does
  not match itself.

## 4. Sources for every claim in this draft

- `SCORECARD.md:33-46` (proxy (a) + r8–r11 counts), `:163` (r12 in-round
  breach), `:367` (move log last row = round 16), `:369-414` (round-17
  blocked record).
- `plans/probe-battery-r19.md` — battery plan: drafted 07:44:09Z (390 lines),
  frozen 07:52:04Z `e3f08a09…` (stale, BR-1), re-based v2 (P4/P5 re-framed to
  M7/M9; §6 re-totalled 22→23 binary, 18→19 requests), re-frozen 07:55:58Z
  `e1a86777…` (current, scribe-verified); §0 before-claim, §3 probes, §6
  prediction set, §7 freeze procedure + §7.1 freeze record. All hash values
  in this draft were computed by the scribe with the plan's own §7 step-2
  command.
- Runner receipts (all under `corpus/evidence/`):
  `probe-r19-shim-ds-predictions.log` (S1–S8, 07:43:30Z), `probe-r19-shim-ds-run.log`
  (executions 07:52:48Z+, seat scoring 07:55Z: 9/9 HIT, mean Brier 0.0050 over
  8 binary terms), `probe-r19-opencode-health.log` (DEFECT 0, 07:47Z),
  `probe-r19-quota23.log` (P1, 07:53:02–13Z), `probe-r19-p1-listing-mismatch.log`
  (P1 duplicate, 07:52:53–07:53:06Z), `probe-r19-P1-key1-quota.log` (addendum,
  07:52:50Z, 200), `probe-r19-P6-zai.log` (P6, 07:52:25Z, 429 rate-limit code
  1302 — 6a/6b miss, 6c unprovable), `probe-r19-devin-shim-seat.log` (seat
  level D1–D5, 07:53:54–07:54:38Z: D1 hit, D2 MISS 400, D3 hit, D4 range-hit
  485, D5 unrecorded), `probe-r19-P4-glm.log` + `probe-r19-P5-glm.log`
  (07:53:22–25Z: both requests 400 terminal — zai leg 429 + devin leg 400 on
  the temperature-bearing shape; 4a/4c-glm UNPROVABLE, 5a UNPROVABLE;
  findings: zai-first order, shim software drift "devin-openai-shim/2",
  status masking), `probe-r19-shim-glm-predictions.log` (G1–G8, 07:55:05Z,
  prereg sha256 `a1674cfc…`) + `probe-r19-shim-glm-run.log` (07:56:26Z +
  07:57:52Z: attempt-1 400 terminal, attempt-2 (temperature dropped) 200
  served by devin fallback — 4a falsified via the leg-change path (407
  outside [10000,13000]), 5a burst HIT span 0.033 ms; G-verdicts 6/7 HIT +
  G1 miss + G3 unprovable; mean Brier 0.0772 over 7 scored; F-2: devin leg
  rejects `temperature` → serving-plane defect routed), `probe-r19-hyper-predictions.log`
  (H1–H10, 07:56:41Z, block sha256 `4fa6e0e6…`; erratum records the re-freeze
  and that the seat verified `e3f08a09…` at 07:52:32Z pre-re-freeze).
- Parent trees: `cascade-legorder/LEGORDER.md` (M7, applied 2026-10-15
  11:26:20 -03), `glm-flash-legorder/LEGORDER.md` (M9, landed 2026-10-15
  14:42Z — zai→devin→hyper, zai leg verified serving, prompt_tokens=19),
  fleet `MANIFEST.json:2414` (mori round-3 shim patch, verbatim).
- Idiom/precedent: `corpus/lessons/round-16-recensus.md` (verdict-per-gate);
  `corpus/evidence/round14-fleet/r14-scribe-drafts.md` (draft format);
  `SCORECARD.md` round-12/14 errata (one-second ordering convention).

## 5. Status at scribe handoff (2026-10-16T08:14Z)

Landed and covered by this draft: the battery plan (both freezes), the
template, and all 15 `corpus/evidence/probe-r19-*.log` runner receipts
(14 findings, D-s1–D-s14). **Not yet landed at handoff:** the scorer note
`corpus/knowledge/probe-battery-r19.md` — the last pipeline stage, and the
leg that carries the round's "scored at close" claim and the rulings this
draft requests (D-s6(i)–(iii) adjudications, duplicate-P1 exclusion, DEFECT-0
exclusion, reshaped-retry class, aggregate calibration read). Also absent:
any runner log for P2/P3 (codex), P7 (opencode battery-governed), P8
(kimi-code), P9 (`:34113`) — whether those probes ran is unknown to the
scribe; the scorer note must state it (the plan's own §4 step 2 makes UNRUN
components a filed-for state, listed with reasons, not a silence).

[PARENT] integration options, in the lane's own spirit of recorded-not-
laundered: (a) wait for the scorer note and fill the {{}} slots from it
(preferred — the after-claim's "scored at close" leg then closes in-round);
or (b) integrate now with the verdict table's calibration cell stating
"scorer note pending at integration; per-probe receipts landed; N findings
recorded" — which is truthful but leaves proxy (a)'s "scored at close" half
open, and the LOG/SCORECARD entries must say so rather than imply the
aggregate exists. Option (b) repeats the r12 shape the calibration rubric
penalises; this scribe's reading is that (a) is the only option that pays
the round its calibration claim.
