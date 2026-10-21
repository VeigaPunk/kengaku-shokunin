# scorecard-verdict-draft — kengaku round 21 (novelty: blind cascade-leg attribution instrument)

Scribe seat, round-21 goal wave. Written 2026-10-16; starting state captured
2026-10-16T10:04–10:08Z at HEAD `3688f76` (round-20 records; the r20 evidence
commit is `af0e3e6`), updated through 10:14Z — the prior-art-lander's note
landed at 10:08:50Z and is folded in (verbatim below); the other five seats'
artifacts were still absent at the 10:13:58Z poll. **This file writes nothing**: every block below is a
paste-ready delta for a PARENT-owned file (`SCORECARD.md`, `LOG.md`); the
parent integrates under the kengaku lane identity. `[PARENT]` markers flag
cells the parent must confirm or fill from landed artifacts at integration
time; `{{PLACEHOLDER}}` slots resolve from landed artifacts or are replaced
by an absence statement with polling evidence — placeholders must not ship.
No scalar axis verdicts — verdicts are recorded per gate, per the round-16
idiom (`corpus/lessons/round-16-recensus.md`).

Round-21 scope (one axis-move, NOVELTY — the attribution instrument): build
and validate a frozen feature-table instrument (latency band / header tells
/ error-wording shape / body schema; weights pre-registered, sha-frozen
BEFORE any trial) that attributes which cascade leg served a given
response, over ≥20 blind trials per shim, accuracy ≥ the frozen bar (80%),
scored against shim-journal ground truth read ONLY after the trials
complete; a prior-art note scopes the novelty honestly (instrument + GT
protocol, not a new phenomenon); mimicry probes test whether attribution
survives feature-profile padding. Hard rules: journal GT read after trials
(feature-freezer and scope-sentinel enforce ordering); frozen before
trials (double-read guard — the r19 TOCTOU lesson, BR-1); small requests,
≥2 s spacing, ≤2 requests per trial step; credentials never read
(localhost shims only). No fabricated knowledge; no scalar axis scores;
no git commits by seats.

Write ownership this round (per dispatch): instrument-impl → `tools/` **or**
`plans/` (one path, its choice) + its receipts; prior-art-lander →
`corpus/knowledge/attrib-prior-art-r21.md` only; trial-runners →
`corpus/evidence/attrib-r21-{ds,glm}-trials.log` only; feature-freezer →
`plans/attrib-r21-frozen.md` only; scorer + note-finalizer →
`corpus/knowledge/attrib-r21.md` only; scribe → this directory only;
lessons-distiller → `corpus/lessons/` only. SCORECARD.md/LOG.md are
parent-owned.

## 0. Measured state at draft time (10:04–10:08Z)

| Quantity | Value | Command |
|---|---|---|
| HEAD | `3688f76` | `git rev-parse --short HEAD` (10:04Z) |
| Working tree (lane) | `M corpus/knowledge/probe-battery-r19.md` (+180), `M plans/probe-battery-TEMPLATE.md` (+183/−27), `?? .ufo/interactive-sessions/`, `?? .ufo/rounds/round-20/goal-wave/`, `?? corpus/lessons/2026-10-16-round20-grid-closure.md` — see D21-s3 | `git status --porcelain` |
| N1 registration | `.ufo/rounds/round-20/kengaku.md:36-37` (verbatim in §1) | `grep -n N1 .ufo/rounds/round-20/kengaku.md` |
| Attribution instrument | **absent**: no `tools/` dir (`ls tools/` → not found); 0 `attrib*` filenames in `plans/`, `corpus/knowledge/`, `corpus/evidence/`; the only in-repo `.py`/`.sh` `attribut` hits are r12 error-record bookkeeping (`ERROR RECORD UNATTRIBUTED`, `corpus/evidence/round12-ladder/recompute_r12.py:53-55,1436-1451`) — not cascade-leg attribution | `git grep -il attribut -- '*.py' '*.sh'` → 4 files, inspected |
| Runnable files (operability baseline) | **37** committed `.py`/`.sh` at HEAD | `git ls-tree -r HEAD --name-only \| grep -cE '\.(py\|sh)$'` |
| Shim-journal GT mechanism | documented in landed r19 receipts: `journalctl --user -u glm-flash-shim.service` (`:8793`, legs `["zai","devin","hyper"]`) and `-u ds-flash-shim.service` (`:8791`, legs `["alibaba-token-plan","hyper","opencode-go"]`) carry `rid=<12hex> leg=<n>/<name> OK\|FAIL status=<s> … <dur>s` lines, quoted read-only, no HTTP | `probe-r19-P4-glm.log:33-37,137-139`; `probe-r19-shim-ds-run.log:19-20,52-55,151-152` |
| r21 artifacts | at 10:05Z none; by 10:38:51Z **five of six landed** (stat-verified): `corpus/knowledge/attrib-prior-art-r21.md` 10:08:50Z; `plans/attrib_probe.py` 10:16:25Z → updated 10:19:53Z (sha `b3e18c78…`, the bytes all live trials ran — sha recorded in both trials metas); `plans/attrib-r21-frozen.md` 10:20:08Z (`FROZEN: 2026-10-16T10:20:08Z sha256:9f0244bb…`, §6; append-only writes after — pin re-verified post-append by the lessons-distiller's `freeze-check --double-read`, exit 0); `corpus/evidence/attrib-r21-{ds,glm}-trials.log` (runner seats) + `attrib-r21-impl-{ds,glm}-trials.log` (impl's own runs, incl. the scoring blocks) by 10:27:50Z; `corpus/lessons/2026-10-16-round21-attribution-freeze-surface.md` ~10:40Z. **Pending: `corpus/knowledge/attrib-r21.md` (scorer + note-finalizer)** — absent at the 10:38:51Z poll | `stat -c '%y %n' <file>` per path |
| Grader | [PARENT: re-run at close — no gate change this round; the r17 verdict (`CHECKS n=733 mismatches=0 errata_pinned=1`) is expected to stand unless the r20-dirty bytes land mid-round (D21-s3)] | `python3 grader.py` |

