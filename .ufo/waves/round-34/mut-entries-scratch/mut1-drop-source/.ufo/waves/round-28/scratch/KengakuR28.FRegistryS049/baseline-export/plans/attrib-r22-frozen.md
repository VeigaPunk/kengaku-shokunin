# attrib-r22 — extended frozen feature table (v2), forced leg coverage on the ds cascade

Seat: leg-coverage-impl, kengaku round 22 (zai flash wave). Registered claim
(the round's operability/coverage move, this seat's clause): **before** — the
r21 instrument's attribution is validated only for the legs that naturally
serve (ds GT collapsed to alibaba-token-plan ×20; hyper and opencode-go took
0 GT trials and are named UNTESTED in the r21 record), and the instrument is
a one-off experiment rather than a standing probe type; **after** — (a)
forced-fallback trials land >=10 each on hyper and opencode-go through the ds
cascade with the extended feature table (RE-FROZEN before the trials, sha
below), accuracy vs the 0.80 bar scored against post-trials journal GT — with
the honest limit named that FORCED coverage is a different claim than natural
coverage; (b) the battery template + note gain probe-type P10 (battery-fold
seat's clause, not this file).

This file extends `plans/attrib-r21-frozen.md` (v1, FROZEN
2026-10-16T10:20:08Z sha256 `9f0244bb…ba33c`, trials-time instrument sha
`b3e18c78…`) and does NOT supersede it: the v1 table remains the frozen basis
of the r21 receipts. The v1 table's hash is byte-stable under the extended
instrument (`python3 plans/attrib_probe.py block-sha --frozen
plans/attrib-r21-frozen.md` → `9f0244bb…ba33c`, verified after every
instrument edit this round).

## 0. Scope and the honest limit (frozen)

- Same novelty boundary as v1 §0: instrument + GT protocol only; latency
  fingerprinting priced OUT of novelty by the r20 scout; no serving-plane
  claims; mori boundary respected (read-only journal use, no remediation).
- **HONEST LIMIT (the round's named one): FORCED coverage is a different
  claim than natural coverage.** The r21 glm GT split (zai 13 / devin 9) came
  from route weather (natural 429 windows); the r22 trials land on hyper /
  opencode-go because the forcing bodies make the earlier legs fail, not
  because route weather sent traffic there. What this establishes: the
  instrument's feature table discriminates those legs' REAL responses when
  they serve, scored against real journal GT. What it does not establish:
  that the legs serve at natural rates, or that natural fallback traffic
  looks like forced traffic. The score phase prints this limit verbatim.
- The forcing mechanism is operator-side shim software behavior, disclosed
  here and pinned by sha; this seat changes no serving-plane state (no env
  edits, no unit restarts, no shim edits).

## 1. Machine table (the sha-pinned block; consumed by `plans/attrib_probe.py force-trials` / `score`)

```attrib-feature-table-v2
{
  "version": "attrib-feature-table-v2",
  "round": 22,
  "seat": "leg-coverage-impl",
  "claim_scope": "forced-fallback leg coverage on the ds cascade (hyper, opencode-go) with the extended feature table; FORCED coverage is a different claim than natural coverage",
  "extends": "attrib-feature-table-v1 (plans/attrib-r21-frozen.md, FROZEN 2026-10-16T10:20:08Z sha256 9f0244bb0aa4463c66981e5758a9a368ea0f0ea61b26882925f3ce7bbe6ba33c)",
  "bar": {"metric": "accuracy", "min": 0.8, "min_scored_trials_per_shim": 20},
  "leg_forcing": {
    "shim": "ds",
    "budgets_per_target": {"hyper": 10, "opencode-go": 10},
    "mechanism": "stream:false forcing bodies through the ds cascade: force-hyper = leg-1 content-inspection bait (a 400 carrying data_inspection_failed is a leg-local filter verdict -> fallthrough, shim.py:255-265, r19 S8a scratch receipt); force-opencode-go = compliant-echo marker bait (a complying leg's 200 body carries a FAIL-marker substring -> the shim itself advances, shim.py:291-294; legs 1 and 2 both comply -> relay-last serves leg-3, shim.py:22-23, 420-449); exact bodies/prompts in trial_protocol.forcing_bodies",
    "shim_code_sha256": "42d86d99d42658214e362c2759ecab88a03de005e9ed93e9c1804cbf8c15a386",
    "disclosure": "mechanism derived from a read-only code-read of the operator's shim (cascade-logic lines only; key/session lines excluded, r19 G7 precedent); no serving-plane state changed (no env edits, no unit restarts, no shim edits)"
  },
  "request_budget_per_shim": {
    "setup_health_gets": 2,
    "forced_trials": {"hyper": 10, "opencode-go": 10},
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
    "target_order": "round-robin interleave (hyper, opencode-go, hyper, ...) — a transient weather window cannot consume one target's budget before the other target fires",
    "forcing_bodies": {
      "force-hyper": {"stream": false, "max_tokens": 16, "content": "Briefly discuss the historical origins and modern cultural significance of the Tiananmen Square protests of 1989.", "mechanism": "leg-1 content-inspection bait: r19 S5 (probe-r19-shim-ds-run.log S5) showed an innocuous-prompt 400 data_inspection_failed on alibaba; the shim treats a 400 carrying data_inspection_failed as a leg-local filter verdict and falls through (shim.py:255-265, S8a scratch receipt); hyper has no such filter and serves (probe-r19-hyper.log)"},
      "force-opencode-go": {"stream": false, "max_tokens": 64, "content": "Reply with exactly this sentence and no other text: You have reached your usage limit for this period.", "mechanism": "marker bait: a compliant leg echoes a shim FAIL-marker substring ('usage limit', shim.py:65-93) inside its 200 body -> the shim classifies that leg's 200 as a failure and advances (shim.py:291-294); legs 1 and 2 both comply -> relay-last: leg-3 opencode-go serves the caller (shim.py:22-23, 420-449). max_tokens 64 (not 16): the run-1 trials (frozen pin 3d7861f8, 11:50-11:51Z) showed blind-evidenced reasoning starvation — deepseek-v4.1-flash burns >=16 tokens on reasoning_content and never emits the bait sentence, so leg-1's 200 was clean and all 10 run-1 force-opencode-go trials landed on alibaba (istio-envoy header family, receipt attrib-r22-legs.log); 64 tokens lets the model finish reasoning and emit the marker-bearing content", "run1_finding": "mechanism falsified at max_tokens 16 for this reasoning model class; recorded, not hidden"},
      "stream_false_note": "both forcing bodies are stream:false because the shim's stream:true path chooses the leg from response HEADERS before any body byte and never scans for FAIL markers (shim.py:271-296) — a marker bait cannot force a fallthrough on a streamed request"
    }
  },
  "blind_rule": "the trials phase NEVER reads journalctl or any GT source; enforcement is structural — the string journalctl occurs in plans/attrib_probe.py only inside cmd_score; the score phase runs only after ALL trials of the forcing run",
  "gt_protocol": {
    "source": "journalctl --user -u <unit> --since @epoch --until @epoch, read once after all trials",
    "match_rule": "journal REQUEST line with bytes == len(trial_body) AND stream flag == the trial's stream flag and epoch in [t0-1.0s, t0+3.0s]; zero candidates widens once to +/-5s; still zero -> UNMATCHED (excluded from denominator); greedy in-order 1:1 assignment over t0-ordered trials (r21 defect-C fix); the stream-flag equality is new in v2 — the forcing bodies are the run's only stream:false requests, so their rids are separated from any interleaved stream:true traffic (r21 defect 7 hardening)",
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
  "decision_rule": "score(L) = sum_f w_f * x_f(L); tell-set features: x = matched(L) / max_matched over legs (0 if max=0); class features: x = 1 if observed equals L's frozen expectation else 0; band features: x = 1 if observed within L's frozen band else 0; features that cannot fire (status 200 for error_tells; absent usage for prompt band/usage tells; stream:true trials for body_schema/id_in_body/stream_span_class) contribute 0 to every leg; prediction = argmax score, ties broken by roster order (earlier leg wins); confidence = S_top / sum(S) (0 if sum=0); special rule: on a non-200 response with zero error-tell matches for EVERY leg, predict the roster-LAST leg (the shim's status-masking relay, frozen from r19 receipts). v2 verdict rule (force-trials runs only): the shim-level bar does not apply — per-target verdicts: target T PASSES iff >=10 of its trials were GT-served BY leg T and accuracy on exactly those trials >= bar.min; trials that landed elsewhere count in the coverage distribution, not the verdict; the HONEST LIMIT line prints verbatim",
  "mimicry_protocol": {
    "scope": "offline ablations on collected trial features ONLY — this seat cannot pad the legs' real profiles (serving plane is operator-side, out of province); ablations lower-bound robustness to profile padding",
    "ablations": ["leave-one-out per feature", "mimicry:header-strip (hdr_tells + id_class zeroed — a header-normalizing padding adversary)", "mimicry:latency-pad (wall_band zeroed)", "mimicry:echo-spoof (model_echo zeroed — a leg adopting another leg's model name)"],
    "honest_read": "if header-strip accuracy falls below the bar, the finding is that attribution rests on header relaying and does NOT yet survive full feature padding — reported, not hidden. On a forced run the mimicry arm is expected to be weakly informative: the GT has at most 2-3 legs and the forcing bodies are constant per target"
  },
  "shims": {
    "ds": {
      "port": 8791,
      "unit": "ds-flash-shim",
      "model": "deepseek-v4.1-flash",
      "legs": ["alibaba-token-plan", "hyper", "opencode-go"],
      "roster_source": "GET /health 2026-10-16T11:46:49.360Z (this round's setup read, zero-quota; byte-matches r19 S7 and the r21 roster_source read of 10:10:54Z)",
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
          "evidence": "v1 profile unchanged (r19 S1+S2 receipts); v2 adds body_schema/id_in_body from the r19 S5 non-stream capture (probe-r19-shim-ds-run.log S5: a 400 data_inspection_failed body) — marked INFERRED for 200-shape: the r19 S5 400 body is an error object, not a chat.completion, so the 200 non-stream shape is inferred OpenAI-standard (chat.completion, id in body) and the trials adjudicate"
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
          "evidence": "v1 profile (probe-r19-hyper.log) for headers/usage/echo/prompt-billing; v2 adds body_schema/id_in_body INFERRED OpenAI-standard for the non-stream 200 shape (unobserved non-stream through the shim; the trials adjudicate); stream_span_class stays v1's incremental but CANNOT FIRE on stream:false trials (feature contributes 0 to every leg)"
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
          "evidence": "v1 profile (probe-r19-opencode-health.log P7) for headers/echo/prompt/timing; v2 adds body_schema/id_in_body INFERRED OpenAI-standard (unobserved non-stream through the shim; the trials adjudicate); stream_span_class stays v1's incremental-inferred but CANNOT FIRE on stream:false trials"
        }
      }
    }
  }
}
```

## 2. Human summary of what changed from v1

Two new features (weight 1.0 each), both firing only on the forcing bodies'
stream:false responses: `body_schema` (the top-level `object` echo —
`chat.completion` vs anything else) and `id_in_body` (a string `id` at the
top level of the non-stream body). They exist because the forcing bodies are
non-stream, so the v1 stream-shape feature cannot fire, and the legs'
non-stream body schemas were never a frozen feature. Three profiles gain the
two new keys, all marked INFERRED for the 200 non-stream shape (the r19 S5
capture is a 400 error body; the trials adjudicate). Everything else —
weights, decision rule, GT protocol, bar — is v1's, plus the stream-flag
match-window hardening and the v2 per-target verdict rule (§1 decision_rule).

## 3. Trial protocol (frozen)

Shim: ds only (the forcing mechanism is defined on the ds cascade
alibaba->hyper->opencode-go; the instrument refuses other shims with exit 2).
Setup: 2 zero-quota `GET /health` reads (11:46:49.360Z above; an earlier
un-timestamped one in the same preparation window — both disclosed here).
Then 20 forced trials: 10 targeting hyper (force-hyper body) + 10 targeting
opencode-go (force-opencode-go body), round-robin interleaved, one request
per trial step, >=2.5 s spacing, 60 s client timeout, no retries. All small
(<=300 bytes), all localhost, no Authorization header, no credential material
read. Trials phase reads NO ground truth. After ALL trials complete, one
journal read scores every trial via the frozen match rule; per-target
verdicts need >=10 on-target GT trials each at accuracy >= 0.80.

## 4. Freeze discipline (the r19/r21 lessons, applied)

- The pin covers exactly the fenced block in §1 (start fence line through end
  fence line inclusive). The FROZEN line below was appended AFTER hashing, so
  appending can never invalidate the pin.
- Double-read guard: two reads >=2 s apart, hashes recomputed each time, both
  must equal the pinned sha (r19 BR-1 repair ritual).
- `plans/attrib_probe.py force-trials` re-verifies the pin AND the table
  version (v2 required) before the first request; mismatch exits 2 with
  nothing sent (r19 DEFECT-0 lesson: enforcement in code).
- No verification command is quoted inside the hashed block.
- The instrument bytes are pinned beside the table this round (r21 defect 2
  lesson): instrument sha256 at freeze time
  `34c4fa671828a7787844cc9b5ec656217aa74cab2c6a393b8b78b01a5049e062`, and
  every score block now records `instrument sha256 at scoring`.
  Erratum (2026-10-16T11:50Z-window): after freeze-2, the instrument gained
  one fix — `load_frozen` now reads the LAST FROZEN line as the live pin
  (needed because this file legitimately carries a superseded + a live
  FROZEN line; the first-match reading made the stale pin shadow the live
  one). Instrument sha256 at trials time:
  `05da8927b21d59e210108ec00ef20637e71ca57358894ea07758e53f9157c2d2`. The
  scoring path (capture → features → additive score) is unchanged; the
  r21 v1 table hash still reproduces under the new bytes
  (`9f0244bb…ba33c`, verified after the edit).

## 5. Known limits at freeze time (recorded, not hidden)

- **Forced vs natural** (§0): the headline limit, printed verbatim by the
  score phase.
- The forcing bodies' leg-1 outcomes are probabilistic: the inspection bait
  may NOT trip alibaba's filter (r19 S5's one benign live attempt did not
  trigger it — S5 is recorded NOT-EXERCISED in the r19 digest), and the
  marker bait may be refused by a leg's own filter or answered with a
  paraphrase that lacks the marker. Either way the trial lands where the
  cascade sends it and the GT adjudicates; the per-target verdicts measure
  what actually landed.
- The v2 profile keys (body_schema/id_in_body) are INFERRED for all three
  legs' 200 non-stream shapes; if a leg's real non-stream shape differs, the
  feature mis-votes 1.0 against that leg — the trials adjudicate.
- opencode-go's discrimination rests on relayed headers (cloudflare /
  x-opencode-*) surviving the shim's success-path relay; if the shim
  suppresses them on this path, opencode-go trials may tie with hyper and
  the roster tie-break would mis-attribute them — the GT scoring reveals
  exactly that, and it is a finding either way.
