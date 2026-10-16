# Probe-battery TEMPLATE — standing preregistered live-route battery (kengaku-shokunin)

**What this is:** the reusable instrument every future round instantiates when it
runs the calibration axis-move: a small battery of falsifiable live-route probes
whose predictions are frozen (hashed, UTC) **before the first request**, executed
with receipts, and scored at close with an aggregate calibration read. It is
host-agnostic: no endpoint, port, or model id is baked in — §9 fills those in
per round from that round's own knowledge lands.

**Lineage (what it extracts from, with receipts):**

| Practice | Established | Evidence |
|---|---|---|
| Ex-ante predictions hashed before the first request, ordering proof | r9 | `corpus/evidence/round9-replication/predictions-r9.md` + `.sha256` + `ordering.log` (hash 21:17:48Z < first `request_ts` 21:17:58Z) |
| Probabilities (Brier) alongside point forecasts; mechanical exclusive verdict rule inside the hashed bundle; "what falsifies the design" pre-run checks | r11 | `corpus/evidence/round11-power/predictions-r11.md`, `prereg-bundle.sha256`, `analysis_r11.md` §Prediction scoring |
| Per-component prediction table (binary p / numeric point+range), hit-miss-unprovable scoring, aggregate hit-rate read | r18 parent battery | `../research/round-18-kimi-model-routing/battery/predictions/PREDICTIONS.{md,json,sha256}`, `battery/ANALYSIS.md` §7 |
| Standing multi-probe battery with registrar freeze gate, per-probe runner logs, quota etiquette | r19 (first instantiation of this template) | `plans/probe-battery-r19.md` (freeze-1 2026-10-16T07:52:04Z sha256 `e3f08a09…` superseded mid-window — BR-1; freeze-2 07:55:58Z `e1a86777…a00a1` valid; §7.1 freeze record), `corpus/evidence/probe-r19-*.log` (15 receipts; P2/P3/P8/P9 named UNRUN at close) |
| Freeze-after-last-edit guard (decoy scan + double-read + post-write recompute), UNRUN-probe completion gate, multi-round provenance table | r20 (template hardening from the r19 freeze record) | `corpus/knowledge/probe-battery-r19.md` §6 defects 2/3/11 + this template §5 step 3, §7 rules 1/5/6 |
| Calibration proxy this battery feeds (predictions before first request + scored at close) | SCORECARD | `SCORECARD.md:33-46` (proxy (a)-(c)) |

**Hard rule that never varies:** no outcome may precede its prediction. A breach
is recorded with receipts, never patched (r19 live example:
`corpus/evidence/probe-r19-opencode-health.log` §DEFECT 0 — two pre-freeze
requests recorded as out-of-band, excluded from scoring).

## 0. Round header (every instantiation starts here)

```
# Round-<N> probe battery — <one-line scope> (kengaku-shokunin)

**status: DRAFT — predictions NOT frozen.**
Runners: do **not** send any request until the FROZEN section carries a
`FROZEN:` line. The prediction-registrar freezes; the registrar gatekeeps
the ordering audit.

- drafted-by: battery-author seat, round-<N> wave (<routing bucket>)
- drafted_utc: <UTC>
- write-scope: this file only
- request-budget: ≤<B> HTTP requests total, ≤<T> output tokens, one attempt
  per probe, strictly sequential
- battery-author network state at draft time: <exact disclosure — every
  request/host-read made before this draft, with timestamps, and which
  predicted events (if any) they may have observed>
```