## 1. The round's falsifiable claim, with receipts

**Before-claim (registered by the r20 novelty scout; the in-repo record):**

> "Novelty scout: latency-fingerprinting is crowded prior art; r21
> registered as N1 (blind leg attribution with shim-journal ground
> truth)."
> — `.ufo/rounds/round-20/kengaku.md:36-37`

Per the round dispatch, the scout priced *latency fingerprinting* OUT of
novelty against a crowded published space (LLMmap/2508.09021, Model
Equality Testing ICLR 2025, AdaptPrint, 2605.29979, 2411.01076,
2412.15431, 2409.20002, 2605.14786 — dispatch-provenance, see D21-s2) and
registered THIS round's claim as N1: **blind cascade-leg attribution with
shim-journal ground truth — instrument-level novelty,
phenomenon-incremental, scoped honestly.**

Scribe re-verification of the before-state (independent, 10:04–10:08Z):

- **N1 is registered** — the verbatim line above; it is the only in-repo
  record of the scout's verdict.
- **No attribution instrument exists in-repo** — §0 row: no `tools/` dir,
  zero `attrib*` files, and the 4 `.py`/`.sh` `attribut` grep hits
  inspected are r12 error-record bookkeeping (attributing error records
  to job cells), not leg attribution.
- **The lane has the raw material but never built the predictor** — every
  prior attribution in the corpus is *post-hoc journal consultation*
  (operator-side GT read after the fact, per request):
  `probe-r19-P4-glm.log:137-139` (rid `f78b4e5f9790` → `leg=1/zai OK`
  confirms the z.ai header family read) and
  `probe-r19-shim-ds-run.log:52-55,151-152` (rid → `leg=1/alibaba-token-plan`
  confirms the istio-envoy header read). The routing knowledge exists as
  prose digests (`corpus/knowledge/kimi-model-routing-round18.md`), never
  as a frozen, weighted, blind-scoring feature table.