- If hyper or opencode-go is quota-dead or transport-dead today, the forced
  trials for that target record transport/5xx outcomes and the target's
  verdict is FAIL with the reason; no retry hammering (one attempt per
  trial).

## 6. Freeze record

FROZEN: 2026-10-16T11:47:59Z sha256:124ade675f73a3e87c19ab82560fcaab4bf5dbcdbf3beb98aa5a4b189c66583d

**SUPERSEDED before any request** (BR-1 repair ritual, r19 §7.1): the
11:47:59Z freeze was missing the top-level `leg_forcing` section the
instrument's gate reads; `force-trials` refused with exit 2 and NOTHING was
sent under that pin (verified: no receipt file was opened — the gate runs
before the receipt append). The section was added; the re-freeze below is
the live pin. The superseded hash is recorded as the identity of the
pre-repair bytes, never silently replaced.

FROZEN: 2026-10-16T11:53:12Z sha256:77b8d4a0be3dc3257a9179c00716c15afd51414fbb93dc1ca0718d5ce3590238
(the v2 live pin — freeze-3; supersedes the 11:47:59Z and 11:49:01Z pins
above; zero requests were sent under the 11:47:59Z pin, run-1 ran under the
11:49:01Z pin; the instrument reads the LAST FROZEN line as live)