The disclosure line is mandatory (r19 precedent: `plans/probe-battery-r19.md`
header — two host reads disclosed, one of them informative for a probe's
prediction, hence that probe's honest-but-informed p=0.80). An undisclosed
pre-draft observation discovered later is an ordering defect.

## 1. Falsifiable claim (before → after)

State the round's claim in the form the calibration proxy scores: what was
true before (with `file:line` evidence and re-runnable commands), what exists
after (this file + the evidence logs + the knowledge land). Example: r19
before = "proxy ran 0/1, 1/1, 0/0, 1/1 across rounds 8–11, ad hoc, no
standing battery or template" (`SCORECARD.md:34-37`); after = "a frozen
battery of ≥6 falsifiable probes, receipts, scored at close, ordering
audited".

## 2. Roles and write ownership (fleet-wave form; solo rounds merge them)

| Role | Owns | Gate |
|---|---|---|
| battery-author | the battery file (§0–§6, §8) | cites every probe to a round receipt; discloses pre-draft network state |
| prediction-registrar | the `FROZEN:` line only | first freeze: verifies no evidence log exists yet; re-freeze: enumerates the logs already on disk instead (§5 step 6, r19 defect 3); computes the anchor hash with the §5 guards; stamps UTC |
| runners | `corpus/evidence/probe-r<NN>-*.log` only | wait for FROZEN; verify the hash; one file per probe |
| scorer + note-writer | `corpus/knowledge/probe-battery-r<NN>.md` | applies §7 scoring mechanically; lands the aggregate read |
| everyone | nothing else | SCORECARD.md / LOG.md are parent-owned; no git commits (parent integrates) |

## 3. Probe schema (one subsection per probe, P1..Pk)

Each probe carries exactly these fields — a probe without all of them is not
in the battery:

```
### P<i> — <imperative headline naming the route/state tested>

- **Hypothesis (falsifiable):** <one sentence, outcome-shaped: a specific
  status/body/timing/parity that can come out the other way>.
- **Source:** <file:line citations for every factual premise — a digest
  entry, a census row, a prior receipt. A probe with no receipt is a
  hunch, not a probe.>
- **Requests (<n>):** exact method + URL + body shape + headers (names
  only) + timeout. Any warm-up pre-call is listed here and marked
  "excluded from metrics" (devin-class cold start, r19 P4 / M3 idiom).
  Never "run script X" — inline the shape; running a prior round's script
  spends its own unbounded budget.
- **Predictions:** component ids in the §4 table.
- **Scoring:** Brier / abs-error+range / pass-fail per component.
- **Frame:** (when load-bearing) how to read the outcome — e.g. a 429 is a
  provider-meter event, not a model failure
  (`corpus/knowledge/ledger-route-telemetry.md:60-62`).
```

Zero-request probes are legal and encouraged: a probe may score components
off another probe's captured bytes (r19 P3, P5) — derived evidence, no extra
traffic.

## 4. Prediction component schema (one table, frozen as a whole)

```
| id | probe | type | prediction | p / point / range |
```

- **binary:** outcome is one event; file `p` ∈ (0,1). Use extremes honestly:
  p=0.93 means "would be surprised, not impossible". Never file p=1.0/0.0 —
  a certainty that misses ends the battery's calibration story.
- **numeric:** file a **point** (units named: ms, tokens, seconds) **and a
  range**; the range is the hit/miss boundary, the point feeds mean
  abs-error. Wide ranges where the basis is one prior draw (r18 lesson:
  "ranges are deliberately wide because the census numbers are single
  draws").
- **pass/fail structural claims** (a vector must match exactly): file as one
  binary component over the whole vector (r19 2a: status vector
  `[200,200,400,...]`).
- Every numeric prediction names its **basis** (which prior number it is
  shifted from) in the probe body — transferability across rounds is the
  point of fixed prompt shapes (reuse the same prompt text so numbers stay
  comparable, r19 P4 reusing the r18 census `COUNT_PROMPT`).
- **Where probabilities are feasible, file probabilities** — point-only
  rows are a calibration-rubric breach (`SKILL.md:564-566`; r9 lesson:
  "point predictions cannot be calibration-scored properly").
- **UNPROVABLE** is a filed-for state, not a failure: components whose probe
  ends UNRUN / TRANSPORT-UNREACHABLE are excluded from denominators and
  listed with reasons (r18 idiom: "a dead lane cannot lose a race").

File a "what would falsify the design itself" block (r11 idiom): seed/shape
checks, what makes the run void, what downgrades claims — **inside the
frozen text**, not in a later review (round-11 lesson 7).

## 5. Freeze discipline (the registrar procedure — never abbreviated)

1. Battery file sits in DRAFT with the status line from §0. Runners poll it
   (`sleep 30`) and send **nothing** — including "harmless" health checks —
   until the freeze exists. Any pre-freeze request is an ORDERING-BREACH:
   record it with verbatim receipts in the probe's log, mark it out-of-band,
   exclude it from scoring, fix the gate (r19 DEFECT 0: a `--live` flag that
   a dry mode never enforced).
2. Registrar verifies **no** `corpus/evidence/probe-r<NN>-*.log` exists yet.
3. Registrar computes the anchor hash — everything above the freeze anchor,
   so the whole prediction set + procedure is covered. The command must be
   **bracketed AND line-anchored**: an unbracketed pattern matches its own
   command text (r19 freeze-1's hash covered a truncated range — knowledge
   note §6 defect 2), and after bracketing, the template's own copied
   command text and the indented example comment below are still decoys
   (verified on a synthetic instantiation: unanchored forms stopped hashing
   at the copied command text — 8195 of 17140 bytes — and the bracketed but
   unanchored form stopped at the indented example comment; the line-anchored
   form reached the real anchor). Verified equivalent on the r19 bytes: both
   forms reproduce freeze-2 `e1a86777…a00a1` there.

   ```bash
   HASH=$(sed -n '1,/^<!-- FROZEN-PREDICTIONS-ANCHO[R] -->$/p' plans/probe-battery-r<NN>.md \
     | sha256sum | cut -d' ' -f1)
   NOW=$(date -u '+%Y-%m-%dT%H:%M:%SZ')
   ```

   Before stamping, the registrar also runs a **decoy scan** and confirms
   the hashed range ends at the real anchor:

   ```bash
   grep -n '^<!-- FROZEN-PREDICTIONS-ANCHOR -->$' plans/probe-battery-r<NN>.md
   sed -n '1,/^<!-- FROZEN-PREDICTIONS-ANCHO[R] -->$/p' plans/probe-battery-r<NN>.md | tail -n 1
   ```

   The `grep` must return exactly one line — the real anchor — and the
   `sed | tail` must print that same anchor line. Any other match (a
   command-text copy, an indented example) means a decoy sits above the
   anchor: bracket the pattern, re-anchor, or reword the decoy text, and
   re-run until the scan is clean.

   **Freeze after the LAST edit (the BR-1 TOCTOU guard).** The hash may be
   computed only once the prediction set is final: the registrar confirms
   with the battery-author that no further above-anchor edit is pending,
   computes the hash, waits ≥1 s, recomputes, and proceeds only if the two
   reads agree (double-read stability check, H1 == H2 — the r19 re-freeze
   practice). A hash computed over bytes that change before the FROZEN line
   is written covers the wrong text: that is the compute-then-write race
   that bit r19 (BR-1 — freeze-1 posted 07:52:04Z while above-anchor edits
   were still landing; RA-1 corrected the timeline, the discipline stands).

4. Registrar replaces the pending line below the anchor with exactly:

   ```
   <!-- FROZEN-PREDICTIONS-ANCHOR -->
   FROZEN: <NOW> sha256:<HASH>
   ```

   Immediately before writing, recompute the hash once more and write only
   if it still equals step 3's value (closes the compute-then-write race,
   r19 §7 step 4); after writing, recompute a third time and confirm it
   equals the posted FROZEN line.

5. Each runner, before its first request, re-runs step 3 and **fails loudly**
   unless the recomputed hash equals the FROZEN line's hash; it records both
   in its log header (`battery_sha256_at_start`, `frozen_line`,
   `first_request_utc`). r19: runners verified the then-live hash in both
   windows (freeze-1 `e3f08a09…` while it stood; freeze-2 `e1a86777…` after
   the re-freeze — registrar re-verified over 8 consecutive polls,
   runner-leg-hyper independently pre-execution). A runner citing a
   superseded hash is a §7-rule-1 gate mismatch, not a valid ordering proof
   (r19 devinleg exclusion).

6. Any edit above the anchor after the freeze **invalidates the freeze** and
   is recorded as a breach; the only repair is a re-freeze (step 3 again,
   full guard), with the superseded hash recorded as the identity of the
   pre-edit bytes, never silently replaced (r19 §7.1 BR-1/RA-1). Corrections
   land as appended errata below the anchor (hashed text freezes typos too —
   round-11 lesson 6). If a re-freeze lands after runners already executed,
   the freeze record must state which prediction rows are byte-identical
   across the two freezes — only those rows stay scoreable from the first
   window (r19 RA-3).
7. Ordering audit at close: for every log, `frozen_utc < first_request_utc`
   and the hashes match; else ORDERING-BREACH, affected outcomes excluded.

Multi-seat variant (used in r19, keep when runners are separate seats): a
runner MAY file **seat-level** frozen predictions in its own log before the
battery freeze (header block + `## FROZEN PREDICTIONS` section + sha256 of
that block, filed before ANY request to its target). Seat predictions
pre-date the battery freeze only if their hash timestamp says so; both
orderings are auditable from the logs.

## 6. Runner receipt schema (`corpus/evidence/probe-r<NN>-*.log`, one file per probe)

```
probe: P<i>
runner-seat: <seat id>
battery_sha256_at_start: sha256:<hash from the FROZEN line>
frozen_line: <FROZEN line verbatim>
first_request_utc: <UTC>
---
[1/n] <UTC> <METHOD> <URL>
exit: <curl/python exit>  http: <status or 000>  ms: <wall>
error: <none | transport detail>
headers-sent: Authorization=<len NN>, Content-Type=application/json, ...
response-headers: <non-credential headers with values; Set-Cookie redacted>
excerpt: <≤400 chars of body, credential-shaped strings stripped>
---
derived: <component-relevant reads, e.g. status=429 model_sent=... >
derived-usage: <usage block or None>
derived-timing: <ttft_content_ms / first_decoded_ms / decode_span_ms ...>
derived-text: <finish_reason, content_chars ...>
last_request_utc: <UTC>
outcome: <all-components-recorded | UNRUN: <reason> | TRANSPORT-UNREACHABLE | ...>
```

Redaction contract (the r18 hygiene-gate precedent, `TOTAL HITS: 0`): no
Authorization/api_key/session-header **values** — names and `<len N>`
markers only; no credential-shaped string (any `sk-…`, JWT, bearer) in any
artifact; SSE excerpts show event types and the fields being scored, not raw
bodies. Set-Cookie values are redacted like credentials.

Also record: pinned code/config digests the outcome depends on (shim script
sha256, config sha256) and the exact command line per entry. Every entry:
UTC stamp, exact command, exit, excerpt — a receipt is something another
seat can re-run or at least re-verify.

## 7. Scoring rules (scorer contract → `corpus/knowledge/probe-battery-r<NN>.md`)

1. **Completion gate — a battery is not closed while any probe is unrun.**
   At close, build the grid: every probe P1..Pk is **executed** (receipt log
   exists) or **UNRUN** (no log). UNRUN is a legal state only when named —
   never dropped from the tables or totals (r19 closed 5/9 with P2/P3/P8/P9
   named UNRUN, their frozen rows listed UNPROVABLE-by-unrun). An UNRUN
   probe gets, in order of preference: (i) run it in-round if request
   budget remains and the freeze stands — cheapest-first (zero-quota
   localhost/freshness probes run first; r19's P9, a single localhost GET,
   was among the unrun); (ii) carry it to the next instantiation against
   the SAME frozen predictions — the completing round scores it against the
   original freeze, never a re-freeze, never edited predictions; or
   (iii) record NOT-RUN with the reason (quota-dead lane, credential access
   out of seat scope, surface gone) and stop. The battery closes only when
   every probe is executed or NOT-RUN-reasoned, and the closing knowledge
   note states the grid (`executed/total`) plus, for every NOT-RUN probe,
   its reason and destination.
2. **Ordering gate (pass/fail for the whole battery).** For every runner
   log verify `frozen_utc < first_request_utc` and the §5 hash equality
   **as it stood at that log's execution time** (runners cannot see future
   edits — the only executable reading; r19 §1 gate table). Violation ⇒
   ORDERING-BREACH: affected outcomes excluded from the aggregate, breach
   recorded with receipts.
