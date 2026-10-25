# attrib-r21 — frozen feature table, blind cascade-leg attribution

Seat: instrument-impl, kengaku round 21 (zai flash wave). Registered claim N1:
**before** — no instrument exists that can attribute which cascade leg served a
given response without operator-side ground truth; **after** — a frozen
feature-table instrument (latency band / header tells / error-wording shape /
body schema — weights below, sha-frozen BEFORE any trial) attributes the
serving leg over >=20 blind trials per shim at accuracy >= the frozen bar
(0.80), scored against the shim journal ground truth read ONLY after the
trials complete.

## 0. Scope (honest novelty boundary)

Instrument + GT protocol only. Latency fingerprinting as a *phenomenon* is
priced OUT of novelty by the round-20 scout (LLMmap 2508.09021, Model Equality
Testing ICLR 2025, AdaptPrint, 2605.29979, 2411.01076, 2412.15431, 2409.20002,
2605.14786 — crowded published space). What is registered here is the
instrument and its ground-truth ordering discipline on THIS fleet's shims, not
a new phenomenon. No serving-plane claims are made or absorbed
(`../mori-shokunin/PROVINCE.md` boundary: mori reads journal events as fleet
evidence; endpoint/model-serving health is out of this lane's remediation
reach entirely — this seat sends small localhost requests and reads the
journal read-only, nothing more).

## 1. Machine table (the sha-pinned block; consumed by `plans/attrib_probe.py`)

