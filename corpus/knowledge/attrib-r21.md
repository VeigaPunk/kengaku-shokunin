# attrib-r21 — blind cascade-leg attribution instrument: design, scored results, limits

Source basis: `plans/attrib-r21-frozen.md` (block anchor `FROZEN:
2026-10-16T10:20:08Z sha256:9f0244bb0aa4463c66981e5758a9a368ea0f0ea61b26882925f3ce7bbe6ba33c`,
file sha256 `43ac5132…cb732`) + `plans/attrib_probe.py` (trials-time sha
`b3e18c78…184b80`, pinned in all four receipt metas; landing-time sha
`effa7ea7…983e56`) + four trial receipts `corpus/evidence/attrib-r21-*.log`
+ the prior-art note `corpus/knowledge/attrib-prior-art-r21.md` (sha
`1e509faa…003e2`, landed 10:08:50Z) + the lessons entry
`corpus/lessons/2026-10-16-round21-attribution-freeze-surface.md` (sha
`27f7fd24…a15eb`). Starting commit `3688f76` (round-20 records); the wave
lands uncommitted per the no-commits rule.

**Provenance of this note (read first).** Finalized by the note-finalizer
seat 2026-10-16T11:10Z-window. The dispatch sequences this seat *after the
scorer lands*; the scorer's close-out (`corpus/knowledge/attrib-r21.md`,
this path) **had not landed at finalize time** — absent at every poll this
seat ran (10:41:31Z, 10:46:04Z, 10:49:52Z, 10:55:23Z, 11:02:41Z,
11:08:37Z; the scribe's drafts already track it pending with placeholders
at 10:47–10:48Z) — while every other seat's artifacts were on disk. This
note therefore composes the scored close-out **from landed receipt bytes
only**: every scored number below is quoted from a receipt's AUTHORITATIVE
block with its provenance; this seat ran **no journal read** (the only
ground-truth-derived numbers cited are the ones the impl seat's score
phases already landed) and sent **no request**. The two official runner
receipts (`attrib-r21-{ds,glm}-trials.log`) remain **unscored** at finalize
time — their score sections are still owed, and a later scorer close-out
supersedes this note wherever it disagrees.

## 0. The round's falsifiable claim, checked

Before (N1, pre-registered via the r20 novelty scout): no instrument exists
that can attribute which cascade leg served a given response without
operator-side ground truth.

After (claimed): a frozen feature-table instrument (latency band / header
tells / error-wording shape / body schema — weights pre-registered,
sha-frozen before any trial) attributes the serving leg over ≥20 blind
trials per shim at accuracy ≥ the frozen bar (0.80), scored against
shim-journal ground truth read only after the trials complete; mimicry
probes test whether attribution survives feature-profile padding; the
prior-art note scopes the novelty honestly.

Per clause:

- **Frozen before trials: YES.** Block pin `9f0244bb…` verified by this
  seat twice independently (`python3 plans/attrib_probe.py freeze-check
  --double-read` → reads=2, stable=True, exit 0, ~10:21:50Z; `block-sha`
  → same hash, exit 0, ~11:08Z), and by the freezer seat (~10:31Z) and the
  lessons seat (post-append re-check). All four receipts record
  `frozen_sha256_at_start == 9f0244bb…`, and every trial postdates the
  freeze (§2).
- **≥20 blind trials per shim: YES, doubled.** 84 blind trials across four
  receipt files (40 ds / 44 glm) against frozen budgets of 21/23 — the
  double execution is defect 1, but the per-shim clause is met twice over.
- **Accuracy ≥ the frozen bar: YES on the landed (scored) receipts** —
  ds **20/20 = 1.000** and glm **22/22 = 1.000**, both PASS
  (bar 0.80, min scored n 20) — with the reading bounded by §4/§8: the
  claim this supports is "attributes the legs that served" (alibaba-token-
  plan, zai, devin), not "attributes the roster" (hyper and opencode-go
  took 0 GT trials; §5 defect 5).
- **Journal GT read only after trials: YES.** First GT read 10:25:25Z
  postdates the last request of all four runs (10:25:01Z); the freezer's
  ordering audit (`plans/attrib-r21-frozen.md` §6.1) passes all four
  receipts, and both runner seats filed blind attestations (runner-A
  addendum item 4; runner-B addendum).
- **Mimicry probes: RAN, UNINFORMATIVE AS RUN** — all eleven ablations
  1.000 on both shims; an information-dependence lower bound, not a
  padding adversary (§4).
- **Prior-art scoping: YES** — INSTRUMENT-NOVEL, PHENOMENON-INCREMENTAL,
  9/9 arXiv primaries fetched HTTP 200 (§5).

## 1. Design (as frozen)

Eight features, additive per-leg scoring (`decision_rule`, frozen block):
header-tell families (w 3.0) and error-wording shape (w 3.0, fires only on
non-200) carry the instrument; model-echo class and usage-schema quirks
(2.0 each) corroborate — including the devin leg's model-id rewrite
`glm-5.3-flash` → `glm-5-3-flash-max` and its ~407-token billing of the
fixed prompt vs zai's 30; latency band, prompt-token band, and id coupling
(1.0 each) are weak corroborators (bands overlap by design — the round
prices latency fingerprinting as crowded prior art); stream span class
(0.5) separates burst legs from incremental ones. Decision: argmax with
frozen roster-order tie-break, confidence = S_top/ΣS, plus the frozen
status-masking fallback (non-200 with no matchable error wording →
roster-last leg, from the r19 relay-semantics receipts).