**SUPERSEDED by freeze-3 (2026-10-16T11:53:12Z
sha256:77b8d4a0be3dc3257a9179c00716c15afd51414fbb93dc1ca0718d5ce3590238).**
Run-1 (20 forced trials, 11:50:06–11:51:50Z, under the 11:49:01Z pin) ran
clean and produced a mechanism falsification: the force-opencode-go marker
bait at max_tokens 16 starved the reasoning model (deepseek-v4.1-flash
spends its whole budget on reasoning_content and never emits the bait
sentence), so leg-1's 200 was clean and all 10 force-opencode-go trials
landed on alibaba-token-plan (blind-evidenced by the istio-envoy header
family in every record; no GT read needed). The force-hyper forcing worked:
9/10 landed on hyper, 1 (T03) overshot to opencode-go — bonus leg-3
coverage. Repair: force-opencode-go max_tokens 16 -> 64 (frozen-row change
in trial_protocol.forcing_bodies with the run1_finding recorded in-block);
force-hyper rows are byte-identical across freeze-2 and freeze-3 (only the
force-opencode-go row changed), so run-1's force-hyper trials stay scoreable
under the r19 RA-3 byte-identity rule. Run-1's GT scoring happens AFTER
run-2 completes (the blind rule spans both runs).

Closing double-read verification: two reads 2.5 s apart (11:47:59Z window),
both sha256 `124ade67…6583d`, stable=True — block untouched since freeze;
the FROZEN line was appended after hashing (appends cannot invalidate the
pin). Post-write recompute: `freeze-check --double-read` → reads=2,
block_sha=124ade675f73a3e8 pinned=124ade675f73a3e8 stable=True -> OK,
exit 0 (2026-10-16T11:48:0xZ window). The 11:47:59Z pin is SUPERSEDED by the
re-freeze above (zero requests sent under it).