```attrib-feature-table-v1
{
  "version": "attrib-feature-table-v1",
  "round": 21,
  "seat": "instrument-impl",
  "claim_scope": "instrument-level blind cascade-leg attribution with shim-journal ground truth; phenomenon-incremental",
  "bar": {"metric": "accuracy", "min": 0.8, "min_scored_trials_per_shim": 20},
  "request_budget_per_shim": {
    "setup_health_gets": 1,
    "standard_trials": 20,
    "error_path_trials": {"ds-flash-shim": 0, "glm-flash-shim": 2}
  },
  "trial_protocol": {
    "spacing_min_s": 2.0,
    "planned_spacing_s": 2.5,
    "requests_per_trial_step": 1,
    "client_timeout_s": 60,
    "retries": "none — one attempt per trial; a timeout/connection error is recorded as the outcome and excluded from the accuracy denominator",
    "auth": "no Authorization header (shims need no caller auth, r19 G7 code-read receipt); localhost only; no credential file is read",
    "standard_body": {"keys_order": ["model","messages","max_tokens","stream","stream_options"], "content": "Count from 1 to 30, space separated, numbers only. No other text.", "max_tokens": 16, "stream": true, "stream_options": {"include_usage": true}, "note": "the r19 P4 shape; 233 bytes with glm-5.3-flash per probe-r19-P4-glm.log"},
    "error_path_body": {"basis": "r19 F-2: the devin leg 400-rejects temperature (terminal in the glm cascade), so standard_body + temperature:0 forces the error-wording path; on ds no error path is forceable (temperature body is servable on leg-1 alibaba per the devinleg corroborating receipt; the content filter did not trigger on an innocuous prompt in S5) — ds error_path_trials = 0", "trials": 2},
    "blind_rule": "the trials phase NEVER reads journalctl or any GT source; enforcement is structural — the string journalctl occurs in plans/attrib_probe.py only inside cmd_score; the score phase runs only after ALL trials of both shims"
  },
  "gt_protocol": {
    "source": "journalctl --user -u <unit> --since @epoch --until @epoch, read once after all trials",
    "match_rule": "journal REQUEST line with bytes == len(trial_body) and epoch in [t0-0.5s, t0+3.0s]; zero candidates widens once to +/-5s; still zero -> UNMATCHED (excluded from denominator); >1 -> GT-AMBIGUOUS (excluded, recorded)",
    "served_leg_rule": "the OK leg line for the matched rid; else on ALL LEGS FAILED the highest-numbered FAIL leg — the shim's own returning-last-leg relay semantics (r19 finding 5, probe-r19-P4-glm.log; S8b scratch control, probe-r19-shim-ds-run.log)",
    "exclusions": "UNMATCHED / AMBIGUOUS / NO-LEG-LINES trials are reported in the receipt and excluded from the accuracy denominator"
  },
  "weights": {
    "hdr_tells": 3.0,
    "model_echo": 2.0,
    "usage_tells": 2.0,
    "error_tells": 3.0,
    "prompt_tokens_band": 1.0,
    "wall_band": 1.0,
    "id_class": 1.0,
    "stream_span_class": 0.5
  },
  "decision_rule": "score(L) = sum_f w_f * x_f(L); tell-set features: x = matched(L) / max_matched over legs (0 if max=0); class features: x = 1 if observed equals L's frozen expectation else 0; band features: x = 1 if observed within L's frozen band else 0; features that cannot fire (status 200 for error_tells; absent usage for prompt band/usage tells; non-stream for span class) contribute 0 to every leg; prediction = argmax score, ties broken by roster order (earlier leg wins); confidence = S_top / sum(S) (0 if sum=0); special rule: on a non-200 response with zero error-tell matches for EVERY leg, predict the roster-LAST leg (the shim's status-masking relay, frozen from r19 receipts)",
  "mimicry_protocol": {
    "scope": "offline ablations on collected trial features ONLY — this seat cannot pad the legs' real profiles (serving plane is operator-side, out of province); ablations lower-bound robustness to profile padding",
    "ablations": ["leave-one-out per feature", "mimicry:header-strip (hdr_tells + id_class zeroed — a header-normalizing padding adversary)", "mimicry:latency-pad (wall_band zeroed)", "mimicry:echo-spoof (model_echo zeroed — a leg adopting another leg's model name)"],
    "honest_read": "if header-strip accuracy falls below the bar, the finding is that attribution rests on header relaying and does NOT yet survive full feature padding — reported, not hidden"
  },
  "shims": {
    "ds": {
      "port": 8791,
      "unit": "ds-flash-shim",
      "model": "deepseek-v4.1-flash",
      "legs": ["alibaba-token-plan", "hyper", "opencode-go"],
      "roster_source": "GET /health 2026-10-16T10:10:54Z (this round's setup read, byte-matches r19 S7)",
      "leg_profiles": {
        "alibaba-token-plan": {
          "hdr_tells": ["server:istio-envoy", "x-envoy-upstream-service-time", "req-cost-time", "req-arrive-time", "resp-start-time", "grpc-encoding", "grpc-accept-encoding"],
          "model_echo": "requested",
          "usage_tells": ["usage:text_tokens"],
          "prompt_tokens_band": [38, 58],
          "wall_band_s": [0.8, 4.0],
          "stream_span_class": "burst",
          "id_class": ["chatcmpl-uuid", "eq-x-request-id"],
          "error_tells": ["data_inspection_failed"],
          "evidence": "headers/id/echo/usage S1+S2 (probe-r19-shim-ds-run.log:35-51,60-83); wall S1 1.816s S5 1.478s journal 1.244-3.409s; prompt 48 for this exact prompt per the excluded-but-corroborating devinleg ds receipt (SCORECARD r19 RA-3c); span 0ms per r19 battery finding 4; data_inspection_failed marker per S8a scratch mechanism test"
        },
        "hyper": {
          "hdr_tells": ["server:google-frontend", "x-ratelimit-limit-day", "x-ratelimit-remaining-day", "transfer-encoding:chunked"],
          "model_echo": "requested",
          "usage_tells": ["usage:hypercredits", "usage:cost"],
          "prompt_tokens_band": [38, 58],
          "wall_band_s": [0.7, 3.0],
          "stream_span_class": "incremental",
          "id_class": [],
          "error_tells": [],
          "evidence": "hyper direct-lane receipt (probe-r19-hyper.log): server=Google Frontend + x-ratelimit-* headers; echo exact (H3); usage cost/hypercredits; prompt 48 (H5); 1485ms POST, first_decoded 1308ms; span 145ms incremental (H8); id format unobserved -> empty id_class (feature cannot fire for this leg)"
        },
        "opencode-go": {
          "hdr_tells": ["server:cloudflare", "cf-ray", "cf-placement", "x-opencode-log-id", "x-opencode-endpoint-id", "x-opencode-upstream-model-id", "x-zen-model"],
          "model_echo": "requested",
          "usage_tells": [],
          "prompt_tokens_band": [38, 58],
          "wall_band_s": [1.0, 6.5],
          "stream_span_class": "incremental",
          "id_class": ["chatcmpl-uuid"],
          "error_tells": [],
          "evidence": "P7 direct-lane receipt (probe-r19-opencode-health.log): cloudflare/CF-RAY/Cf-Placement/x-opencode-*/x-zen-model headers; echo exact (7b); prompt 48 (7c); TTFT 1724ms (7d) and 3356/4958ms r18 M6 -> band [1.0,6.5]; span class incremental inferred from first_decoded 1724 vs elapsed 1927 (n=1, marked inferred); id chatcmpl-uuid inferred OpenAI shape (marked inferred)"
        }
      }
    },
    "glm": {
      "port": 8793,
      "unit": "glm-flash-shim",
      "model": "glm-5.3-flash",
      "legs": ["zai", "devin", "hyper"],
      "roster_source": "GET /health 2026-10-16T10:10:56Z (this round's setup read, byte-matches r19 4c v2)",
      "leg_profiles": {
        "zai": {
          "hdr_tells": ["x-log-id", "ga-traceid", "set-cookie", "alt-svc"],
          "model_echo": "requested",
          "usage_tells": ["usage:cached_tokens"],
          "prompt_tokens_band": [24, 36],
          "wall_band_s": [1.0, 5.5],
          "stream_span_class": "burst",
          "id_class": ["date-prefixed", "eq-x-log-id"],
          "error_tells": [],
          "evidence": "zai-leg serve receipt (probe-r19-P4-glm.log v2 2/2): z.ai header family X-LOG-ID/X-Request-ID/ga-traceid/Set-Cookie/Alt-Svc; echo glm-5.3-flash; usage prompt_tokens_details.cached_tokens; prompt 30 (battery 4f exact); journal leg serve 2.097s and 4.968s -> band [1.0,5.5]; span 0ms burst (5b); chunk id == X-LOG-ID value, 25-char date-prefixed; error body unobserved through the shim (leg-1 never last) -> empty error_tells"
        },
        "devin": {
          "hdr_tells": ["server:devin-openai-shim/2"],
          "model_echo": "rewritten:glm-5-3-flash-max",
          "usage_tells": [],
          "prompt_tokens_band": [326, 488],
          "wall_band_s": [0.3, 2.5],
          "stream_span_class": "burst",
          "id_class": [],
          "error_tells": ["devin_shim_error", "invalid_argument", "trace ID:"],
          "evidence": "devin-leg serve+error receipts (probe-r19-shim-glm-run.log attempt 1/2, probe-r19-P4-glm.log attempts 1/2): Server devin-openai-shim/2; model id rewritten glm-5-3-flash-max (G2); error body type devin_shim_error code invalid_argument with trace-ID message; prompt 407 for this exact prompt -> band +/-20%; journal serve 0.567s, cascade wall 1.737s after zai 429 -> band [0.3,2.5]; span 0.033ms burst; id format unobserved -> empty id_class. Caveat frozen: server:devin-openai-shim/2 may be the shim's own header on the error path rather than a relayed upstream header — it co-occurs with devin-leg responses in every r19 receipt either way; the trials adjudicate"
        },
        "hyper": {
          "hdr_tells": ["server:google-frontend", "x-ratelimit-limit-day", "x-ratelimit-remaining-day", "transfer-encoding:chunked"],
          "model_echo": "requested",
          "usage_tells": ["usage:hypercredits", "usage:cost"],
          "prompt_tokens_band": [38, 58],
          "wall_band_s": [0.7, 3.0],
          "stream_span_class": "burst",
          "id_class": [],
          "error_tells": [],
          "evidence": "hyper lane profile shared with the ds leg (probe-r19-hyper.log) for headers/usage/prompt-billing (same COUNT_PROMPT text bills 48 on hyper's tokenizer, H5 — marked inferred for glm-5.3-flash); stream_span_class burst per census ANALYSIS.md:193/:208 (the burst row WAS measured on glm-5.3-flash; H8's incremental falsification was hyper+deepseek — per-model property, r19 finding 4; marked unverified post-redeploy)"
        }
      }
    }
  }
}
```
``