Trial protocol (frozen): per shim 1 zero-quota setup `GET /health` (done
10:10:54/56Z, before the freeze), then 20 standard blind trials (fixed
r19-P4-shape body, 16 output tokens, stream, no temperature, **no
Authorization header**), +2 error-path trials on glm only (`temperature:0`
forces the devin-leg 400 there and nowhere else — ds `error_path_trials=0`
as frozen). One request per trial step, ≥2.5 s spacing, 60 s timeout, no
retries; a transport error is recorded, not retried, and excluded from the
denominator. Blind rule in code: the string `journalctl` occurs in
`plans/attrib_probe.py` only inside `cmd_score`; `cmd_trials` refuses to
send unless the table pin verifies (mismatch → exit 2, nothing sent).

GT protocol (frozen): one `journalctl --user -u <unit>` read per shim after
ALL trials; trials join to journal REQUEST lines by body-length + time
window; served-leg rule = the matched rid's first OK leg, else on
ALL-LEGS-FAILED the highest-numbered FAIL leg (the shim's own
returning-last-leg relay semantics, r19 finding 5); UNMATCHED / AMBIGUOUS /
NO-LEG-LINES trials are reported and excluded from the denominator.

Freeze discipline (r19 lessons applied): the pin covers exactly the fenced
block; the FROZEN line was appended after hashing so appends cannot
invalidate it; double-read guard; no verification command inside the hashed
block; `cmd_trials` enforces the pin in code (the r19 DEFECT-0 lesson).

## 2. Ordering and blind gate

| run (seat) | window (UTC) | trials | gate |
|---|---|---|---|
| impl-ds (instrument-impl) | 10:21:04 → 10:22:20 | 20 std | PASS (post-freeze 10:20:08Z) |
| runner-B glm (`attrib-r21-glm-trials.log`) | 10:21:42 → 10:24:04 | 20 std + 2 err | PASS |
| impl-glm (instrument-impl) | 10:22:32 → 10:24:43 | 20 std + 2 err | PASS |
| runner-A ds (`attrib-r21-ds-trials.log`) | 10:23:45 → 10:25:01 | 20 std | PASS |

Chain: FROZEN 10:20:08Z < first trial 10:21:04Z < last request 10:25:01Z <
first GT read 10:25:25Z. No GT source was read before the last trial
(freezer §6.1 audit; runner attestations). Pre-freeze host traffic: the two
disclosed zero-quota setup reads only.

## 3. Scored results (quoted from the landed AUTHORITATIVE blocks)

All GT-derived numbers below are the impl seat's score-phase outputs as
landed in `attrib-r21-impl-{ds,glm}-trials.log`; this seat recomputed only
their arithmetic (counts, means, confidence intervals) from the receipts'
own tables.