## 7. Post-trials errata (append-only; below the anchor, pin untouched)

- **R22-1 (instrument defect, found post-run-2):** freeze-3 raised the
  force-opencode-go row's max_tokens 16 -> 64, but the instrument's
  `force_body()` hardcoded 16 and ignored the frozen row — run-2 (pin
  77b8d4a0…, instrument 05da8927…) replicated run-1's conditions exactly.
  Fixed after run-2 (`force_body` reads the frozen row; instrument sha
  bb6bd919…712c, verified against the table: opencode-go -> 64, hyper ->
  16); the fix ran no trial (budget spent). Lesson: a frozen-row change
  must ship in the instrument bytes the same round, or the freeze lies.
- **Carried gap (the claim's opencode-go clause):** NOT MET this round.
  On-target GT: hyper 19/19 = 1.000 across both runs (>=10 bar MET in
  run-2: 10/10 PASS); opencode-go 1/1 (run-1 T03, blind-predicted,
  GT-confirmed) — n=1, far below the >=10 bar. The mechanism is proven
  reachable (the diagnostic replay's full marker chain, rid 075335ff5c09:
  all three legs marker-FAIL -> relay-last opencode-go serves), but the
  bait's starve-then-emit race (deepseek-v4.1-flash reasoning budget vs
  max_tokens) makes it unreliable at 16 tokens and untested at 64 in a
  scored trial. The 44-call etiquette scale is spent (43 requests by this
  seat); the >=10-opencode-go clause carries to the next instantiation
  with the instrument fix already shipped.
- **Twin traffic (r21 defect-7 recurrence):** two other seats ran the same
  forcing protocol against :8791 inside this seat's windows
  (attrib-r22-legs-hyper.log — seat-labelled leg-coverage-impl, UNSCORED —
  and attrib-r22-opencode-trials.log — trial-runner-opencode, self-scored).
  The stream-flag GT-join hardening separates forcing rids from stream:true
  traffic but not from identical-body twin forcing traffic; greedy in-order
  assignment disambiguated this seat's joins (40/40 chain-consistent).
  Rid-level provenance is MIXED in the 11:50:58-11:52:26Z overlap window.
- **Scored results (this seat's authoritative blocks, receipt
  attrib-r22-legs.log):** run-1 ACCURACY 20/20 = 1.000 PASS (GT: hyper 9 /
  alibaba 10 / opencode-go 1); run-2 ACCURACY 20/20 = 1.000 PASS (GT:
  hyper 10 / alibaba 10; TARGET hyper 10/10 -> PASS). Ablations: hdr_tells
  LOO 17/20 (run-1) and 19/20 (run-2) — header relaying is load-bearing on
  this GT; header-strip mimicry 19/20 and 20/20; all other ablations
  1.000. The honest-limit line printed verbatim in both score blocks.
