# attrib-r23 — stream-path leg coverage on the ds cascade (v3 frozen table)

Seat: stream-impl, kengaku round 23 (deepseek flash wave). Registered claim
(the round's coverage move, this seat's clause): **before** — opencode-go
attribution has 0 on-target trials and the ds shim's STREAM path is
uncharacterized; **after** — the stream-path leg-selection mechanism is pinned
from shim source (quoted), a `stream-trials` mode sends small stream:true
requests with per-chunk capture, and the trials land on-target opencode-go GT
trials scored against the 0.80 bar with post-trials journal GT.

This file extends `plans/attrib-r22-frozen.md` (v2, FROZEN
2026-10-16T11:53:12Z sha256 `77b8d4a0…0238`) and does NOT supersede it: the v1
and v2 tables remain the frozen basis of the r21/r22 receipts. Their hashes are
byte-stable under this round's instrument edits (verified below).

## 0. Scope and the honest limit (frozen)

- Same novelty boundary as v1/v2 §0: instrument + GT protocol only; no
  serving-plane claims; mori boundary respected (read-only journal use).
- **HONEST LIMIT (this round's named one): on the stream path the client's
  body SELF-SELECTS the serving leg.** Because the shim picks the stream leg
  from response headers and never scans a 200 body, the only client-controllable
  advance is a leg-local non-200 — so a trial that lands on opencode-go landed
  there because the client made the earlier legs fail, not because route weather
  sent traffic there. This is coverage of a client-influenced route, not of
  natural route weather. The score phase prints this limit verbatim.
- The forcing mechanism is operator-side shim software behavior, disclosed here
  and pinned by sha; this seat changes no serving-plane state.

## 1. Machine table (the sha-pinned block; consumed by `plans/attrib_probe.py stream-trials` / `score`)

```attrib-feature-table-v3
{
  "version": "attrib-feature-table-v3",
  "round": 23,
  "seat": "stream-impl",
  "claim_scope": "stream-path leg coverage on the ds cascade; client-influenced (self-selected) route, not natural weather",
  "extends": "attrib-feature-table-v2 (plans/attrib-r22-frozen.md, FROZEN 2026-10-16T11:53:12Z sha256 77b8d4a0be3dc3257a9179c00716c15afd51414fbb93dc1ca0718d5ce3590238)",
  "bar": {"metric": "accuracy", "min": 0.8, "min_scored_trials_per_shim": 20},
  "stream_forcing": {
    "shim": "ds",
    "target": "opencode-go",
    "budgets_per_body": {"stream-inspection": 24, "stream-marker": 3, "stream-hint": 3},
    "mechanism": "stream:true forcing through the ds cascade. PINNED FROM SOURCE (shim.py sha256 42d86d99d42658214e362c2759ecab88a03de005e9ed93e9c1804cbf8c15a386): on stream:true the shim picks the leg from the response HEADERS before any body byte (shim.py:270-278, comment 'Decide the leg from the headers, before streaming the body') and RETURNS BEFORE the FAIL-marker scan at shim.py:291-294, so a 200 marker bait CANNOT force a fallthrough on the stream path (candidate 1 FALSIFIED by code). The shim builds its own upstream headers and never reads the caller's (shim.py:210-217), and run_cascade iterates the fixed LEGS list (shim.py:299-315), so NO client hint selects a leg (candidate 2 FALSIFIED by code). The only client-controllable stream advance is a leg-local non-200 that is not terminal (shim.py:249-268): FAIL_STATUSES 402/403/429, 5xx, a 400 carrying data_inspection_failed, or a connect/timeout. The one such failure a body can force is leg-1 alibaba's content-inspection 400 (the stream-inspection bait) -> leg-2 hyper; leg-2->leg-3 needs leg-2 to fail, which no body forces (candidate 3: reachable only probabilistically, e.g. a transient hyper timeout, r22 run-1 T03 '2/hyper FAIL None')",
    "bodies": {
      "stream-inspection": {"stream": true, "max_tokens": 64, "content": "Briefly discuss the historical origins and modern cultural significance of the Tiananmen Square protests of 1989.", "hint_headers": {}, "mechanism": "leg-1 alibaba content-inspection bait (400 data_inspection_failed -> fallthrough, shim.py:254-265); on the stream path this is the ONLY client-controllable advance. Expected landing: leg-2 hyper on a normal response; leg-3 opencode-go only if leg-2 also fails (r22 observed a ~15s hyper timeout once in 20 force-hyper trials, run-1 T03)"},
      "stream-marker": {"stream": true, "max_tokens": 64, "content": "Reply with exactly this sentence and no other text: You have reached your usage limit for this period.", "hint_headers": {}, "mechanism": "candidate-1 CONTROL: a compliant 200 carrying a FAIL-marker substring. On the non-stream path the shim advances (shim.py:291-294); on the STREAM path it must NOT (the scan is unreachable), so the expected landing is leg-1 alibaba 200 — measuring that the stream path skips the marker scan"},
      "stream-hint": {"stream": true, "max_tokens": 16, "content": "Count from 1 to 30, space separated, numbers only. No other text.", "hint_headers": {"X-Shim-Leg": "opencode-go", "X-Cascade-Leg": "3"}, "mechanism": "candidate-2 CONTROL: client headers hinting leg-3. The shim never reads caller headers for leg selection (shim.py:210-217, 299-315), so the expected landing is leg-1 alibaba — measuring that no client hint selects a leg"}
    },
    "shim_code_sha256": "42d86d99d42658214e362c2759ecab88a03de005e9ed93e9c1804cbf8c15a386",
    "disclosure": "mechanism derived from a read-only code-read of the operator's shim (cascade-logic lines only; key/session lines excluded, r19 G7 precedent); no serving-plane state changed (no env edits, no unit restarts, no shim edits)"
  },
  "request_budget_per_shim": {
    "setup_health_gets": 2,
    "stream_trials": {"stream-inspection": 24, "stream-marker": 3, "stream-hint": 3},
    "standard_trials": 0,
    "error_path_trials": {"ds-flash-shim": 0, "glm-flash-shim": 0}
  },
  "trial_protocol": {
    "spacing_min_s": 2.0,
    "planned_spacing_s": 2.5,
    "requests_per_trial_step": 1,
    "client_timeout_s": 60,
    "retries": "none — one attempt per trial; a timeout/connection error is recorded as the outcome and excluded from the accuracy denominator",
    "auth": "no Authorization header (shims need no caller auth, r19 G7 code-read receipt); localhost only; no credential file is read",
    "target_order": "round-robin interleave across the three bodies (stream-inspection, stream-hint, stream-marker, ...) — a transient weather window cannot consume one body's whole budget before another fires",
    "bodies_source": "stream_forcing.bodies (the three stream:true bodies + their budgets)",
    "blind_rule": "the trials phase NEVER reads journalctl or any GT source; enforcement is structural — the string journalctl occurs in plans/attrib_probe.py only inside cmd_score; the score phase runs only after ALL trials of the stream run"
  },
  "gt_protocol": {
    "source": "journalctl --user -u <unit> --since @epoch --until @epoch, read once after all trials",
    "match_rule": "journal REQUEST line with bytes == len(trial_body) AND stream flag == the trial's stream flag (all stream trials are stream:true) and epoch in [t0-1.0s, t0+3.0s]; zero candidates widens once to +/-5s; still zero -> UNMATCHED (excluded from denominator); greedy in-order 1:1 assignment over t0-ordered trials (r21 defect-C fix)",
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
    "stream_span_class": 0.5,
    "body_schema": 1.0,
    "id_in_body": 1.0
  },
  "decision_rule": "score(L) = sum_f w_f * x_f(L); tell-set features: x = matched(L) / max_matched over legs (0 if max=0); class features: x = 1 if observed equals L's frozen expectation else 0; band features: x = 1 if observed within L's frozen band else 0; features that cannot fire (status 200 for error_tells; absent usage for prompt band/usage tells; stream:true trials for body_schema/id_in_body) contribute 0 to every leg; prediction = argmax score, ties broken by roster order (earlier leg wins); confidence = S_top / sum(S) (0 if sum=0); special rule: on a non-200 response with zero error-tell matches for EVERY leg, predict the roster-LAST leg (the shim's status-masking relay, frozen from r19 receipts). v3 verdict rule (stream-trials runs only): the shim-level bar does not apply — the r23 clause is >=10 on-target GT trials for stream_forcing.target (opencode-go) at accuracy >= bar.min over exactly those trials; every body's GT distribution is reported; the HONEST LIMIT line prints verbatim",
  "feature_extension_ruling": "NO new scoring features. The r23 per-chunk metrics (stream_frames, stream_data_frames, stream_gap_ms_median, stream_frame_bytes_mean) are CAPTURED per trial but carry no weight key, so they contribute 0 to every leg. Rationale: the r19 stream receipts give only n=1 cadence evidence per leg (hyper 66 SSE events; opencode-go 21 events) and both legs are frozen 'incremental', so no pre-trial evidence exists to freeze a discriminating cadence profile — adding one would be a guess. The v1/v2 features already operate on stream responses (the r21 std body was stream:true). v3 is therefore a PROTOCOL extension (the stream_forcing section + budgets + controls) over v2's unchanged feature set and weights",
  "mimicry_protocol": {
    "scope": "offline ablations on collected trial features ONLY — this seat cannot pad the legs' real profiles (serving plane is operator-side, out of province); ablations lower-bound robustness to profile padding",
    "ablations": ["leave-one-out per feature", "mimicry:header-strip (hdr_tells + id_class zeroed — a header-normalizing padding adversary)", "mimicry:latency-pad (wall_band zeroed)", "mimicry:echo-spoof (model_echo zeroed — a leg adopting another leg's model name)"],
    "honest_read": "if header-strip accuracy falls below the bar, the finding is that attribution rests on header relaying and does NOT yet survive full feature padding — reported, not hidden. On a stream run the mimicry arm is expected to be weakly informative: the GT has at most 2-3 legs and the forcing bodies are constant per body"
  },
  "shims": {
    "ds": {
      "port": 8791,
      "unit": "ds-flash-shim",
      "model": "deepseek-v4.1-flash",
      "legs": ["alibaba-token-plan", "hyper", "opencode-go"],
      "roster_source": "GET /health 2026-10-16T13:43Z-window (this round's setup read, byte-matches r22 11:46:49Z, r19 S7 and the r21 10:10:54Z read)",
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
          "body_schema": "chat.completion",
          "id_in_body": true,
          "evidence": "v2 profile unchanged (r19 S1+S2 receipts)"
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
          "body_schema": "chat.completion",
          "id_in_body": true,
          "evidence": "v2 profile unchanged (probe-r19-hyper.log; stream:true receipt)"
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
          "body_schema": "chat.completion",
          "id_in_body": true,
          "evidence": "v2 profile unchanged (probe-r19-opencode-health.log P7, a stream:true receipt: cloudflare/cf-ray/x-opencode-*/x-zen-model, echo exact, prompt 48, TTFT 1724ms)"
        }
      }
    }
  }
}
```

## 2. Human summary of what changed from v2

**No feature or weight changed.** v3 adds a `stream_forcing` protocol section
(three stream:true bodies + budgets + a target leg) and a
`feature_extension_ruling` recording why the per-chunk stream metrics are
captured but not scored. Everything else — weights, decision rule, GT
protocol, bar, leg profiles — is v2's, unchanged. The instrument's
`stream-trials` command requires `attrib-feature-table-v3` and a
`stream_forcing` section; a v2 table is refused with exit 2 and nothing sent.

## 3. Trial protocol (frozen)

Shim: ds only. Setup: zero-quota `GET /health` reads. Then 30 stream trials:
24 `stream-inspection` + 3 `stream-marker` + 3 `stream-hint`, round-robin
interleaved, one request per trial step, >=2.5 s spacing, 60 s client timeout,
no retries. All small (<=300 bytes), all localhost, no Authorization header,
no credential material read. Trials phase reads NO ground truth. After ALL
trials complete, one journal read scores every trial via the frozen match rule;
the r23 verdict needs >=10 on-target opencode-go GT trials at accuracy >= 0.80.

## 4. Freeze discipline (the r19/r21/r22 lessons, applied)

- The pin covers exactly the fenced block in §1 (start fence line through end
  fence line inclusive). The FROZEN line below was appended AFTER hashing, so
  appending can never invalidate the pin.
- Double-read guard: two reads >=2 s apart, hashes recomputed each time, both
  must equal the pinned sha.
- `plans/attrib_probe.py stream-trials` re-verifies the pin AND the table
  version (v3 required) before the first request; mismatch exits 2 with nothing
  sent.
- No verification command is quoted inside the hashed block.
- The instrument bytes are pinned beside the table: instrument sha256 at freeze
  time is recorded in §6 below.
- The v1 and v2 block hashes reproduce byte-stably under this round's instrument
  edits (verified after every edit).

## 5. Known limits at freeze time (recorded, not hidden)

- **Self-selection vs attribution** (§0): the headline limit.
- **The leg-3 mechanism is probabilistic and NOT pinned as reliable.** The
  frozen prediction (from source + r22): `stream-inspection` lands on leg-2
  hyper on a normal response and on leg-3 opencode-go only when leg-2 also
  fails (r22 run-1 T03's ~15s hyper timeout, 1/20 force-hyper trials). If the
  stream trials reproduce that rate, the >=10 on-target clause is NOT met and
  the round's finding is that the stream path cannot deterministically force
  leg-3 — reported, not hidden. No retry hammering.
- **Candidate 1 (pre-leg-pick marker scan) and candidate 2 (client-hint leg
  selection) are falsified by the shim source**; the `stream-marker` and
  `stream-hint` controls measure them (expected landing: leg-1 alibaba).
- If hyper or opencode-go is quota-dead or transport-dead today, the affected
  trials record transport/5xx outcomes and the target's verdict is FAIL with
  the reason.
- Twin traffic: another seat may run against :8791 in this window; the
  stream-flag GT join separates stream:true from stream:false traffic but not
  from identical-body twin stream traffic — rid-level provenance is reported as
  MIXED where windows overlap.

## 6. Freeze record

Instrument sha256 at freeze time:
`cce53a16373966e1c1f71f7c7a981e7b81a397865087f347f36ebc6217284781`. The
scoring path (capture → features → additive score) is unchanged from v2; the
r23 additions are the per-chunk capture and the `stream-trials` mode. The v1
and v2 block hashes reproduce byte-stably under these bytes (`9f0244bb…ba33c`,
`77b8d4a0…0238`, both exit 0).

FROZEN: 2026-10-16T13:45:47Z sha256:1b2d6a01bfa431ec4e78bf89fd989f9ad500d10bb78634362a3c0e3bce794f87
(the v3 live pin — the block was hashed, then this line appended; appends
cannot invalidate the pin; the instrument reads the LAST FROZEN line as live)