## 2. Human summary of the frozen rule

Eight features, additive: header-tell families (weight 3.0) and error-wording
shape (3.0, fires only on non-200) carry the instrument; model-echo class and
usage-schema quirks (2.0 each) corroborate — including the devin leg's model-id
rewrite `glm-5.3-flash` -> `glm-5-3-flash-max` and its ~407-token billing of
the fixed prompt vs zai's 30; latency band, prompt-token band and id coupling
(1.0 each) are weak corroborators (bands overlap — that is the honest
expectation, since latency fingerprinting alone is a crowded, weak
space); stream span class (0.5) separates the burst legs
(alibaba/zai/devin) from the incremental ones (hyper; opencode inferred).
Model self-name is deliberately near-worthless alone on ds (all three legs
echo the requested name) — exactly the claim's framing; it earns weight only
through the devin rewrite class.

The decision rule is argmax over per-leg additive scores with frozen tie-break
(roster order) and the frozen status-masking fallback (non-200 with no
matchable error wording -> roster-last leg).

## 3. Trial protocol (frozen)

Per shim: 1 setup `GET /health` (zero quota, done 10:10:54/56Z before this
freeze), then 20 standard blind trials (fixed r19-P4-shape body, 16 output
tokens, stream, no temperature, no Authorization header), plus 2 error-path
trials on glm only (same body + `temperature: 0` — forceable only there, r19
F-2). One request per trial step, >=2.5 s spacing, 60 s client timeout, no
retries. 21 requests ds + 23 requests glm total, all small, all localhost.
Trials phase reads NO ground truth. After BOTH shims' trials complete, one
journal read per shim unit scores every trial via the frozen match rule.