**ds-flash-shim (:8791) — `attrib-r21-impl-ds-trials.log`, final block
10:27:01Z:** `ACCURACY: 20/20 = 1.000 (bar 0.80, min scored n 20) -> PASS`;
GT counts `{"alibaba-token-plan": 20}`; exclusions: none. Every trial's
prediction was `alibaba-token-plan` (confidence 0.538, scores
10.5/4.0/5.0), made blind — the ds trials all share one feature vector
(full istio-envoy header family, echo `requested`, usage
text_tokens+cached_tokens, pt 48, wall 1.33–1.76 s, burst span,
chatcmpl-uuid), and the journal agreed 20/20. Wilson 95% CI on 20/20:
[0.839, 1.000] (this seat's computation, z = 1.96).

**glm-flash-shim (:8793) — `attrib-r21-impl-glm-trials.log`, single block
10:27:03Z:** `ACCURACY: 22/22 = 1.000 (bar 0.80, min scored n 20) -> PASS`;
GT counts `{"devin": 9, "zai": 13}`; exclusions: none. The GT split is the
round's real measurement: zai 429 windows forced the cascade onto devin
mid-run, so the instrument had to attribute **two** legs under alternation,
and every per-trial chain matches its blind prediction (zai trials:
`1/zai OK 200`; devin trials: `1/zai FAIL 429; 2/devin OK 200`). The devin
serves were identified through the rewrite class (`rewritten:
glm-5-3-flash-max`), the ~407-token billing, and the `server:
devin-openai-shim/2` tell; the frozen caveat that this header may be the
shim's own error-path header rather than a relayed upstream header was
adjudicated by the trials in favor of relayed-at-serve (it co-occurs with
200-level devin serves here). Wilson 95% CI on 22/22: [0.851, 1.000].
Descriptive pooled read (different shims, different GT distributions):
42/42 = 1.000, Wilson [0.916, 1.000] — a summary, not an independent n.

**The adjudication trail behind the ds PASS (receipt-verbatim, kept
append-only):** four score blocks, three instrument defects, one bar
refusal —

| block (UTC) | result | mechanism |
|---|---|---|
| 10:25:25Z | `0/0 FAIL` (20× UNMATCHED) | matcher defect B (below): journal epochs +10800 s off — a bookkeeping FAIL, not an attribution result |
| 10:25:58Z | `0/0 FAIL` (20× UNMATCHED) | first repair attempt did not take |
| 10:26:11Z | `18/18 = 1.000 FAIL` | defects A+C produced 2 spurious AMBIGUOUS(2) exclusions; the frozen bar **refused the shrunken denominator** (min scored n 20) despite perfect accuracy — the gate working as designed |
| 10:27:01Z | `20/20 = 1.000 PASS` | re-adjudication after the matcher fixes; AUTHORITATIVE per the receipt's seat adjudication |

The glm block (10:27:03Z) ran after the fixes and carries no failed blocks.
A bookkeeping FAIL and a mechanism FAIL are opposite findings under the
same verdict word; only the receipt detail distinguishes them (lesson 3 of
the round's lessons entry).

**Official runner receipts: UNSCORED at finalize time.** Both files carry
complete trial records + seat addenda and no `GT + scoring` section (grep
count 0 at 11:08Z). Their recorded features make later scoring lawful
without any new request (the freezer's §6.1 note: features and predictions
are already in the receipts; the table is unchanged); the scorer owns that
call. Runner-A's addendum predicts its own result shape: all 20 ds trials
share one feature vector, so if GT agrees, the official ds block will be
another single-leg sweep.

## 4. Mimicry-probe outcomes

**Ran clean, and the honest reading is "uninformative as run", by the
frozen protocol's own `honest_read` clause.** All eleven ablations —
leave-one-out per feature (8) plus `mimicry:header-strip(hdrid)` (hdr_tells
+ id_class zeroed), `mimicry:latency-pad` (wall_band zeroed), and
`mimicry:echo-spoof` (model_echo zeroed) — scored **1.000 on both shims**
(20/20 ds, 22/22 glm, receipt-verbatim).

What that does and does not show:

- It shows **no single feature family is load-bearing on this GT**: the
  feature set is redundant — header tells, the devin model-id rewrite,
  usage schema, and the token/latency bands each separately separate zai
  from glm-cascade devin, so removing any one family leaves the argmax
  intact. Even where a band feature abstained (the 151-token devin billings
  outside the frozen [326, 488] band; the 16 s walls outside [0.3, 2.5]),
  the tell features carried the trial — features that abstain beat features
  that guess.
- It does **not** show attribution surviving a motivated padding adversary.
  The frozen ablations *remove* evidence; real padding (Kurian et al.'s
  semantic-preserving output filtering; 2605.14786's timing randomization)
  *injects or randomizes misleading* signal — and the legs are
  operator-side, so a client seat cannot pad them at all
  (`mimicry_protocol.scope`, frozen). The published adjacency (prior-art
  note §1/§2) prices the padding question as phenomenon-incremental; this
  round's arm bounds only information dependence.
- On ds the arm is doubly uninformative: with GT collapsed to one leg, any
  ablation that still predicts alibaba scores 20/20 regardless of what was
  zeroed. The glm arm (two-leg GT) is the only informative one, and it says
  the rewrite class + usage schema + bands jointly survive header-strip.

## 5. Prior-art scoping (from `corpus/knowledge/attrib-prior-art-r21.md`)

Verdict: **INSTRUMENT-NOVEL, PHENOMENON-INCREMENTAL** (search-set verdict:
9 fetched arXiv primaries, all HTTP 200, receipt §7 of that note).

- Phenomenon — crowded, published: response-text model fingerprinting
  (LLMmap 2407.15847; AdaptPrint 2608.22213; Kurian et al. 2508.09021),
  distribution-equality testing (Model Equality Testing, ICLR 2025,
  2410.20247), serving-stack fingerprinting (2605.29979), timing side
  channels (2411.01076, 2412.15431, 2409.20002), agent-action
  identification (2605.14786). The r19 receipts already show legs echoing
  their underlying models, so "which leg" and "which model" largely
  coincide fleet-locally. **No round-21 text claims the phenomenon.**
- Instrument — not found in the fetched set: no source attributes a
  cascade *leg* from *operational serving-stack artifacts* (header
  families, error-wording shape, body schema, latency shape) via a frozen
  hand-weighted table, validated against an *operator-side journal read
  only after trials*. The lane's own freeze-before-request discipline,
  promoted to a scoring protocol.
- Citation correction (prior-art note §5, defect 4 below): the brief's
  "LLMmap/2508.09021" conflates two papers — LLMmap is 2407.15847;
  2508.09021 is Kurian et al. (attack/defense). Correction changes the
  citation, not the verdict.
- What would falsify the instrument-novelty label: a fetched source doing
  leg attribution from operational features against operator-side GT. The
  search set is bounded; the label is a bounded negative (r9/r11 wording
  convention).

## 6. Adjacency (routed, not absorbed)

- **Serving-plane observations → integrator, unowned plane** (r19/r20
  precedent, unchanged): the zai 429 alternation that produced the glm GT
  split is route weather, not a model signal
  (`ledger-route-telemetry.md:60-62` frame); the devin leg's bimodal
  billing (407 vs 151 tokens for the identical prompt within one window)
  and its 16 s walls are shim/upstream serving facts this lane measured
  and reports; the status-masking relay semantics
  (`ALL LEGS FAILED -> returning last leg`) remain an observability defect
  of the shim software. Nothing fixed, nothing absorbed.
- **mori boundary respected**: the instrument's only privileged read is the
  post-trial `journalctl --user` read — fleet evidence, read-only,
  detection/report only; no OS state, no remediation, matching
  `../mori-shokunin/PROVINCE.md` (mori reads journal/cgroup events as
  evidence and never owns state; endpoint/model-serving health is out of
  this lane's remediation reach entirely, as the frozen table §0 words it).
- **Credentials: never read** (hard rule held): no Authorization header was
  sent (the shims need no caller auth, r19 G7 code-read receipt); all
  traffic was localhost; no credential file opened. Runner attestations
  concur.
- **Dispatch mechanism → kumitate/protocol**: the duplicate-execution
  defect (below) is the r19 missing-dispatch-ledger lesson recurring; the
  fix (serialized trial windows or a frozen per-seat join marker) is
  orchestration mechanism, routed, not built here.
- **Prompt craft → none**: no prompt-craft evidence was produced; the
  fixed COUNT_PROMPT body is an instrument constant, not a craft finding.

## 7. Defects and breaches (recorded, never patched)

1. **Double execution / budget breach.** 84 blind trials ran against
   frozen budgets of 21 ds + 23 glm (40 vs 21; 44 vs 23). The impl seat's
   own validation runs duplicated the runner seats' trials against the
   same shims; both sides disclosed in-receipt (runner-A addendum item 1;
   runner-B addendum; impl metas). The r19 defect-7 pattern recurred
   because the round again had no dispatch ledger; and the twin-traffic
   hazard it creates is not cosmetic — see defect 7. Routed (§6).
2. **The instrument's own bytes were never under a pin, and were edited
   mid-round after the trials.** Trials ran under sha `b3e18c78…`
   (receipt-pinned); the matcher was patched at 10:26:44Z; the landed
   scoring blocks were produced by `effa7ea7…`; score blocks record only
   the *table* sha (`frozen_sha256`), never the code sha that scored. The
   freeze surface covered the data and let the code float (lesson 1).
   Mitigation, verified from landed bytes + the impl adjudication: the
   edits are confined to the GT-matching path (`parse_ts`, match window,
   greedy assignment) and ablation plumbing — the blind prediction path
   (capture → extract_features → additive score) is unchanged in its math,
   and the GT join cannot influence trial-time predictions that already
   happened. Next instantiation pins the instrument file beside the table
   and records `instrument_sha256_at_scoring` in every score block.
3. **Matcher defects A/B/C, fixed pre-adjudication (impl adjudication,
   ds receipt):** (A) the [t0−0.5, t0+3.0] window rejected stamps that sit
   up to 1 s before t0 at 1-second journal resolution → widened to
   [t0−1.0, t0+3.0]; (B) `parse_ts` computed UTC wall time then called
   naive `.timestamp()`, re-applying the host's −03 offset — journal
   epochs +10800 s (demonstrated by runner-A on a **canned r19 line,
   without any journal read** — the reusable move: canned-GT smoke the
   scorer on prior receipts, which preserves the blind); (C) 1-second
   truncation pulled the next trial's stamp into the previous trial's
   window → spurious AMBIGUOUS(2) and the 18/18 block → greedy in-order
   1:1 assignment. Consequence trail in §3. The 18/18 FAIL is also the
   round's positive control: the frozen bar refused a shrunken denominator
   rather than rescale.
4. **Frozen in-block errata (permanent by design — the pin cannot be
   edited):** (a) the block's line 15 cites "LLMmap 2508.09021" — the
   prior-art note's §5 correction (LLMmap = 2407.15847) landed at 10:08:50Z,
   ten minutes *before* the freeze, and was frozen over anyway (lesson 7:
   compose from the landed corrections, not the brief); (b) the block's
   `standard_body` note says "233 bytes" — that is the r19 *error-path*
   body (with `temperature:0`); the frozen std body is 215 B (glm) / 221 B
   (ds), as every record's `body_len` shows (runner-A addendum item 2).
   GT matching was unaffected (the shim logs the bytes actually sent).
5. **GT collapse and the never-fired live error path narrowed the claim.**
   ds GT is single-leg (alibaba-token-plan ×20); glm GT is two-leg (zai 13,
   devin 9); **hyper took 0 GT trials on both shims and opencode-go 0 on
   ds — UNTESTED**, reported per the frozen §5 requirement, not averaged
   away. In the scored receipts the error-path arm never produced a
   non-200 (zai accepts `temperature:0`; both impl err trials served 200
   from leg-1), so `error_tells` stays validated by the r19 receipts plus
   one unscored capture (the official receipt's T21 did record a live 400
   `devin_shim_error`/`invalid_argument`/trace-ID relay — its GT section
   is part of what the owed scoring would adjudicate).
6. **The mimicry arm is a lower bound, not a padding adversary** (§4) —
   recorded as an outcome, not a breach; the frozen `honest_read` clause is
   what kept 11×1.000 from being sold as robustness.
7. **The GT join cannot distinguish your traffic from your twin's.** The
   99-request-line journal window behind the impl-glm score (two seats'
   identical 215-byte bodies interleaved 10:22:32–10:24:04Z, windows
   sharing ~92 s per the lessons entry) means rid-level provenance in that
   block is mixed even where leg-level GT is unambiguous — the greedy
   in-order assignment disambiguated it this time (every assigned chain
   matches its blind prediction), but the mechanism is one journal-arrival
   tie away from a silent cross-set swap. Structural fixes named in lesson
   4: serialized windows via a dispatch ledger, or a frozen per-seat join
   marker (nonce in the body / seat-tagged journal lines).
8. **The scorer's close-out never landed** (polling trail in the header).
   The two official receipts remain unscored; the aggregate verdict and
   the overlap adjudication this round's other seats explicitly reserved
   for that note are covered here only as receipt-verbatim quotations.
   This note is the finalizer's composition, not the scorer's
   adjudication; a later close-out supersedes.
9. **Hygiene nits (recorded, none scoring-relevant):**
   `datetime.utcnow()` deprecation warnings, recorded by runner-A against
   the trials-time bytes (`plans/attrib_probe.py:126,455` of that
   version) — not present in the landing-time file; `cmd_block_sha` crash
   (`TypeError`, `plans/attrib_probe.py:627` of the version the lessons
   seat hit) — not reproduced on the landing-time bytes by this seat
   (`block-sha` exit 0 at ~11:08Z); a stray `` `` `` line at
   `plans/attrib-r21-frozen.md:160` (outside the hashed block; harmless);
   `plans/__pycache__/` was created by an import side effect during the
   round and removed by this seat at ~10:38Z — it must not land. The
   lessons entry also records an r20 records-commit gap (cited paths
   untracked in `af0e3e6`/`3688f76`) — parent-owned landing-step check.

## 8. Honest limits

1. **Fleet-local.** Two shims, one host, one day; every profile value
   derives from r19 receipts of this fleet's routing; the instrument says
   nothing about any other host, provider, or even this host next week
   without a re-freeze and fresh trials.
2. **Time-varying — and the round's best result is weather-dependent.** The
   glm GT split (zai 13 / devin 9) exists because transient zai 429 windows
   forced fallbacks during one 2½-minute window; on a clean-zai day the glm
   GT collapses to one leg exactly as the frozen §5 pre-named, and the
   two-leg demonstration would not exist. Within the window itself the
   devin leg showed bimodal billing (407 vs 151 tokens, same prompt) and
   16 s walls — the frozen bands were stale on arrival for those trials,
   and bands generally will drift (r18→r19 moved TTFTs and prompt taxes on
   unchanged-looking lanes). The durable parts of the instrument are the
   tells and schema quirks; the bands are per-instantiation.
3. **N is small and the class distribution is degenerate.** n = 20 and 22
   scored trials; Wilson 95% intervals [0.839, 1.000] and [0.851, 1.000]
   even at 100% observed. Per-leg n: alibaba 20, zai 13, devin 9, hyper 0,
   opencode-go 0 — **3 of the 5 roster legs were exercised at all**, and
   the 0.80 bar was met on the 3 that served. The claim the numbers
   support: "the instrument attributed every leg that served, blind, with
   journal GT" — not "the instrument attributes the roster", and not any
   per-leg precision claim for devin at n = 9.
4. **The mimicry clause of the claim is not established** — the arm ran,
   passed everywhere, and shows less than the claim's wording dreamt of
   (§4). A motivated-padding result needs operator cooperation or a
   redesigned adversary arm.
5. **The scored record is one adjudication.** The ds PASS sits at the end
   of a four-block debugging trail (§3); a second scorer could defensibly
   re-adjudicate the two AMBIGUOUS exclusions differently (the 18/18
   block), and the official receipts are unscored. The receipts preserve
   every input needed to re-run that judgement; the numbers here are the
   impl seat's authoritative blocks plus this seat's arithmetic on them.
6. **No scalar axis verdicts** — the axis-move assessment belongs to the
   parent's SCORECARD integration; this note supplies the measured
   premises (novelty-proxy inputs: fetched-URL prior-art verdicts landed;
   instrument inspectable in-repo; construct newly measured above the
   pre-registered bar — on 3 of 5 legs).
7. **Calibration reading, descriptive only.** The instrument's confidence
   outputs (0.538–0.867 across trials) were never calibrated against
   anything — they are ratios of additive scores, not probabilities, and
   this note does not score them as predictions. The blind-prediction
   Brier-style scoring idiom of r19/r20 was not pre-registered for this
   instrument and was not retro-fitted here.

## 9. Inputs for the parent's landing step

- The falsifiable claim's outcome, per clause: §0 (all clauses met or
  bounded as stated; the accuracy clause met on the served legs).
- Novelty-proxy inputs: prior-art note with fetched URLs (9/9 HTTP 200);
  instrument inspectable in-repo (`plans/attrib_probe.py` +
  `plans/attrib-r21-frozen.md`); the phenomenon/instrument split is
  INCREMENTAL/NOVEL per that note — the split the SCORECARD's novelty
  proxy asks for.
- Artifacts produced this round (all working-tree at finalize time;
  commit/index/LOG is the parent's): 2 plans files, 4 evidence receipts,
  2 knowledge notes (prior-art + this one), 1 lessons entry, 3 scribe
  drafts under `.ufo/rounds/round-21/goal-wave/`.
- Owed after this note: the official receipts' score sections and (if the
  scorer seat surfaces) a superseding close-out; the LOG/SCORECARD
  placeholders in the scribe's drafts (`{{ACCURACY_SCORER_LINE}}` etc.)
  resolve from §3 above or from that close-out.

## 10. Sources

- `plans/attrib-r21-frozen.md` — frozen table + protocol + freeze record
  (§6) + freezer audit (§6.1); block anchor sha256
  `9f0244bb0aa4463c66981e5758a9a368ea0f0ea61b26882925f3ce7bbe6ba33c`;
  file sha256 `43ac5132c88715586de6e94da6d41bb7e135eea4b4b3ce0db7766044dc7cb732`.
- `plans/attrib_probe.py` — the instrument; trials-time sha `b3e18c78…`
  (receipt-pinned), landing-time sha
  `effa7ea7ba582e9273433f0fa5da266a7ff527ac2e58b367bfb2b4d958983e56`.
- `corpus/evidence/attrib-r21-impl-ds-trials.log` (sha256
  `1dddb3d62eb3edec…03daf1`) — trials + four score blocks + seat
  adjudication (AUTHORITATIVE ds block, defects A–C, D1–D3).
- `corpus/evidence/attrib-r21-impl-glm-trials.log` (sha256
  `04c505e4d384ce34…2556744`) — trials + AUTHORITATIVE glm block + adjudication.
- `corpus/evidence/attrib-r21-ds-trials.log` (sha256
  `7e6102461583c749…d52ecd`) — runner-A trials + addendum (DEFECT-A canned
  demonstration, DEFECT-B byte erratum, blind attestation, run-side
  observation). Unscored at finalize time.
- `corpus/evidence/attrib-r21-glm-trials.log` (sha256
  `aa6956065b58ba61…cc08bb`) — runner-B trials + addendum. Unscored at
  finalize time.
- `corpus/knowledge/attrib-prior-art-r21.md` (sha256
  `1e509faabc2826f8…003e2`) — prior-art pricing, verdict + wording constraints.
- `corpus/lessons/2026-10-16-round21-attribution-freeze-surface.md`
  (sha256 `27f7fd246b09119c…a15eb`) — the round's seven lessons; this note
  cites them as lesson 1–7.
- Basis receipts: `corpus/evidence/probe-r19-*.log` (the r19 feature
  evidence the frozen profiles cite), digest
  `corpus/knowledge/probe-battery-r19.md` (sha256 `0f28227d735f3708…d544`),
  `corpus/knowledge/kimi-model-routing-round18.md` (leg roster history).
- Boundary: `../mori-shokunin/PROVINCE.md`; scorecard proxies: SCORECARD.md
  §novelty proxy; starting commit `3688f76`.

## Round-22 addendum — forced-fallback leg coverage (parent-integrated 2026-10-16T13:10Z)

The standalone scorer seat of the r22 wave failed on a provider empty
response; this addendum is integrator-written from the instrument's
authoritative score blocks in `corpus/evidence/attrib-r22-legs.log` (runs 1-2,
adjudicated) and the ablation seat's handoff. The r21 numbers above stand
untouched.

- **hyper: COVERED.** Run-2 forced-fallback trials: on-target GT n=10,
  correct 10/10 = 1.000 (bar 0.80) — PASS. Run-1 was 9/9 on-target but n<10,
  so run-2 closed the count. Forcing mechanism: leg-1 content-inspection bait
  (400 `data_inspection_failed`) reliably cascades to leg-2.
- **opencode-go: NOT COVERED — named gap.** 0 on-target trials in both runs:
  the compliant-echo marker bait starves against this reasoning-model class
  (the model declines to echo the FAIL marker). The mechanism was proven
  reachable once (T03: a real opencode-go serve, blind-predicted correctly).
  An instrument fix shipped (v2 `body_schema`/`id_in_body` features,
  stream-flag GT join); the next forcing mechanism is r23's registered claim.
- **v2 table discipline:** three freeze pins — `124ade67…` (defective,
  superseded BEFORE any request), `3d7861f8…` (run-1), `77b8d4a0…` (live,
  freeze-3). The supersede-before-request path is the r19/r21 discipline
  working under table evolution.
- **Ablations (seat handoff):** `hdr_tells` LOO 17/20 and 19/20 — header
  relaying is load-bearing on this GT; header-strip mimicry 19/20 and 20/20.
- **Honest limit (critic):** forced coverage is a DIFFERENT claim than
  natural coverage — hyper is now validated on forced serves; natural hyper
  serves remain unmeasured.
- **Battery fold:** probe-type P10 (attribution health-check) landed in
  `plans/probe-battery-TEMPLATE.md` + this battery's §11.

## Round-23 addendum — stream-path leg coverage (scorer-r23, 2026-10-16T13:52Z)

Standalone scorer seat of the r23 wave (deepseek flash bucket,
`cascade/deepseek-v4.1-flash`). This seat sent **no request**; its only
privileged read is the post-trials journal (three captures: 1792157834–1792158036,
1792158318–1792158630, union 1792157834–1792158630, all after the last trial
request of every r23 run). Every number below is quoted from a landed receipt's
authoritative block or recomputed by this seat's independent re-implementation
of the frozen rule (`/tmp/kengaku-r23-scorer/score_r23.py`, forked from the r22
scorer seat's verified tool that reproduced the r22 blocks 40/40, plus
`join_audit_r23.py` for the twin-join audit). Scratch only — this addendum is
the seat's sole lane write. The r21 and r22 numbers above stand untouched.

### The round's clause, checked

- **Stream-path mechanism pinned from shim source (quoted): YES.** The selector
  is the per-leg HTTP status: for `stream:true` a 200 returns success from the
  response HEADERS before any body byte — `shim.py:270-278` (`return {"ok":
  True, ...}` after `if stream:`), so the FAIL-marker scan (`_marker_in`, called
  only at `shim.py:291`, non-stream branch) is unreachable on the stream path.
  Only a non-terminal non-200 advances the cascade (`shim.py:249-268`):
  FAIL_STATUSES {402,403,429}, 5xx, connect/timeout, and the one body-forced
  case, a 400 carrying `data_inspection_failed` (leg-1 alibaba). The shim builds
  its own upstream headers and never reads the caller's (`shim.py:210-217`) and
  `run_cascade` iterates the fixed `LEGS` list (`shim.py:299-315`), so no client
  header hint selects a leg. Three candidate levers were pre-registered and two
  falsified by code, one bounded: (1) marker bait on stream — FALSIFIED
  (scan unreachable); (2) client hint — FALSIFIED (headers ignored); (3)
  deterministic leg-3 — reachable only probabilistically (a transient leg-2
  failure). Empirically confirmed: the falsifier seat's stream-marker probe
  recorded alibaba serving a streamed body that literally contained `usage
  limit` (raw-SSE offset 1889 of 7336 bytes) with **no** fallthrough
  (`~/.cache/kengaku-tmp/falsifier-r23/p1b.out`, `p1c.out`), and the
  `stream-hint` control (headers `X-Shim-Leg`, `X-Cascade-Leg`) landed leg-1
  alibaba 3/3.
- **≥10 on-target opencode-go GT trials: NOT MET — 0 across all 104 r23 stream
  trials.** Scored: batch 1 (14) 0/14; batch 2 impl (30) 0/30; batch 2 twin
  (30) 0/30; verifier (30, unscored; blind leg distribution identical, alibaba 6
  / hyper 24). The 24-trial `stream-inspection` arm landed **hyper 24/24** — the
  probabilistic leg-2 failure that produced r22's single opencode-go serve
  (run-1 T03, 1/20) did **not** reproduce (0/24). The frozen verdict line,
  quoted verbatim from the twin run's block: `STREAM TARGET opencode-go:
  on-target GT n=0, correct 0/0 = 0.000 (bar 0.80, min on-target n 10) -> FAIL`.
- **Per-chunk features captured: YES, and deliberately unscored.** The r23
  instrument captures `stream_frames`, `stream_data_frames`,
  `stream_gap_ms_median`, `stream_frame_bytes_mean` per trial; the v3
  `feature_extension_ruling` freezes them as captured-but-weightless (no
  pre-trial per-leg cadence evidence exists to freeze a discriminating profile,
  so adding one would be a guess). No feature or weight changed from v2.
- **v3 re-freeze BEFORE trials: YES for the instrument-native run; a pre-v3
  deviation batch also exists.** v3 (`plans/attrib-r23-frozen.md`, FROZEN
  2026-10-16T13:45:47Z block `1b2d6a01…`; instrument at freeze `cce53a16…`)
  gates `stream-trials` (v3 + `stream_forcing` required, else exit 2, nothing
  sent). The runner seat's 14-trial batch 1 ran **before** v3 landed, on the v2
  table with instrument `bb6bd919…`, and disclosed the deviation in its receipt
  header. Both batches are scored below.

### Scored results (post-trials journal GT; every block cites its bytes)

| run | trials | instrument | accuracy | GT distribution | opencode-go on-target | source |
|---|---|---|---|---|---|---|
| batch 1 (runner, v2 deviation) | 14 | `bb6bd919…` | 14/14 = 1.000 | hyper 10 / alibaba 4 | 0 | `attrib-r23-stream-trials.log` L1–226, block 13:41:01Z |
| batch 2 (impl, v3 stream mode) | 30 | `cce53a16…` | 30/30 = 1.000 | hyper 24 / alibaba 6 | 0 | same file L227+ (this seat's score block 13:50Z) |
| batch 2 (twin seat, v3) | 30 | `cce53a16…` | 30/30 = 1.000 | hyper 24 / alibaba 6 | 0 | `attrib-r23-stream.log`, self-scored 13:49:42Z |
| verifier (v3, unscored) | 30 | `cce53a16…` | — | blind pred alibaba 6 / hyper 24 | 0 | `/tmp/vfy-y.log` (gate check sent unexpectedly) |
| combined main receipt (b1+b2) | 44 | — | 44/44 = 1.000 | hyper 34 / alibaba 10 | 0 | this seat, Wilson [0.920, 1.000] |

- Batch 1 (`bb6bd919…`) independent re-score: 14/14 = 1.000, Wilson
  [0.785, 1.000]; 0 ambiguous joins over 185 journal REQUEST lines; prediction
  re-derivation 14/14; natural 4 / forced 10. The instrument's own block prints
  `ACCURACY: 14/14 = 1.000 … -> FAIL` — the FAIL is the frozen shim-level bar's
  **min-n 20** refusing a 14-trial denominator, not a miss (the r23 verdict
  frame is per-target, below).
- Batch 2 impl (`cce53a16…`) independent re-score: 30/30 = 1.000, Wilson
  [0.886, 1.000]; per-body `stream-inspection` 24 → hyper 24, `stream-marker` 3
  → alibaba 3, `stream-hint` 3 → alibaba 3; natural 6 / forced 24;
  re-derivation 30/30.
- Batch 2 twin: independently reproduced by this seat (30/30 = 1.000, Wilson
  [0.886, 1.000], GT hyper 24 / alibaba 6 — identical to its own block);
  ablations `loo:hdr_tells` **14/30 = 0.467**, every other LOO and all three mimicry arms 1.000 — header relaying is
  the load-bearing feature on this stream population (batch 1: `hdr_tells` LOO
  10/14). The v2-table shim-level `ACCURACY … PASS` line is the pre-patch
  verdict; the target clause below is the r23 clause.

### Stream-path features vs `stream:false` (which carried, which abstained)

| feature | `stream:false` (r22 forced runs) | `stream:true` (r23) | read |
|---|---|---|---|
| `body_schema` | fired (`chat.completion`) | **abstains** (null) | mode-partitioned; contributes 0 on stream |
| `id_in_body` | fired (true) | **abstains** (null) | same |
| `stream_span_class` | abstains (null) | fires: alibaba `burst` (matches its frozen profile); hyper `burst` on short serves / `incremental` on long (frozen profile says `incremental`) | fires; hyper's frozen value is **stale for short stream serves** — a measured profile drift that never decided a trial (sensitivity patch of hyper→`burst`: batch 1 14/14, batch 2 30/30, zero prediction flips) |
| `hdr_tells` | relayed response headers | relayed response headers | carried and **load-bearing** (LOO 10/14, 14/30); note hyper's frozen `transfer-encoding:chunked` item is unreachable — the shim strips hop-by-hop headers (`shim.py:337`) |
| `usage_tells` | from the body JSON | from the SSE final chunk | carried; same families (alibaba `text_tokens`+`cached_tokens`; hyper `cost`) |
| `model_echo` | body `model` | first chunk `model` | carried (`requested`) |
| `prompt_tokens` | body `usage` | chunk `usage` | carried (alibaba 48–50; hyper 52) |
| `id_class` | body `id` vs headers | chunk `id` | carried for alibaba (`chatcmpl-uuid`); hyper's frozen `id_class` is `[]`, so it abstains |
| `wall_s` / bands | carried | carried | carried (hyper's long serves exceed the frozen [0.7, 3.0] band) |
| per-chunk metrics | impossible | new: frames / data-frames / median gap / mean frame bytes | captured, unscored (v3 ruling) |

### Legs table (honest)

- **opencode-go — still UNTESTED; the r22 gap carries forward.** r22: 0
  on-target on both runs; r23 stream path: 0 across 104 trials. The stream path
  is **not a new lever** — it removes the marker lever (unreachable on stream)
  and admits only the leg-1 inspection lever, which lands hyper. Reaching leg-3
  needs leg-2 to fail, which no client body forces (weather-only; 0/24 today).
- **hyper — now characterized on BOTH paths.** r22 `stream:false`: 10/10
  on-target = 1.000; r23 `stream:true`: 24/24 on-target = 1.000 in each of the
  impl and twin runs. Its short stream serves arrive as a single burst.
- **alibaba — +10 stream-mode natural trials at 1.000** (batch-1 std/marker and
  batch-2 marker/hint; leg-1 `OK` with no fallthrough).
- The score phase prints the round's honest limit verbatim: on the stream path
  the client's chosen body **SELF-SELECTS** the serving leg, so a landed leg is
  coverage of a client-influenced route, not of natural route weather. For
  opencode-go there is no client influence at all — hence 0.

### Defects and limits (recorded, not patched)

1. **The round's central clause is NOT MET — a falsified premise, not a
   measurement failure.** The mechanism admits no client-controllable leg-3
   advance; the only probabilistic branch (leg-2 timeout) did not fire.
2. **Instrument bytes floated through the round.** `bb6bd919…` (batch-1 trials,
   receipt-pinned) → `7b009655…` (batch-1 score block) → `cb2388d0…`/`51cc7d4c…`
   → `cce53a16…` (v3 freeze + batch-2 trials and scoring) → `489f938a…`
   (post-freeze verdict-path patch at 13:51:06, disclosed in-code: it sets the
   process verdict to the target clause and adds `shim_level_verdict`; the
   blind-prediction path is untouched). The r21 defect-2 family recurs: score
   blocks record the code sha that scored, and it differs from the trials sha.
3. **Triple execution of the stream protocol.** The impl run, a twin seat's run,
   and a verifier whose gate-check unexpectedly **passed and sent** 30 trials
   (`/tmp/vfy-y.log`) ran concurrently against :8791 — 104 lane stream trials
   this round against r22's 44-call scale. The r21 defect-1 / r22 twin family,
   third recurrence; a dispatch ledger or per-seat join nonce is still unpaid.
4. **Twin-traffic ambiguity (quantified).** 17 of 30 batch-2 windows carried
   2–3 same-class candidates (identical bodies). The frozen greedy join and an
   independent min-|dt| monotone alignment agree on **every GT value** (both
   30/30) because same-class twins are GT-equivalent here; rid-level provenance
   is MIXED where the runs overlap. Adjudication rule carried from the r22
   scorer: a feature-contradicted join is a JOIN-DEFECT, never an attribution
   miss — no such case arose.
5. **Batch 1 ran on the v2 table despite material stream-feature differences**
   (mode-partitioned features; hyper's span-class drift). The deviation is
   disclosed in the runner's receipt header; v3 froze after it, and the runner's
   own predictions (`0 opencode-go on-target`) were confirmed.
6. **Serving-plane observations (routed to the integrator, not absorbed):**
   hyper quota headers at 13:37Z `x-ratelimit-limit-day 10000 /
   remaining-day 8322`; alibaba's inspection filter fired 24/24 on the bait;
   no hyper header-timeout was observed this round (r22's single 15 s timeout
   did not reproduce). Nothing was fixed.

### Sources (all working-tree; commit/index/LOG parent-owned)

- `plans/attrib-r23-frozen.md` (v3) — block `1b2d6a01bfa431ec4e78bf89fd989f9ad500d10bb78634362a3c0e3bce794f87`
  (FROZEN 2026-10-16T13:45:47Z), file sha `6a0254dd…7d0e4d`; extends v2
  (`77b8d4a0…`) and v1 (`9f0244bb…`), both re-verified byte-stable this round.
- `plans/attrib_probe.py` — instrument `bb6bd919…` (batch-1 trials),
  `cce53a16…` (v3 freeze + batch-2 trials/scoring), `489f938a…` (working-tree
  bytes at this addendum; post-freeze verdict-path patch).
- `corpus/evidence/attrib-r23-stream-trials.log` (sha `5ce762aa…e2112fb`) —
  runner batch 1 (14 trials, blind predictions sha `8b26166d…`, driver sha
  `6b91d3f3…`) + impl batch 2 (30 trials, `stream_forcing` mechanism quoted).
- `corpus/evidence/attrib-r23-stream.log` (sha `16d8ab8f…5e06e1e`) — twin run,
  30 trials + its self-scored block (13:49:42Z) + ablations.
- `/tmp/vfy-y.log` (verifier, 30 trials, unscored), `/tmp/kengaku-tmp/r23-stream/`
  (driver, predictions, JSONL scratches), `/tmp/kengaku-r23-scorer/` (this
  seat's captures, score blocks, audit JSON).
- `corpus/lessons/2026-10-16-round23-stream-surface.md` — the design-time
  stream-surface lessons (mechanism + feature-abstention + GT-surface asymmetry).
- Falsifier probes `~/.cache/kengaku-tmp/falsifier-r23/p1b.out` / `p1c.out`
  (marker-in-streamed-body with no fallthrough) and the operator shim
  `~/.local/share/ds-flash-shim/shim.py` sha
  `42d86d99d42658214e362c2759ecab88a03de005e9ed93e9c1804cbf8c15a386`
  (read-only, never executed).


## Erratum (round 25, 2026-10-20 — interval re-verdict)

Appended; the lines above stay as written. The point verdicts quoted in this entry are re-verdicted by
`python3 plans/attrib_calibration.py --summary` under the exact two-sided CP95 rule
(`corpus/knowledge/attribution-interval-calibration.md`): the r22 `TARGET hyper 10/10 -> PASS` and the reading
"hyper is now validated" are **INDETERMINATE** (lower bound 0.691503; n ≥ 17 needed at zero errors) on the
registered last-block population (19/19 pooled with run 1 would PASS — population-dependent); every `0/0 -> FAIL`
target line is **UNTESTED**, not a failure. The overall-accuracy PASSes (20/20, 22/22, 20/20, 30/30) hold, as
trial-level PASSes over 1–3 request bodies.