3. **Per-component scores.**
   - binary: Brier term `(p − o)²`, o ∈ {0,1};
   - numeric: signed error and abs-error in the named unit + range
     hit/miss;
   - UNRUN / TRANSPORT-UNREACHABLE ⇒ UNPROVABLE: excluded from denominators,
     listed with reasons.
4. **Per-probe verdict:** PASS iff every scored component hit (binary
   outcome on the >0.5 side of p; numeric inside range); else FAIL with
   signed misses shown. UNPROVABLE probes are neither.
5. **Aggregate calibration read — measurements, never axis scores:** (i)
   mean Brier over scored binaries with the always-0.5 reference (0.25)
   stated beside it as a comparison, not a grade; (ii) mean abs-error per
   numeric quantity, per unit; (iii) range hit-rate; (iv)
   pass/fail/unprovable counts. **Recompute on completion:** when a carried
   probe executes in a later round against the same freeze, the aggregate
   is recomputed across ALL executed binaries of the battery (not just that
   round's) and both readings — the partial close and the completed grid —
   are preserved, each with its denominator. The lane's idiom forbids
   scalar axis verdicts — these lines feed SCORECARD via the parent in
   proxy units.
6. **Multi-round provenance table (mandatory once a battery spans
   rounds).** The scoring note carries one table mapping every scored
   component to its origin:

   ```
   | id | probe | frozen in (freeze hash) | executed in (round) | receipt | scored in |
   ```

   The prediction set never moves: a completing round cites the ORIGINAL
   freeze hash, and the note records which freeze each outcome was scored
   against (r19 needed exactly this to adjudicate a mid-window re-freeze —
   RA-3's byte-identity test is the precedent). No silent re-basing of an
   aggregate to the completing round.
7. **Surprises are findings, not noise:** a falsified route-state
   prediction (leg-order flip, restored surface, changed error string) is
   recorded with its receipt and routed per PROVINCE §Refusals if it sits on
   an unowned plane (serving-plane state is report-out, not lane remediation).
8. **Report indeterminate honestly:** a probe whose verdict rule doesn't
   fire is reported as indeterminate, never laundered into a pass (round-9
   lesson).

## 8. Quota etiquette (binding on every instantiation)

- **Budget is enumerated, not approximate:** the battery's request list is
  the whole budget (r19: 19 requests, ≤240 output tokens, stated in the
  header). No widening mid-round; a new probe waits for the next round's
  freeze.
- **One attempt per probe.** A single retry only for connection-level
  failures (timeout / refused), and it counts against the budget.
- **A 429/401 ends the probe.** Quota-dead lanes get exactly one confirming
  call — never hammer; a second call cannot change the meter.
- **Sequential, ≥2 s between requests to the same upstream host;** no
  concurrency anywhere.
- **Stop conditions:** two consecutive transport failures on one lane, or
  any 5xx, end that probe (recorded as its outcome class).
- **Zero-quota probes are preferred when they can carry the hypothesis:**
  unauthenticated GETs (r19 P8) and localhost health/`/models` checks cost
  nothing; a 429 response itself is the measurement for a meter-state probe
  (r19 P1 — a dead key answering 429 *is* the predicted outcome).
- **Warm-ups are declared, listed, and excluded from metrics** (cold-start
  lanes), and their client timeout is set above the observed worst block
  (300 s + margin).
- **Scratch goes to `/tmp`; on `EDQUOT` move to `$HOME/.cache/kengaku-tmp`
  and delete it when done.** Nothing headline-bearing lives outside
  `corpus/evidence/`.

## 9. Instantiation checklist (how a future round uses this template)

1. **Pick hypotheses from the round's knowledge lands** — every probe cites
   a digest/receipt with `file:line` (r19 built all 9 probes from the r18
   routing digest + telemetry lands). Include at least one standing
   freshness probe over an ABSENT/DECLARED-DEAD surface so its restore is
   caught by the battery rather than by accident (r19 P9); a 200 there is a
   freshness event — report to the integrator, don't absorb a re-pin.
2. **Copy §0–§10, fill the placeholders:** round number, scope, budget,
   probes, prediction table. Delete nothing from §5/§7/§8 — they are the
   instrument.
3. **Draft → disclose → freeze → run → score → land → close the grid:**
   battery file (DRAFT), registrar freeze (§5), runner logs (§6), scorer's
   knowledge entry `corpus/knowledge/probe-battery-r<NN>.md` (§7), lessons
   per round convention, LOG/SCORECARD rows via the parent — then §9 step 7.
4. **Mock-smoke any runner script before the first real request** — a dry
   mode must default to **no network**, not "network unless --live is
   absent" (r19 DEFECT 0); a stdlib mock catches runtime defects without
   spending a live draw or breaking the ordering window (round-11 lesson 1).
5. **Host-agnostic means parameterized:** endpoints, ports, model ids,
   prompt text, and ranges come from the instantiating round's own lands —
   never from this file. If a future host has no shims, the probe classes
   (meter-state, auth-state, latency-hold, transport-stability,
   freshness-of-absence) still instantiate against whatever routes exist.
6. **Close the loop:** every probe scored at close **in the round it ran**
   (the r12 breach — scored only in r14 — bought no calibration credit,
   `SCORECARD.md:163`); landed bytes match run bytes or carry a recorded
   reason (proxy (e)).
7. **Close the grid before declaring the battery done** (the r19 close was
   5/9 — legal because the four were named UNRUN, but the battery was not
   finished):

   - [ ] every probe P1..Pk has a receipt log, or is carried to the next
         instantiation, or is NOT-RUN with a recorded reason (§7 rule 1);
   - [ ] carried probes execute against the ORIGINAL freeze — verify the
         FROZEN line's hash still recomputes before running them; never
         re-freeze to complete a battery;
   - [ ] the aggregate is recomputed across all executed binaries of the
         battery, and the partial-close reading is preserved beside it
         with both denominators (§7 rule 5);
   - [ ] the multi-round provenance table is filled (§7 rule 6) if any
         probe executed outside the instantiating round;
   - [ ] the closing note states the grid `executed/total` and, for every
         NOT-RUN probe, its reason and destination.
8. **A wave that instantiates the battery must assign every probe a named
   runner seat at dispatch** — the r19 wave left P2/P3/P8/P9 seatless and
   they went unrun (knowledge note §8.3); an unassigned probe is a
   dispatch defect, not a runner failure. Cheapest probes (zero-quota
   localhost/freshness) are assigned first — they are the ones that
   otherwise fall through.

## 10. Known defects of this instrument (so future rounds price them)

- Aggregate Brier over heterogeneous, positively-informed components is a
  *lower bound* on skill — the 0.25 reference is stated beside it, never
  treated as a baseline beaten (r19 §4 wording, inherited here).
- Battery probes are single-draw; ranges are wide by design and the battery
  measures route *state*, not model capability — no pass-rate claims ride
  on one probe.
- The anchor-hash freeze covers the file above the anchor only; anything a
  runner needs from *outside* the file (e.g. a script pinned by sha256)
  must be hashed into its own log before its first request (r19
  runner-shim-ds practice: code pin + seat-prediction block hash in the
  log header).
- Seat-level predictions pre-dating the battery freeze create two
  prediction clocks; both are auditable but the scorer must score the
  battery's components from §5-table predictions, and seat-level additions
  as secondary (clearly labelled) rows.
- The freeze is a procedure, not a lock — three r19-priced failure modes:
  (1) the freeze can race concurrent drafting (BR-1 TOCTOU — guarded by
  §5's freeze-after-last-edit double-read, but only if the registrar
  actually runs the guard); (2) the registrar's "no runner log exists"
  precondition is unsatisfiable at a re-freeze (r19 defect 3) — a re-freeze
  must instead enumerate the logs already on disk and state which
  prediction rows are byte-identical across freezes (r19 RA-3); (3) 1-second
  UTC resolution means a prediction filed in the same second as its request
  proves only `filed ≤ request`, never `filed < request` (r19 defect 13) —
  file seat predictions at least one second before the first request.
- Wave-run batteries skew their executed set: runner seats pick up the
  probes near their own lanes and the cheapest ones fall through (r19 ran
  the quota/transport probes; the codex service_tier set and the zero-quota
  freshness probe went unrun). The §7 rule 1 completion gate and §9 steps
  7–8 exist because of this; a partial close is honest only when the unrun
  probes are named and carried, never dropped.
- A template is a snapshot of one round's idioms — its examples go stale
  when that round's numbers are corrected (this file cited r19's superseded
  freeze hash and v1 budget until the r20 revision: knowledge note defect
  11). When instantiating, re-derive every example from the round's own
  lands; when revising, sweep every hash/figure against the landed record.