## 4. Freeze discipline (the r19 lessons, applied)

- The pin covers exactly the fenced block in §1 (start fence line through end
  fence line inclusive). The FROZEN line below was appended AFTER hashing, so
  appending can never invalidate the pin (unlike r19's above-anchor edits).
- Double-read guard: two reads >=2 s apart, hashes recomputed each time, both
  must equal the pinned sha (r19 BR-1 repair ritual).
- `plans/attrib_probe.py trials` re-verifies the pin and records
  `frozen_sha256_at_start` in the receipt BEFORE the first request; mismatch
  exits 2 with nothing sent (r19 DEFECT-0 lesson: enforcement in code).
- No verification command is quoted inside the hashed block (r19 defect 2:
  a sed pattern that self-matches its own command text).

## 5. Known limits at freeze time (recorded, not hidden)

- No live r19 receipt observed a ds-shim FALLBACK serve (leg-2/leg-3 through
  :8791) — header-relay behaviour on those paths is unverified; the trials
  reveal it and the GT scoring adjudicates it.
- The glm roster's hyper leg is the least-measured profile (two values marked
  inferred in-table).
- zai 429 body wording through the shim is unobservable (leg-1 is never the
  relay source), so zai attribution under error relays is out of the frozen
  rule's reach by construction.
- If zai serves all glm trials (no 429 window), glm GT collapses to one leg —
  per-leg GT counts are reported and 0-GT legs are named UNTESTED.

## 6. Freeze record

FROZEN: 2026-10-16T10:20:08Z sha256:9f0244bb0aa4463c66981e5758a9a368ea0f0ea61b26882925f3ce7bbe6ba33c

Closing double-read verification: 2026-10-16T10:35:00Z-window both reads sha256 9f0244bb0aa4463c66981e5758a9a368ea0f0ea61b26882925f3ce7bbe6ba33c — block untouched since freeze; trials verified the same pin at start (recorded frozen_sha256_at_start in both receipts).
Erratum: the prior closing line labelled the double-read window "2026-10-16T10:35:00Z-window" — a drafting placeholder. The closing double-read actually ran at 2026-10-16T10:28:22Z (FREEZE-CHECK reads=2 stable=True -> OK, exit 0); the sha256 and the untouched-block conclusion are unchanged.

### 6.1 Freezer-seat audit record (append-only; freezer seat, 2026-10-16T10:37Z-window)