- **Prior-art pricing state** — the novelty proxy's fetched-URL leg has
  not been exercised since r14 (r19/r20 are calibration rounds; SCORECARD
  novelty-proxy history `SCORECARD.md:47-54`, r19/r20 sections "novelty
  unchanged").

**After-claim (this round's deliverable, dispatch wording):** a frozen
feature-table instrument (latency band / header tells / error-wording
shape / body schema — weights pre-registered, sha-frozen BEFORE any trial)
attributes the serving leg over ≥20 blind trials per shim with accuracy ≥
the frozen bar (80%), scored against the shim journal ground truth read
ONLY after trials complete; the prior-art note scopes the novelty honestly
(instrument + GT protocol, not a new phenomenon); mimicry probes test
whether attribution survives feature-profile padding.

**Falsifiability shape (both legs can fail honestly):** the after-claim
has an *existence* leg (instrument, frozen, inspectable in-repo) and a
*performance* leg (≥80% over ≥20 blind trials per shim). A frozen
instrument scoring below the bar is a **falsification, recorded not
patched** — the round still lands (existence leg + honest MISS), and the
verdict table must not launder a sub-bar score into "instrument exists".
Symmetrically, "instrument exists but never ran" fails the performance leg
and is reported as such (the r19 close's own verdict shape: "partially
met, honestly reportable").

## 1.1 The evidence-grounded feature space (scribe inventory, design input only)

The scribe does not freeze weights or design the instrument
(feature-freezer-owned). This section inventories the per-leg observable
tells already landed in receipts, so the frozen table's feature families
are grounded in the corpus rather than invented — each row cites its
receipt:

| family | tell | leg(s) | receipt |
|---|---|---|---|
| header tells | `Server: devin-openai-shim/2` (shim software, both shims — constant, not a leg tell) | shim-level | `probe-r19-P4-glm.log:30` |
| header tells | z.ai family: `X-LOG-ID`, `ga-traceid`, `Alt-Svc=h3=":443"`, `Set-Cookie` | glm leg-1 zai | `probe-r19-P4-glm.log:125-126` |
| header tells | `server: istio-envoy` + `x-envoy-upstream-service-time`, no `x-opencode-*` | ds leg-1 alibaba-token-plan | `probe-r19-shim-ds-run.log:151` |
| header tells | `x-zen-model` (+ stream model echo `deepseek-v4.1-flash`) | ds leg-3 opencode-go | `probe-r19-shim-ds-run.log` (S-row, r19 battery 7b HIT: `x-zen-model` + stream field) |
| latency band | burst span 0 ms (14 reasoning deltas, one flush); TTFT ~2.1 s | glm leg-1 zai | `probe-r19-P4-glm.log:131-132,154`; battery 5b |
| latency band | incremental span 145 ms, TPS 434.91 | hyper (both cascades) | r19 note §5 finding 4 (`probe-r19-hyper.log` finding 1) |
| latency band | TTFT 1724 ms | ds leg-3 opencode-go | r19 note §2 row 7d |
| body schema | `usage.prompt_tokens_details.cached_tokens` + `completion_tokens_details.reasoning_tokens`; model echo `glm-5.3-flash`; prompt_tokens 30 | glm leg-1 zai | `probe-r19-P4-glm.log:129-130,134-135` |
| body schema | COUNT_PROMPT billed 48 (vs census 31 — serving-side change) | hyper | r19 note §5 finding 5 |
| error wording | `devin_shim_error` / `invalid_argument` / "an internal error occurred (trace ID: …)" on temperature:0 | devin leg (glm leg-2) | `probe-r19-P4-glm.log:31,44` |
| error wording | 429 `code 1302` "Rate limit reached" | zai under load | r19 note §2 row 6a |
| status masking | all-legs-fail returns LAST leg's status; journal line `ALL LEGS FAILED -> returning last leg` | shim-level | `probe-r19-P4-glm.log:37,93-96` |

Ground-truth mechanism (already landed, read-only): `journalctl --user -u
<shim>.service` lines `rid=<12hex> leg=<n>/<name> OK|FAIL status=<s>
<dur>s` — `probe-r19-P4-glm.log:34-37,47-50,137-139`;
`probe-r19-shim-ds-run.log:53-55,85-88,110-114`. `/health` enumerates the
leg order (`legs` array): glm `["zai","devin","hyper"]`
(`probe-r19-P4-glm.log:118`), ds `["alibaba-token-plan","hyper","opencode-go"]`
(`probe-r19-shim-ds-run.log:20`).

## 1.2 The round's results as landed (receipts read 10:27–10:42Z)

**Freeze → trials → GT ordering (global, all four trial files):** frozen
`2026-10-16T10:20:08Z sha256:9f0244bb…` < first trial 10:21:00.575Z
(impl-ds) < last trial 10:25:01Z (runner-A ds) < first journal GT read
10:25:25Z (impl-ds score block 1). The scribe independently reproduced
the block hash from the fenced bytes (match: True). **No GT read
precedes any trial; the freeze preceded everything.**

**Trial results (receipt-verbatim; the scorer note's adjudication is
still pending and supersedes where it disagrees — lesson preamble):**

| receipt | trials | authoritative score block | result |
|---|---|---|---|
| `attrib-r21-impl-ds-trials.log` | 20 std (10:21:04–10:22:19Z) | 4th block, 10:27:01Z (append-only trail: two 0/0 UNMATCHED blocks, one 18/18 FAIL-on-denominator block) | `ACCURACY: 20/20 = 1.000 (bar 0.80, min scored n 20) -> PASS`; GT counts `{alibaba-token-plan: 20}` — **single-leg GT; hyper/opencode-go 0 GT trials = UNTESTED** |
| `attrib-r21-impl-glm-trials.log` | 20 std + 2 err (10:22:32–10:24:41Z) | single block, 10:27:03Z | `ACCURACY: 22/22 = 1.000 (bar 0.80, min scored n 20) -> PASS`; GT counts `{devin: 9, zai: 13}` — hyper UNTESTED |
| `attrib-r21-ds-trials.log` (runner-A) | 20 std (10:23:45–10:25:01Z) | none — GT deferred to the scorer seat; addendum files DEFECT-A (parse_ts +3 h offset, demonstrated on a canned r19 line) + DEFECT-B (frozen byte-count erratum) | predictions all alibaba-token-plan, conf 0.538 |
| `attrib-r21-glm-trials.log` (runner-B) | 20 std + 2 err (10:21:42–10:24:04Z) | none — "The journal GT read is the score phase's — the scorer seat runs it after BOTH shims' trials complete" | predictions zai×13 / devin×9 shaped (receipt §T-rows) |

**Mimicry/ablation arm:** all 11 ablations (8 leave-one-out +
`mimicry:header-strip(hdrid)` + `mimicry:latency-pad` +
`mimicry:echo-spoof`) scored **1.000 on both shims** (ds 20/20, glm
22/22). The lessons-distiller's honest read (lesson 5) is the one the
drafts must carry: these are an **information-dependence lower bound**,
not a padding adversary — zeroing a weight removes evidence, it does
not inject misleading signal (the frozen protocol's own `honest_read`
clause pre-committed this interpretation).

**Defects and deviations recorded (never patched):**

1. **Matcher defects A/B/C** (impl-ds adjudication): 1-second stamp
   truncation; parse_ts re-applying the host −0300 offset (+3 h epochs —
   the cause of the two 0/0 UNMATCHED FAIL blocks); spurious
   AMBIGUOUS(2) from the ±5 s widening (fixed by greedy in-order 1:1
   assignment). The 10:26:11Z block shows the bar **refusing a shrunken
   denominator** (18/18 = 1.000 but n=18 < min 20 → FAIL) — lesson 3's
   bookkeeping-FAIL vs mechanism-FAIL separation, in one receipt.
2. **Instrument sha unrecorded at scoring** (lesson 1): trials ran under
   `b3e18c78…`; the matcher fixes produced `effa7ea7…` by scoring time;
   score blocks record only the *table* sha. The trials→scoring linkage
   is prose-only. Next instantiation: pin the instrument beside the
   table.
3. **`cmd_block_sha` crashes** (`TypeError`, `plans/attrib_probe.py:627` —
   distiller hit; the scribe independently reproduced the same class on
   the pre-fix instrument at 10:14Z, see D21-s12).
4. **Duplicate execution** (r19 defect-7 recurrence, no dispatch
   ledger): 84 blind trials across four files (40 ds / 44 glm) vs the
   frozen 21/23 budgets; both seats disclosed in-receipt (runner-A
   addendum item 1; runner-B addendum). The glm journal window carried
   **99 request-lines** (foreign traffic) for 22 impl trials — the
   D21-s7 rid-collision hazard, materialized twice (impl-ds AMBIGUOUS×2;
   the glm 99-line window), resolved by the matcher's greedy assignment;
   the scorer note must state how the window was disambiguated (cheap
   cross-check: runner-B's independent blind predictions vs the same GT).
5. **Frozen-table errata, permanent inside the pin** (lesson 7): §0
   prose cites "LLMmap 2508.09021" (the conflated citation — the
   prior-art note's §5 correction landed 10:08:50Z, eleven minutes
   before the freeze, and was not incorporated); the standard-body note
   says 233 bytes (runner-A DEFECT-B: measured 215/221 B; 233 B is the
   error-path body). The block is sha-pinned — fixes are errata-only,
   next instantiation.
6. **Frozen-table calibration defects exposed by the trials** (impl
   adjudications D1/D2/D4/D5/D6, recorded, table stays as frozen):
   wall bands overlap (latency non-discriminating — the honest
   expectation); devin billing bimodality 407/151 on the identical
   body; wall-band misses at 16.0 s/10.6 s (features abstained, tells
   carried); the error path never exercised live (zai accepts
   temperature:0 — both err trials served 200 from leg-1; error_tells
   stays validated by r19 receipts + mock-smoke only); one
   connection-level `FAIL status=None` fall-through witnessed live
   (r19 G8 mechanism).
7. **Hygiene:** `plans/__pycache__/` (import side effect) should not
   land.

## 2. Verdict draft — novelty axis-move (paste-ready section)

```markdown
## Round 21 — blind cascade-leg attribution instrument (novelty axis-move)

One 32-seat flash wave (operator routing: zai bucket). The r20 novelty
scout priced latency-fingerprinting OUT of novelty (crowded published
space) and registered N1: blind cascade-leg attribution with shim-journal
ground truth — instrument-level novelty, phenomenon-incremental. The
round builds and validates the instrument: a frozen feature-table
(latency band / header tells / error-wording shape / body schema; weights
pre-registered, sha-frozen BEFORE any trial, double-read guard per the
r19 TOCTOU lesson), ≥20 blind trials per shim (glm-flash-shim :8793,
ds-flash-shim :8791), accuracy scored against the frozen bar (80%) with
shim-journal ground truth read ONLY after trials complete; mimicry probes
test whether attribution survives feature-profile padding; the prior-art
note scopes the claim honestly (instrument + GT protocol, not a new
phenomenon).

| Axis | Verdict | Evidence / limit |
|---|---|---|
| **novelty** *(owned)* | [PARENT: verdict line per gate — the proxy's three legs fire or not per the landed artifacts] | N1 registration (`.ufo/rounds/round-20/kengaku.md:36-37`); prior-art note **landed** (`corpus/knowledge/attrib-prior-art-r21.md`, 10:08:50Z): "INSTRUMENT-NOVEL, PHENOMENON-INCREMENTAL (search-set verdict)" — 9/9 arXiv primaries fetched HTTP 200 (§7 receipt); honest scoping §4 ("No round-21 text may claim the phenomenon as a discovery"); citation correction §5 (the brief's "LLMmap/2508.09021" conflates two papers — LLMmap is 2407.15847 — verdict unaffected); frozen feature table `plans/attrib-r21-frozen.md` (`FROZEN: 2026-10-16T10:20:08Z sha256:9f0244bb…` — scribe-reproduced from the fenced bytes, match: True); blind trials 84 across four receipts (`attrib-r21-{ds,glm}-trials.log` runner seats + `attrib-r21-impl-{ds,glm}-trials.log` impl's own runs) scored **above-bar on both shims: ds 20/20 = 1.000 PASS, glm 22/22 = 1.000 PASS** (impl receipts' authoritative blocks 10:27:01/10:27:03Z; scorer note pending, supersedes where it disagrees); mimicry arm all 11 ablations 1.000 on both shims — an information-dependence lower bound per the frozen `honest_read` clause (lesson 5), not a padding adversary. Novelty-proxy reading: the fetched-URL leg fires (first exercise since r14), split recorded phenomenon-INCREMENTAL / instrument-NOVEL per the landed note (proxy definition SCORECARD.md:47-54) — [PARENT: whether novelty MOVES on the rubric is the parent's judgement]. |
| calibration | [PARENT: verdict] | The round's discipline machinery, exercised under load: freeze-before-trials (double-read stability guard; pin verified at freeze, at every trial start via `frozen_sha256_at_start` in all four receipts' metas, and post-append by the distiller's `freeze-check --double-read` exit 0) + GT-read-after-trials ordering **clean globally**: frozen 10:20:08Z < first trial 10:21:00.575Z < last trial 10:25:01Z < first GT read 10:25:25Z; bar and denominator pre-registered — and the bar **refused a shrunken denominator** (the 18/18 = 1.000 FAIL at n=18 < 20), the pre-registration working as designed; matcher defects A/B/C recorded never patched (four append-only score blocks on ds); instrument sha unrecorded at scoring (b3e18c78 → effa7ea7 — lesson 1, next-instantiation pin). |
| operability | [PARENT: verdict — a new runnable instrument lands in-repo for the first time since r11's probe scripts; the runbook baseline was 37 committed `.py`/`.sh` at `3688f76`] | `plans/attrib_probe.py` (stdlib-only; `freeze-check` exits 0/2 with a verdict; `score` exits 0/1 on the frozen bar; `cmd_block_sha` currently crashes — TypeError at `:627`, recorded) — [PARENT: confirm the stranger-runnable property at integration]. |
| coverage | [PARENT: verdict] | Index parity at close: `corpus/knowledge/attrib-prior-art-r21.md`, `corpus/knowledge/attrib-r21.md`, `corpus/evidence/attrib-r21-{ds,glm}-trials.log`, `plans/attrib-r21-frozen.md` — [PARENT: verify per `corpus/README.md` and add rows]. |
| depth | unchanged | No new sourced domain claim beyond the instrument's own note and the prior-art note's citations. |
| freshness | [PARENT: verdict] | The trials are same-day re-verifications of the live cascade route surface (last pinned r19/r20, same day); all four trial receipts carry UTC-stamped trial windows (10:21:04–10:25:01Z) with per-trial t0_utc stamps, and the score blocks record their journal-read UTC (10:25:25–10:27:03Z). |
| adjacency | unchanged | All requests localhost shims (:8791/:8793); credentials never read (receipts redact Authorization as `<len N>`); journal reads are the shim's own unit log as GT for this lane's own probes — the r19-established pattern; any serving-plane finding (leg-order change, error-path change) is routed to the integrator, not absorbed. |

Honest ceiling: the instrument is host- and day-specific (the r19 note's
§8 limit-2 idiom applies verbatim) — ≥80% attribution on 2026-10-16 on
this host's two shims does not transfer; the shim redeployed
2026-10-15T17:16:22Z once already (r19 note §5 finding 1), and another
redeploy invalidates the frozen table by construction. **The accuracy
numbers carry a GT-collapse caveat the receipts themselves file**: ds GT
is single-leg (alibaba-token-plan ×20), glm two-leg (zai 13 / devin 9);
hyper is 0-GT UNTESTED on both shims (frozen table §5 pre-named the
collapse) — the claim the numbers support is "attributes the legs that
served", not "attributes the roster". The error path never fired live
(zai accepts temperature:0 — impl adjudication D5); error_tells stays
validated by r19 receipts + mock-smoke only. The mimicry arm bounds the
claim (information-dependence lower bound — lesson 5's wording): a
motivated padding adversary is untestable from a client seat; the
frozen `honest_read` clause kept the passing arm from being sold as
stronger than it is.
```

**[PARENT] Fill rules for the section above:**

1. `{{ACCURACY_SCORER_LINE}}` and `{{AGGREGATE_LINE}}`
   resolve ONLY from
   `corpus/knowledge/attrib-r21.md` when it lands (pending at the
   10:38:51Z poll — absent becomes an absence statement with polling
   evidence); the accuracy/freeze/ordering/mimicry lines already
   resolved inline come from the landed receipts and lesson and are
   quoted verbatim from them; do not recompute a scorer's number.
2. The novelty cell's verdict line must be a verdict *per gate*
   (round-16 idiom), not a scalar. Whether novelty moves is the parent's
   judgement; this draft files the evidence and the proxy reading.
3. If the accuracy result is below the frozen bar, the novelty cell must
   still be scored on the proxy's legs (construct + inspectable
   instrument + prior-art verdict) with the MISS recorded as the round's
   honest falsification — a sub-bar instrument with a clean freeze/audit
   chain is a landed calibration result, not a failed round.

## 3. Scribe findings (filed, not patched; each with its receipt)

- **D21-s1 (before-state re-verification — the round's premise holds at
  draft time):** every leg of the before-claim verified independently at
  2026-10-16T10:04–10:08Z (§0 table + §1): N1 registered in-repo; no
  attribution instrument anywhere in the repo (the 4 `attribut` `.py`/`.sh`
  hits inspected and ruled out — r12 error-record bookkeeping); no r21
  artifacts on disk; the GT mechanism (shim unit journal, rid + per-leg
  lines) documented in landed r19 receipts. The premise "no instrument
  exists that can attribute which cascade leg served a given response
  without operator-side ground truth" is true at round start.
- **D21-s2 (N1 provenance was thin in-repo — RESOLVED by the lander, with
  a citation correction the drafts must carry):** the scout's pricing
  evidence (the crowded-space fetch list named in the dispatch) existed
  ONLY in the wave dispatch text; the in-repo record was the one-line
  registration (`.ufo/rounds/round-20/kengaku.md:36-37`). The
  prior-art-lander resolved this: `corpus/knowledge/attrib-prior-art-r21.md`
  (landed 10:08:50Z) re-verified the set seat-side — 9 arXiv abs pages
  fetched in-session, HTTP 200 ×9 (§7 receipt) — and prices N1
  **INSTRUMENT-NOVEL, PHENOMENON-INCREMENTAL** (§1, search-set verdict,
  adversarial-default convention). Two load-bearing facts the parent
  must carry into the verdict: (a) the note's §5 **citation correction**
  — the round brief's "LLMmap/2508.09021" conflates LLMmap (2407.15847)
  with Kurian et al. (2508.09021); both real, verdict unaffected
  (recorded, not patched); the brief also lacked IDs for Model Equality
  Testing (2410.20247) and AdaptPrint (2608.22213) — the note supplied
  and cross-checked them; (b) the note's §4 wording is the honest
  scoping the round must keep ("No round-21 text may claim the
  phenomenon as a discovery"), and its §3 names the load-bearing case
  the published space cannot do: ds-cascade hyper and opencode-go legs
  shared a deepseek-family model in r19 receipts, so response-text model
  fingerprinting alone cannot attribute the leg.
- **D21-s3 (inherited dirty bytes — the r20 SCORECARD section cites
  working-tree-only evidence):** at HEAD `3688f76`, the r20 records
  commit carried only `.ufo/rounds/round-20/kengaku.md`, `LOG.md`,
  `SCORECARD.md`; the r20 evidence commit `af0e3e6` carried only the 4
  receipts. The scorer's §10 extension (`corpus/knowledge/
  probe-battery-r19.md`, +180 lines, `git diff --stat` 10:04Z) and the
  template revision (`plans/probe-battery-TEMPLATE.md`, +183/−27) are
  **uncommitted**, as are the r20 lesson and the r20 scribe drafts. The
  landed SCORECARD round-20 section cites those bytes (template §5 step
  3 / §7 rules / §9 steps with line numbers) — a tree reset would dangle
  the pointers. This is the r8 breach class (evidence working-tree-only)
  and the r17 class (inherited dirty WIP). [PARENT: commit the r20 bytes
  before/with the r21 evidence landing, or record the carry explicitly.]
- **D21-s4 (dual ordering guard — the round's two hard rules need a
  mechanical proof form):** (a) *frozen before trials*: the r19 TOCTOU
  lesson (BR-1, freeze racing its own last edit) migrates as
  `plans/probe-battery-TEMPLATE.md` §5 step 3 (author-confirmation +
  double-read stability H1==H2 + pre-write recompute + post-write third
  recompute); the feature-freezer's `plans/attrib-r21-frozen.md` should
  reuse that procedure and stamp `FROZEN: <UTC> sha256:<H>` with the
  hashed byte range stated exactly (the §6 defect-2 sed self-match
  lesson: bracket the anchor, e.g. `sed -n '1,/FROZEN-ANCHO[R]/p'`).
  (b) *GT read after trials*: the scorer's note should record
  `gt_first_read_utc` and `last_trial_utc` per shim and assert
  `gt_first_read_utc > last_trial_utc`; trial receipts should carry their
  own request timestamps so the assertion is auditable from landed bytes.
  The historical journal excerpts in r19 receipts (quoted in §1.1) are
  design input, not trial-window GT — reading them pre-trial does not
  breach the rule; the trial window's journal reads do.
- **D21-s5 (request-budget tension — flag before integration, not at
  it):** ≥20 blind trials per shim × 2 shims = ≥40 requests, plus the
  mimicry arm, against the wave-generic "≤2 requests per trial step". The
  r20 precedent governs: the frozen pre-registered set supersedes the
  generic cap when disclosed in-receipt (`probe-r19-P2-servicetier.log:10`,
  adjudicated in `corpus/knowledge/probe-battery-r19.md` §10.1
  provenance line). The feature-freezer's frozen plan should therefore
  enumerate the FULL request set (every trial, every spacing) so the
  supersession is pre-registered, and the "≤2 requests per trial step"
  wording should be read as per-step, not per-trial — [PARENT: confirm
  the reading]. The ≥2 s spacing and one-attempt rules stand.
- **D21-s6 (the 80% bar needs its denominator pinned pre-trial):** the
  bar is falsifiable only if the frozen table defines, BEFORE any trial:
  (a) accuracy = correct-leg-attributions / scored trials, per shim;
  (b) whether no-leg-served (all-legs-fail) trials enter the denominator
  or are excluded with the status-masking mechanism noted
  (`probe-r19-P4-glm.log:37,93-96` — the caller sees the last leg's
  status; GT for such trials is "no leg served", not "leg N");
  (c) the chance baseline stated beside the bar (1/3 per 3-leg cascade —
  80% ≫ chance is the point of the claim); (d) the mimicry arm reported
  SEPARATELY from the clean ≥20-trial denominator (padding trials that
  counted toward the 80% bar would make the bar ambiguous — the padding
  arm is a survival test, not an accuracy input). These are
  feature-freezer items; filed now so they are not resolved post-hoc by
  the scorer.
- **D21-s7 (GT matching mechanics — the rid-collision hazard):** the
  shim journal correlates by `rid`, which is NOT echoed in the response
  headers the r19 receipts show (z.ai family: X-LOG-ID/ga-traceid/
  X-Request-ID — none is the shim's 12-hex rid). r19's corroboration
  matched journal lines to requests by timestamp + byte count + stream
  flag, manually, in quiet windows. Under a 32-seat wave the same shim
  serves concurrent foreign traffic in the same seconds
  (`probe-r19-P4-glm.log:79-84`: repeated 429/OK across many rids within
  ~11 s). The frozen plan should pin the GT matcher (e.g., unique request
  byte-counts per trial, or trials run in checked-quiet windows) —
  otherwise a mis-attributed GT row silently corrupts the accuracy
  score. This is the round's most likely silent-failure mode.
- **D21-s8 (adjacency boundary — the journal read is in-province, with a
  named limit):** reading the shim units' own journals as GT for this
  lane's own probes is the r19-established pattern
  (`probe-r19-P4-glm.log:17`: "Journal lines are quoted read-only from
  `journalctl --user -u glm-flash-shim.service` (no HTTP)"). It is NOT
  mori-shokunin's watchdog/liveness reading of journals (mori
  `PROVINCE.md`: reads journal events as fleet evidence, detection and
  report only) and not kumitate's dispatch mechanism — the r21 instrument
  stays inside the kengaku serving-plane-probe scope; credentials never
  read (shim api_key stays `<len N>` in receipts). Any serving-plane
  *finding* (leg reorder, new error class) is routed to the integrator
  per the lane's standing adjacency discipline, not absorbed.
- **D21-s9 (scribe self-disclosure, ordering-safe):** this seat issued
  zero HTTP requests to any probe target and read no journal GT for any
  trial window (no trials exist yet). Reads were lane files, the fleet
  reports dir, plus one `date -u` per session start. Nothing this seat
  did can enter an ordering audit.
- **D21-s10 (polling discipline — the D20-s13 lesson applied):** r21
  artifact landing will be tracked with UTC-explicit predicates
  (`find <file> -newermt '<UTC string>'` with a UTC-explicit date, or
  `stat` mtime comparison) — the r20 scribe's local-time `-newermt`
  predicate silently inverted "landed" into "pending" for ~25 min
  (D20-s13, `.ufo/rounds/round-20/goal-wave/scorecard-verdict-draft.md`
  §3). §5 below is updated only on `stat`-verified mtimes.
- **D21-s11 (fleet-level report copy):** the fleet round-20 report dir
  `~/.ufo/reports/round-20/` contains only `kasegi.md` at 10:06Z — the
  kengaku round-20 fleet copy is not present there (the lane-local copy
  is committed at `.ufo/rounds/round-20/kengaku.md`). [PARENT: confirm
  whether the fleet-level copy is still owed for r20 and route the r21
  report accordingly.]
- **D21-s12 (instrument crash found offline by the scribe — the
  freezability defect, fixed by the impl seat before freeze):** at
  10:14Z, with the frozen table still absent, the scribe ran
  `python3 plans/attrib_probe.py freeze-check --frozen
  plans/attrib-r21-frozen.md` and `block-sha` → both crashed with
  `TypeError: find() argument 1 must be str, not bytes` at
  `plans/attrib_probe.py:67` (`BLOCK_START`/`BLOCK_END` are bytes,
  `text` is str), exit 1; `python3 -c "import ast; ast.parse(...)"` →
  AST parse OK. The impl seat evidently fixed this before freezing
  (mtime 10:19:53Z; the trials metas record instrument sha `b3e18c78…`
  and all subsequent runs verified the pin). The scribe's zero-request
  offline self-check is exactly the mock-smoke-before-freeze move the
  r19 DEFECT-3 lesson asks for — it caught a freezability failure
  before the freeze existed. Residual: `cmd_block_sha` still crashed
  for the distiller at `:627` post-fix (`TypeError: Strings must be
  encoded before hashing` — lesson's named leftovers); recorded, not
  patched.
- **D21-s13 (the frozen table froze the brief's conflated citation —
  lesson 7, cross-referenced):** `plans/attrib-r21-frozen.md:15`
  cites "LLMmap 2508.09021" inside the sha-pinned block, eleven minutes
  AFTER the prior-art note's §5 correction landed (10:08:50Z); the
  233-byte figure (runner-A DEFECT-B) is the same family. The pin makes
  both permanent — errata-only. The procedural lesson (seats compose
  from the brief, not from landed notes) is the distiller's to carry;
  the scribe's drafts cite the correction explicitly (§1.2 item 5) so
  no paste-ready block propagates the error.
- **D21-s14 (the scribe's two pre-named hazards both materialized —
  the drafts' design-input value, checked):** D21-s7 (rid collision)
  materialized as impl-ds's AMBIGUOUS(2) pair and the glm 99-request
  window (99 journal request-lines for 22 trials); the frozen greedy
  matcher + zero interleaving in the ds window resolved it, and the
  cheap cross-check (runner-B's independent blind predictions vs the
  same GT) remains available to the scorer. D21-s5 (budget supersession)
  materialized as the duplicate execution (84 trials vs 21+23 frozen);
  disclosed in-receipt by both seats; the structural fix (dispatch
  ledger or per-seat join marker frozen into the protocol) is lesson 4's
  named debt. Both hazards were pre-registered in this draft BEFORE the
  trials ran — the scribe's design-input pass did its job; the fixes
  belong to the next instantiation, not to a patch.
- **D21-s15 (the scorer note is the round's last artifact — the
  drafts' remaining slots):** at the 10:38:51Z poll
  `corpus/knowledge/attrib-r21.md` is absent; the lesson's preamble
  records the same at ~10:40Z and states the supersession rule ("where
  the scorer's adjudication disagrees it supersedes"). The verdict
  draft's §2 quotes the receipts' authoritative blocks and marks the
  scorer's adjudication as pending; the parent must resolve
  `{{ACCURACY_SCORER_LINE}}`/`{{AGGREGATE_LINE}}`
  from the landed note at integration, or record its absence with
  polling evidence — the r19 precedent (P2/P3/P8/P9 UNRUN rows named,
  not hidden) is the honest shape for a partially-landed round.

## 4. Sources for every claim in this draft

- `.ufo/rounds/round-20/kengaku.md:36-37` — the N1 registration (verbatim).
- `corpus/knowledge/attrib-prior-art-r21.md` — **landed 10:08:50Z**
  (prior-art-lander seat): §1 verdict (INSTRUMENT-NOVEL,
  PHENOMENON-INCREMENTAL), §2 the 9 fetched papers table, §3 the
  leg-level/operational-features/frozen-table/journal-GT gaps, §4 the
  honest scoping wording, §5 the citation correction
  (LLMmap = 2407.15847 ≠ 2508.09021 = Kurian et al.), §7 the fetch
  receipt (HTTP 200 ×9).
- `SCORECARD.md:47-54` — the novelty proxy definition (fetched-URL leg;
  phenomenon-new vs instrument-new split); `:416-454` (round-19
  section), `:456-481` (round-20 section — grid 9/9, 3c falsified,
  combined mean Brier 0.0998/46).
- `corpus/knowledge/probe-battery-r19.md` — r19 close note + r20 §10
  extension (working-tree bytes carry the §10 extension — D21-s3);
  §5 findings (leg orders, shim redeploy, per-leg tells), §6 defects
  (BR-1, sed self-match, budget breach), §8 honest limits (host/day
  specificity), §10.1 (the frozen-set-governs precedent).
- `plans/probe-battery-TEMPLATE.md` — the freeze discipline
  (§5 step 3 double-read guard, hash-command form, breach doctrine) the
  feature-freezer should reuse (working-tree bytes — D21-s3).
- `corpus/evidence/probe-r19-P4-glm.log` — journal line format, z.ai
  header family, body schema, devin error wording, status masking,
  leg enumeration via `/health`.
- `corpus/evidence/probe-r19-shim-ds-run.log` — ds leg enumeration,
  istio-envoy tell, journal format, S8 stub mechanism tests.
- **Round-21 landed artifacts (read in full by this scribe):**
  `plans/attrib_probe.py` (663 lines, sha `b3e18c78…` as run);
  `plans/attrib-r21-frozen.md` (FROZEN 10:20:08Z `9f0244bb…`);
  `corpus/evidence/attrib-r21-{ds,glm}-trials.log` (runner seats A/B,
  no score sections — GT deferred);
  `corpus/evidence/attrib-r21-impl-{ds,glm}-trials.log` (the scoring
  blocks: ds 20/20 PASS, glm 22/22 PASS, defect adjudications D1–D6);
  `corpus/knowledge/attrib-prior-art-r21.md` (verdict §1, fetch
  receipt §7);
  `corpus/lessons/2026-10-16-round21-attribution-freeze-surface.md`
  (7 lessons + named leftovers).
- `corpus/knowledge/kimi-model-routing-round18.md` — the r18 routing
  digest (prose, not an instrument; TTFT/TPS/burst binding definitions).
- `.ufo/rounds/round-20/goal-wave/scorecard-verdict-draft.md` — the r20
  scribe drafts (D20-s13 polling lesson; paste-ready idiom this file
  follows).
- `../mori-shokunin/PROVINCE.md` — the adjacency boundary cited in
  D21-s8.
- Round dispatch (this wave's prompt) — the round scope, hard rules,
  write ownership, and the scout's crowded-space citation list
  (dispatch-provenance per D21-s2).

## 5. Status at scribe handoff (updated on stat-verified mtimes only)

**At 10:08Z** no r21 artifact had landed; **by 10:40Z five of six had**
(below). Inventory watched (state at the 10:38:51Z poll):

| seat-owned artifact | path | state at 10:38:51Z |
|---|---|---|
| instrument-impl | `plans/attrib_probe.py` (its choice: `plans/`) | **landed** 10:16:25Z, updated 10:19:53Z (sha `b3e18c78…` = the bytes every live trial ran); its own validation receipts `corpus/evidence/attrib-r21-impl-{ds,glm}-trials.log` landed by 10:27:50Z |
| feature-freezer | `plans/attrib-r21-frozen.md` | **landed** 10:20:08Z (`FROZEN: 2026-10-16T10:20:08Z sha256:9f0244bb…`, §6; scribe-reproduced, match: True) |
| trial-runners | `corpus/evidence/attrib-r21-{ds,glm}-trials.log` | **landed** by 10:27:50Z (runner seats A/B; score phases deferred to the scorer seat — no GT sections in these two files, by design) |
| scorer + note-finalizer | `corpus/knowledge/attrib-r21.md` | **absent at 10:38:51Z poll — the round's last artifact** (the lesson's preamble records the same; D21-s15) |
| prior-art-lander | `corpus/knowledge/attrib-prior-art-r21.md` | **landed 10:08:50Z** (206 lines; folded into §0/§2/D21-s2) |
| lessons-distiller | `corpus/lessons/2026-10-16-round21-attribution-freeze-surface.md` | **landed ~10:40Z** (200 lines; lesson 5's mimicry wording + the named-leftovers list folded into §1.2) |
| trial-runners | `corpus/evidence/attrib-r21-{ds,glm}-trials.log` | **landed by 10:27:50Z**, plus the impl seat's own `attrib-r21-impl-{ds,glm}-trials.log` with the scoring blocks (folded into §1.2) |

Every paste-ready block in §2 quotes only landed artifacts; the only
remaining `{{…}}` slots are the scorer-note-dependent ones
(`{{SCORER_NOTE_STATE}}`-family) and `{{CLOSE_COMMIT}}` — they resolve
at integration from `corpus/knowledge/attrib-r21.md` and the landing
commit, or become absence statements with polling evidence. [PARENT:
the
integration steps remain — LOG.md §21 entry, SCORECARD.md round-21
section, the fleet report, index rows, grader re-run, the D21-s3
decision on the inherited dirty r20 bytes, and the duplicate-execution
adjudication (§1.2 item 4) — all drafted in this
directory (log-entry-draft.md, report-draft.md, §2 above).]