Independent verification by the wave's feature-freezer/gatekeeper seat (the seat
that was dispatched to author this freeze; the instrument-impl seat had already
landed and frozen it at 10:20:08Z, so this seat verified instead — recorded, not
adjudicated):

- Pin: `python3 plans/attrib_probe.py block-sha` →
  `9f0244bb0aa4463c66981e5758a9a368ea0f0ea61b26882925f3ce7bbe6ba33c` == the
  FROZEN line (recomputed ~10:31Z); `freeze-check --double-read` → reads=2,
  stable=True -> OK, exit 0 (independent of the 10:28:22Z closing read above).
- Ordering audit over ALL FOUR receipt files on disk at audit time — no trial
  predates the freeze; every receipt records
  `frozen_sha256_at_start == 9f0244bb…`:

  | receipt | first_request_utc | last_request_utc | trials | gate |
  |---|---|---|---|---|
  | corpus/evidence/attrib-r21-impl-ds-trials.log | 10:21:04Z | 10:22:20Z | 20 std | PASS (post-freeze) |
  | corpus/evidence/attrib-r21-glm-trials.log | 10:21:42Z | 10:24:04Z | 20 std + 2 err | PASS (post-freeze) |
  | corpus/evidence/attrib-r21-impl-glm-trials.log | 10:22:32Z | 10:24:43Z | 20 std + 2 err | PASS (post-freeze) |
  | corpus/evidence/attrib-r21-ds-trials.log | 10:23:45Z | 10:25:01Z | 20 std | PASS (post-freeze) |

  Pre-freeze host reads by the impl seat: two zero-quota `GET /health` setup
  calls (10:10:54/56Z), disclosed in-table (§1 roster_source) — setup, not
  trials. Blind rule held: the first GT read is the impl-ds score phase at
  10:25:25Z, which postdates the last request of all four runs (10:25:01Z,
  owned-ds) — the frozen blind_rule clause ("the score phase runs only after
  ALL trials of both shims") is met by both score phases (10:25:25Z ds,
  10:27:03Z glm).
- SCORING DEFECT (root-caused by this seat, post-trial diagnostic journal read,
  no lane files touched): the impl-ds score phase (10:25:25Z) recorded 20/20
  EXCLUDED:UNMATCHED -> ACCURACY 0/0 FAIL, but the journal data in its window
  is exact — 20 REQUEST lines, all `bytes=221` (== the trials' body_len), all
  leg lines present, epochs matching trial t0s (verified read-only at
  ~10:36Z). Cause: the score phase ran with instrument bytes sha256
  `b3e18c78…` (the sha pinned in all four receipts) whose `parse_ts` computed
  `(dt - delta).timestamp()` — on this -0300 host the naive `.timestamp()`
  re-applies the local offset, landing journal epochs +10800 s off (measured:
  07:21:04-0300 → 13:21:04Z instead of 10:21:04Z), outside every ±3 s/±5 s
  match window. The instrument was edited at 10:26:44Z (current sha256
  `effa7ea7ba582e9273433f0fa5da266a7ff527ac2e58b367bfb2b4d958983e56`); the fix
  computes epoch as `(utc_naive - datetime(1970,1,1)).total_seconds()`. The
  impl-glm score phase (10:27:03Z) ran after the edit and matched 22/22.
  Consequence: the impl-ds FAIL is an instrument-clock defect, not a
  ground-truth failure; re-scoring that run's recorded features with the fixed
  bytes is lawful under the frozen protocol (features and predictions are
  already in the receipt; the table is unchanged) — the scorer owns that call.
- Recorded, not adjudicated (for the scorer): (a) four receipt files exist
  where the round contract named two — the `-impl-` pair duplicate the owned
  pair against the same shims (r19 RA-4 ii duplicate-coverage precedent);
  (b) all four receipts pin instrument sha `b3e18c78…` as the bytes that RAN
  the trials, while the score phases run `effa7ea7…` — the scorer should
  record which scoring-path bytes each GT section used; (c) the impl-glm GT
  covers 2 of 3 roster legs (zai 13, devin 9, hyper 0 = UNTESTED), so the
  1.000 PASS is a two-leg accuracy, per the table's own honesty note.
